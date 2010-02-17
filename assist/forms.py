#coding: utf-8

from django import forms
from django.forms import CharField, IntegerField, DecimalField

class HiddenForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(HiddenForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            field.widget = forms.HiddenInput()


class AssistMode1Form(HiddenForm):
    Shop_IDP        = IntegerField(u'Идентификатор магазина в ASSIST')
    Order_IDP       = CharField(u'Номер заказа в системе расчетов Интернет-магазина', max_length=128,
                                help_text=u'Номер заказа должен быть уникален, иначе платеж будет неуспешным')
    Subtotal_P      = DecimalField(u'Сумма платежа в оригинальной валюте', max_digits=17, decimal_places = 2)
    Currency        = CharField(u'Код валюты, в которой указана сумма платежа Subtotal_P', max_length=3, required=False)
    Language        = IntegerField(u'Язык авторизационных страниц ASSIST', required=False, default=0)
    Delay           = IntegerField(u'Признак авторизации кредитной карты при двустадийном механизме работы', required=False, default=0)
    URL_RETURN      = CharField(u'URL страницы, на которую должен вернуться покупатель после осуществления платежа при нажатии кнопки «Вернуться в магазин»', max_length=128, required=False)
    URL_RETURN_OK   = CharField(u'URL страницы, куда должен вернуться покупатель после успешного осуществления платежа', max_length=128, required=False)
    URL_RETURN_NO   = CharField(u'URL страницы, куда должен вернуться покупатель после неуспешного осуществления платежа', max_length=128, required=False)
    Comment         = CharField(u'Комментарий', max_length=255, required=False,
                                help_text=u'передается в ASSIST и отображается в выписках по операциям')
    ChoosenCardType = IntegerField(u'Идентификатор типа карты для оплаты.', required=False,
                                   help_text=u"1 – VISA 2 - EC/MC 3 – DCL 4 – JCB 5- AMEX. Покупатель сможет оплатить покупку только картой указанного типа (указанный тип карт должен быть активирован для магазина).")
    CardPayment     = IntegerField(u'Может ли покупатель сделать платеж по кредитной карте', required=False, default=1)
    WebMoneyPayment = IntegerField(u'Может ли покупатель сделать платеж', default=1, required=False)
    PayCashPayment  = IntegerField(u'Может ли покупатель сделать платеж с помощью платежной системы PayCash', default=1, required=False)
    QiwiBeelinePayment = IntegerField(u'Может ли покупатель сделать платеж с помощью платежного средства «Мобильный платеж. Интернет (Билайн)» системы QIWI', default=1, required=False)
    AssistIDCCPayment = IntegerField(u'Может ли покупатель сделать платеж по кредитной карте с использованием Assist®ID', default=1, required=False)

class AssistMode2Form(AssistMode1Form):
    LastName = CharField(u'Фамилия', max_length=64)
    FirstName = CharField(u'Имя', max_length=64)
    MiddleName = CharField(u'', max_length=64, required=False)
    Email = forms.EmailField(u'Электронный адрес', max_length=64)
    Phone = CharField(u'Телефон', max_length=64, required=False)
    Address = CharField(u'Адрес', max_length=128, required=False)
    Country = CharField(u'Код страны покупателя', max_length=3, required=False)
    State = CharField(u'Код штата/региона', max_length=3, required=False)
    City = CharField(u'Город', max_length=64, required=False)
    Zip = CharField(u'Почтовый индекс', max_length=64, required=False)
