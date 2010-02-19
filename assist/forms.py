#coding: utf-8

from django import forms
from django.forms import CharField, IntegerField, DecimalField

from assist.conf import SHOP_IDP, TEST_MODE, MODE1_URL, MODE2_URL

class HiddenForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(HiddenForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget = forms.HiddenInput()


class AssistMode1Form(HiddenForm):
    Shop_IDP        = IntegerField(label=u'Идентификатор магазина в ASSIST', initial = SHOP_IDP)
    Order_IDP       = CharField(label=u'Номер заказа в системе расчетов Интернет-магазина', max_length=128,
                                help_text=u'Номер заказа должен быть уникален, иначе платеж будет неуспешным')
    Subtotal_P      = DecimalField(label=u'Сумма платежа в оригинальной валюте', max_digits=17, decimal_places = 2)
    Currency        = CharField(label=u'Код валюты, в которой указана сумма платежа Subtotal_P', max_length=3, required=False)
    Language        = IntegerField(label=u'Язык авторизационных страниц ASSIST', required=False, initial=0)
    Delay           = IntegerField(label=u'Признак авторизации кредитной карты при двустадийном механизме работы', required=False, initial=0)
    URL_RETURN      = CharField(label=u'URL страницы, на которую должен вернуться покупатель после осуществления платежа при нажатии кнопки «Вернуться в магазин»', max_length=128, required=False)
    URL_RETURN_OK   = CharField(label=u'URL страницы, куда должен вернуться покупатель после успешного осуществления платежа', max_length=128, required=False)
    URL_RETURN_NO   = CharField(label=u'URL страницы, куда должен вернуться покупатель после неуспешного осуществления платежа', max_length=128, required=False)
    Comment         = CharField(label=u'Комментарий', max_length=255, required=False,
                                help_text=u'передается в ASSIST и отображается в выписках по операциям')
    ChoosenCardType = IntegerField(label=u'Идентификатор типа карты для оплаты.', required=False,
                                   help_text=u"1 – VISA 2 - EC/MC 3 – DCL 4 – JCB 5- AMEX. Покупатель сможет оплатить покупку только картой указанного типа (указанный тип карт должен быть активирован для магазина).")
    CardPayment     = IntegerField(label=u'Может ли покупатель сделать платеж по кредитной карте', required=False, initial=1)
    WebMoneyPayment = IntegerField(label=u'Может ли покупатель сделать платеж', initial=1, required=False)
    PayCashPayment  = IntegerField(label=u'Может ли покупатель сделать платеж с помощью платежной системы PayCash', initial=1, required=False)
    QiwiBeelinePayment = IntegerField(label=u'Может ли покупатель сделать платеж с помощью платежного средства «Мобильный платеж. Интернет (Билайн)» системы QIWI', initial=1, required=False)
    AssistIDCCPayment = IntegerField(label=u'Может ли покупатель сделать платеж по кредитной карте с использованием Assist®ID', initial=1, required=False)
    DemoResult = CharField(label=u'', max_length=5, required=True, initial='AS000')

    target = MODE1_URL

    def __init__(self, *args, **kwargs):
        super(AssistMode1Form, self).__init__(*args, **kwargs)
        if not TEST_MODE:
            del self.fields['DemoResult']


class AssistMode2Form(AssistMode1Form):
    LastName = CharField(label=u'Фамилия', max_length=64)
    FirstName = CharField(label=u'Имя', max_length=64)
    MiddleName = CharField(label=u'Отчество', max_length=64, required=False)
    Email = forms.EmailField(label=u'Электронный адрес', max_length=64)
    Phone = CharField(label=u'Телефон', max_length=64, required=False)
    Address = CharField(label=u'Адрес', max_length=128, required=False)
    Country = CharField(label=u'Код страны покупателя', max_length=3, required=False)
    State = CharField(label=u'Код штата/региона', max_length=3, required=False)
    City = CharField(label=u'Город', max_length=64, required=False)
    Zip = CharField(label=u'Почтовый индекс', max_length=64, required=False)

    target = MODE2_URL
