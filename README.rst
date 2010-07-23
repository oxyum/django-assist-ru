================
django-assist-ru
================

django-assist-ru - это приложение для интеграции платежной системы ASSIST в
проекты на Django.

До использования следует ознакомиться с официальной документацией
ASSIST (http://assist.ru/files/manual_new.pdf). Приложение реализует
протокол взаимодействия, описанный в этом документе.

Установка
=========

Как обычно::

    $ pip install django-assist-ru

или ::

    $ easy_install django-assist-ru

или ::

    $ hg clone http://bitbucket.org/kmike/django-assist-ru/
    $ cd django-assist-ru
    $ python setup.py install


Потом следует добавить 'assist' в INSTALLED_APPS и выполнить ::

    $ python manage.py syncdb

Если используется South, то вместо syncdb нужно сделать ::

    $ python manage.py migrate


Настройка
=========

В settings.py нужно указать следующие настройки:

* ASSIST_SHOP_IDP - идентификатор магазина (число)
* ASSIST_LOGIN - логин
* ASSIST_PASSWORD - пароль

Необязательные параметары:

* ASSIST_TEST_MODE - включен ли тестовый режим. По умолчанию False (т.е. включен боевой режим).
* ASSIST_SERVER - адрес "боевого" сервера Assist. По умолчанию - https://secure.assist.ru


Использование
=============

Форму для приема платежей следует показывать на странице, у которой кодировка
1251. Для тех, кто использует кодировку utf-8, в django-assist-ru есть
декоратор cp1251, который перекодирует страницу в 1251, исправляет
http-заголовки и меняет meta-теги на нужные ::

    from assist.decorators import cp1251

    @cp1251
    @login_required
    def go_to_assist(request)
        ...


Формы для приема платежей
-------------------------

Для того, чтобы упростить конструирование html-форм для отправки пользователей в
ASSIST, в django-assist-ru есть 2 формы: AssistMode1Form и AssistMode2Form
(для 2х режимов работы ASSIST). Эти формы нужны не для валидации данных, а для
упрощения вывода информации в шаблонах.

Пример::

    # views.py

    from django.shortcuts import get_object_or_404
    from django.views.generic.simple import direct_to_template
    from django.contrib.auth.decorators import login_required

    from assist.decorators import cp1251
    from assist.forms import AssistMode2Form

    @cp1251
    @login_required
    def go_to_assist(request, order_id)
        order = get_object_or_404(Order, pk = order_id)
        form = AssistMode2Form(initial={
                   'Order_IDP': order.id,
                   'Subtotal_P': order.total,
                   'Comment': order.name,
                   'LastName': request.user.last_name,
                   'FirstName': request.user.first_name,
                   'Email': request.user.email,
                   'Phone': request.user.get_profile().phone,
               })
        return direct_to_template(request, 'go_to_assist.html', {'form': form})

За полным перечнем допустимых в initial полей можно обратиться к документации
ASSIST или к исходникам, названия полей совпадают.

django-assist-ru не включает в себя модели "Покупка", т.к. эта модель будет
отличаться от сайта к сайту. Задача разработчика - сформировать и передать
параметры Order_IDP (номер заказа) и Subtotal_P (сумма заказа) в форму.
Остальные поля являются необязательными.

Соответствующий шаблон::

    {% extends 'base.html' %}

    {% block content %}
        <form action="{{ form.target }}" method="POST">
            <p>{{ form.as_p }}</p>
            <p><input type="submit" name='SUBMIT' value="Купить"></p>
        </form>
    {% endblock %}

Форма выведется в виде набора скрытых input-тегов.

У форм AssistMode1Form и AssistMode2Form есть атрибут target, содержащий URL,
по которому форму следует отправлять. В тестовом режиме это будет тестовый URL,
в боевом - боевой.


Получение результатов платежей
------------------------------

::

    from assist.models import AssistAuthResult
    AssistAuthResult.objects.update_auth_report()

Метод получает результаты авторизации через запрос к серверу ASSIST и
создает/обновляет по ним записи в БД (по одной записи AssistAuthResult на
каждый BillNumber).

По правилам ASSIST, не стоит выполнять эту операцию чаще, чем 1 раз в 10 минут.

Не следует выполнять эту операцию при возврате пользователя со
страницы оплаты, лучше делать это по расписанию.


Получение актуального статуса платежа по заказу
-----------------------------------------------

Результат последней транзакции не обязательно является актуальным статусом
платежа в Assist, и учет только последней транзакции по заказу может
привести к тому, что некоторые платежи потеряются.

Транзакция со статусом 'in process' создается при каждом переходе
пользователя на страницу оплаты Assist. Поэтому можно создать сразу
несколько сессий оплаты "in process" и оплатить более раннюю.
В итоге последним (как по дате, так и по номеру) окажется результат со
статусом "in process" вместо "оплачено". Затем этот "in process" перейдет
в "ничего не вышло" по таймауту, и мы будем иметь неоплаченный заказ,
хотя на самом деле заказ был оплачен.

Чтобы избежать проблем в этой ситуации, применен следующий подход:

* Если есть какая-то транзакция с позитивным результатом (например,
  'Authorized'), то транзакции с соответствующим негативным результатом
  (для 'Authorized' это 'Not authorized') игнорируются.
* Статус "in process" не учитывается совсем. Для действий, инициируемых
  пользователем, этот статус означает только то, что человек зашел на
  страницу ASSIST. Для действий, инициируемых программно, статус 'in process'
  не гарантирует ни уникальности, ни последовательности выполнения операции.
  Вместо проверки, было ли начато выполнение операции, можно выполнять
  повторное инициирование операции, это безопасно для операций съема средств:
  в худшем случае просто получим ошибку от ASSIST.

В django-assist-ru есть метод менеджера модели, реализующий описанный подход::

    from assist.models import AssistAuthResult
    order_id = 145
    bill = AssistAuthResult.objects.actual_for_order(order_id)

Двустадийный режим работы
-------------------------

При двустадийном механизме работы разделены процессы авторизации кредитной
карты и совершения финансовой транзакции.

Для того, чтобы активировать двустадийный режим, следует передать параметр
Delay=1 при создании формы::

    @cp1251
    @login_required
    def go_to_assist(request, order_id)
        order = get_object_or_404(Order, pk = order_id)
        form = AssistMode1Form(initial={
                   'Order_IDP': order.id,
                   'Subtotal_P': order.total,
                   'Delay': 1
               })
        return direct_to_template(request, 'go_to_assist.html', {'form': form})

Деньги будут не списываться со счета, а блокироваться. Списание денег со счета
инициируется отдельно (в течение 14 дней с момента блокировки) с помощью метода
charge::

    bill = AssistAuthResult.objects.get(id=123)
    bill.charge()

Разблокировать деньги, не дожидаясь 14 дней, можно с помощью метода
refund::

    bill = AssistAuthResult.objects.get(id=123)
    bill.refund()

Возврат средств за оплаченный заказ осуществляется этой же командой.
