#coding: utf-8
from django.db import models
from django.db.models import CharField, DateTimeField, IntegerField

from assist import AssistChargeError
from assist.managers import AssistAuthResultManager
from assist.api import charge_bill, refund

RESPONSE_CODE_CHOICES = (
    ('AS000', u'АВТОРИЗАЦИЯ УСПЕШНО ЗАВЕРШЕНА'),
    ('AS100', u'ОТКАЗ В АВТОРИЗАЦИИ'),
    ('AS101', u'ОТКАЗ В АВТОРИЗАЦИИ. Ошибочный номер карты'),
    ('AS102', u'ОТКАЗ В АВТОРИЗАЦИИ. Недостаточно средств'),
    ('AS104', u'ОТКАЗ В АВТОРИЗАЦИИ. Неверный срок действия карты'),
    ('AS105', u'ОТКАЗ В АВТОРИЗАЦИИ. Превышен лимит'),
    ('AS106', u'ОТКАЗ В АВТОРИЗАЦИИ. Неверный PIN'),
    ('AS107', u'ОТКАЗ В АВТОРИЗАЦИИ. Ошибка приема данных'),
    ('AS108', u'ОТКАЗ В АВТОРИЗАЦИИ. Подозрение на мошенничество'),
    ('AS109', u'ОТКАЗ В АВТОРИЗАЦИИ. Превышен лимит операций ASSIST'),
    ('AS110', u'Требуется авторизация по 3D-Secure'),
    ('AS200', u'ПОВТОРИТЕ АВТОРИЗАЦИЮ'),
    ('AS300', u'АВТОРИЗАЦИЯ В ПРОЦЕССЕ. ЖДИТЕ'),
    ('AS400', u'ПЛАТЕЖА С ТАКИМИ ПАРАМЕТРАМИ НЕ СУЩЕСТВУЕТ'),
    ('AS998', u'ОШИБКА СИСТЕМЫ. Свяжитесь с ASSIST'),
)

STATUS_CHOICES = (
    ('Authorized', u'Платеж прошел успешно'),
    ('Not authorized', u'Платеж не прошел'),
    ('Preauthorized', u'Авторизация при двустадийном механизме прошла успешно'),
    ('Not preauthorized', u'Авторизация при двустадийном механизме не прошла'),
    ('Captured', u'Финансовое подтверждение прошло успешно'),
    ('Not captured', u'Финансовое подтверждение не прошло'),
    ('Voided', u'Он-лайн отмена авторизации прошла успешно'),
    ('Not Voided', u'Он-лайн отмена авторизации не прошла'),
    ('Refunded', u'Возврат средств прошел успешно'),
    ('Not Refunded', u'Возврат средств не прошел'),
    ('Reversaled', u'Отмена авторизации прошла успешно'),
    ('Not Reversaled', u'Отмена авторизации не прошла'),
    ('in process', u'В процессе'),
)

PAYMENT_TRANSACTION_TYPE_CHOICES = (
    (1, u'Оплата кредитной картой'),
    (2, u'Предварительная авторизация кредитной карты (авторизация при двустадийном режиме работы)'),
    (3, u'Поставторизация кредитной карты (финансовое подтверждение)'),
    (4, u'Возврат средств по оплате кредитной картой (refund)'),
    (6, u'Chargeback средств по оплате кредитной картой'),
    (7, u'Он-лайн отмена авторизации по кредитной карте (void)'),
    (9, u'Reversal'),
    (10, u'Перевод средств WebMoney'),
    (20, u'Оплата средствами PayCash'),
    (24, u'Оплата средствами QIWI (в т. ч. Мобильный платеж Beeline)'),
)

class AssistAuthResult(models.Model):
    OrderNumber     = CharField(u'Номер заказа', max_length=128, null=True, blank=True, db_index=True)
    Response_Code   = CharField(u'Код возврата', max_length=5, null=True, blank=True) # choices = RESPONSE_CODE_CHOICES)
    Recommendation  = CharField(u'Расшифровка кода возврата', max_length=255, null=True, blank=True)
    Message         = CharField(u'Сообщение об ошибке', max_length=255, null=True, blank=True)
    Comment         = CharField(u'Комментарий', max_length=255, null=True, blank=True)
    Date            = DateTimeField(u'Дата и время оплаты', null=True, blank=True)
    Total           = CharField(u'Сумма операции', max_length=17, null=True, blank=True)
    Currency        = CharField(u'Код валюты', max_length=3, null=True, blank=True)
    CardType        = CharField(u'Тип платежного средства', max_length=128, null=True, blank=True)
    CardNumber      = CharField(u'Номер платежного средства', max_length=128, null=True, blank=True)
    LastName        = CharField(u'Фамилия', max_length=64, null=True, blank=True)
    FirstName       = CharField(u'Имя', max_length=64, null=True, blank=True)
    MiddleName      = CharField(u'Отчество', max_length=64, null=True, blank=True)
    Address         = CharField(u'Адрес', max_length=128, null=True, blank=True)
    Email           = CharField(u'Адрес электронной почты', max_length=64, null=True, blank=True)
    Country         = CharField(u'Код страны банка-эмитента', max_length=3, null=True, blank=True)
    Rate            = CharField(u'Курс валюты', max_length=17, null=True, blank=True,
                                help_text=u'в настоящий момент не передается')
    ApprovalCode    = CharField(u'Код авторизации', max_length=6, null=True, blank=True)
    CardSubType     = CharField(u'Подтип карты', max_length=128, null=True, blank=True)
    CVC2            = CharField(u'Наличие CVC2/CVV2/4DBC', max_length=1, null=True, blank=True,
                                help_text=u'0 – авторизация без CVC2, 1 – авторизация с СVC2')
    CardHolder      = CharField(u'Держатель карты', max_length=128, null=True, blank=True)
    IPAddress       = CharField(u'IP-адрес покупателя', max_length=15, null=True, blank=True)
    ProtocolTypeName = CharField(u'Тип протокола (SET/NET/POS)', max_length=128, null=True, blank=True)
    BillNumber      = CharField(u'Номер платежа', max_length=16, null=True, blank=True, db_index=True,
                                help_text=u'Номер платежа в системе ASSIST')
    BankName        = CharField(u'Название банка-эмитента', max_length=128, null=True, blank=True)
    Status          = CharField(u'Состояние заказа', max_length=128, null=True, blank=True,
                                choices = STATUS_CHOICES)
    Error_Code      = CharField(u'Код ответа процессингового центра', max_length=64, null=True, blank=True)
    Error_Comment   = CharField(u'Расшифровка кода ответа процессингового центра', max_length=128, null=True, blank=True)
    ProcessingName  = CharField(u'Наименование процессингового центра', max_length=128, null=True, blank=True)
    PacketDate      = DateTimeField(u'Дата и время запроса', null=True, blank=True)
    PatmentType     = IntegerField(u'Тип транзакции', null=True, blank=True,
                                   choices = PAYMENT_TRANSACTION_TYPE_CHOICES)

    objects = AssistAuthResultManager()

    def __unicode__(self):
        return u"Результат авторизации в Assist %s (заказ %s): %s" % (
                self.BillNumber, self.OrderNumber, self.Status)

    class Meta:
        verbose_name = u'Результат авторизации в системе Assist'
        verbose_name_plural = u'Результаты авторизации в системе Assist'

    def charge(self):
        if (self.Status == 'Preauthorized'):
            return charge_bill(self.BillNumber)
        raise AssistChargeError('Invalid bill status')

    def refund(self):
        return refund(self.BillNumber)

