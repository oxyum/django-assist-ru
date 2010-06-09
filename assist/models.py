#coding: utf-8
from datetime import datetime
from django.db import models
from django.db.models import CharField, DateTimeField, IntegerField

from assist import AssistChargeError
from assist.managers import AssistAuthResultManager
from assist.api import charge_bill, refund
from assist.constants import RESPONSE_CODE_CHOICES, STATUS_CHOICES, PAYMENT_TRANSACTION_TYPE_CHOICES
from assist.utils import get_changes_between_models

class AssistResultChange(models.Model):
    auth_result = models.ForeignKey('AssistAuthResult', verbose_name=u'Результат авторизации в Assist')
    changed_at = DateTimeField(u'Дата и время изменения', default=datetime.now)
    changes = models.TextField(u'Что изменилось')

    class Meta:
        verbose_name = u'Изменения в результатах Assist'
        verbose_name_plural = u'Журнал изменений результатов Assist'
        ordering=['-id']


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
        raise AssistChargeError('%s: Invalid bill status (%s)' % (self.BillNumber, self.Status))

    def refund(self):
        return refund(self.BillNumber)

    def _log_changes(self, old):
        changes = get_changes_between_models(old, self, excludes=['PacketDate'])
        changes_txt = "\n".join(["%s: %s -> %s" % (f, changes[f][0], changes[f][1]) for f in changes])
        if changes:
            # приписываем историю к старому результату, т.к. id у нового будет тем же
            AssistResultChange.objects.create(auth_result = old, changes = changes_txt)


