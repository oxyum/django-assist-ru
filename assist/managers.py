#coding: utf-8
import urllib
import urllib2

from django.db import models

from assist.conf import FINANCIAL_CONFIRM_URL, SHOP_IDP, LOGIN, PASSWORD

ASSIST_FORMAT_CSV = 1
ASSIST_FORMAT_WDDX = 2
ASSIST_FORMAT_XML = 3
ASSIST_FORMAT_SOAP = 4

class AssistAuthResultManager(models.Manager):

    def financial_confirmation(self, Billnumber,
                               Subtotal_P=None, Currency=None, Language=1,
                               Format=ASSIST_FORMAT_CSV, S_FIELDS='*'):
        """ Отправить запрос на финансовое подтверждение при двустадийном режиме
        работы. На основании ответа создать экземпляр модели."""

        if Format != ASSIST_FORMAT_CSV:
            raise NotImplementedError('Only CSV responses are supported')

        bill = self.get(BillNumber = Billnumber)
        data = urllib.urlencode((
                   ('Billnumber', Billnumber),
                   ('Shop_ID', SHOP_IDP),
                   ('Login', LOGIN),
                   ('PASSWORD', PASSWORD),
                   ('Subtotal_P', Subtotal_P or bill.Total),
                   ('Currency', Currency or bill.Currency),
                   ('Language', Language),
                   ('Format', Format),
                   ('S_FIELDS', S_FIELDS),
               ))
        response = urllib2.urlopen(FINANCIAL_CONFIRM_URL, data)
        data = response.read().decode('1251').encode('utf8')

        # А тут данные нужно отпарсить и создать модель из них, но т.к. данных
        # реальных нет и из мануала ничего не понятно, пока ничего не делаем
        auth_result = {}
        return self.create(**auth_result)
