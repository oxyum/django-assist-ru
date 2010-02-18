#coding: utf-8
import urllib
import urllib2
import csv
import os

from django.db import models

from assist.conf import CHARGE_URL, GET_RESULTS_URL, SHOP_IDP, LOGIN, PASSWORD

ASSIST_FORMAT_CSV = 1
ASSIST_FORMAT_WDDX = 2
ASSIST_FORMAT_XML = 3
ASSIST_FORMAT_SOAP = 4

def parse_csv_response(data):
    reader = csv.reader(data.decode('1251').encode('utf8').strip().split(os.linesep), delimiter=';')
    fields = reader.next()
    results = []
    for row in reader:
        d = {}
        for k,v in zip(fields, row):
            d[k]=v
        results.append(d)
    return results

class AssistAuthResultManager(models.Manager):

    def charge(self, Billnumber,
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
        response = urllib2.urlopen(CHARGE_URL, data)
        data = response.read().decode('1251').encode('utf8')
        print data

        # А тут данные нужно отпарсить и создать модель из них, но т.к. данных
        # реальных нет и из мануала ничего не понятно, пока ничего не делаем
        auth_result = {}
        return self.create(**auth_result)

    def fetch_auth_results(self):
        """ Получить результаты авторизации через запрос к серверу ASSIST.
            По правилам ASSIST, нельзя выполнять чаще, чем 1 раз в 10 минут.
            Получает все данные за последние 3 дня и создает по ним нужные
            записи в БД.
        """
        data = urllib.urlencode((
                   ('Shop_ID', SHOP_IDP),
                   ('Login', LOGIN),
                   ('PASSWORD', PASSWORD),
                   ('Header1', 1),
               ))
        response = urllib2.urlopen(CHARGE_URL, data)
        results = parse_csv_response(response.read())
