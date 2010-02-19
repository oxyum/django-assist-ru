================
django-assist-ru
================

django-assist-ru - это приложение для интеграции платежной системы ASSIST в
проекты на Django.

До использования следует ознакомиться с официальной документацией
ASSIST (http://assist.ru/files/manual_new.pdf).


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

Необязательный параметар: ASSIST_TEST_MODE - включен ли тестовый режим.
По умолчанию False (т.е. включен боевой режим).


Использование
=============

Форму для приема платежей следует показывать на странице, у которой кодировка
1251. Для тех, кто использует кодировку utf-8, в django-assist-ru есть
декоратор cp1251::

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

Соответствующий шаблон::

    {% extends 'base.html' %}

    {% block content %}
        <form action="{{ form.target }}" method="POST">
            <p>{{ form.as_p }}</p>
            <p><input type="submit" class="button" name='SUBMIT' value="Купить"></p>
        </form>
    {% endblock %}

Форма выведется в виде набора скрытых input-тегов.

У форм AssistMode1Form и AssistMode2Form есть атрибут target, содержащий URL,
по которому форму следует отправлять. В тестовом режиме это будет тестовый URL,
в боевом - боевой.

