#coding: utf-8
import urllib
import urllib2
import csv
from datetime import datetime

from django.db import models
from django.utils.datastructures import SortedDict

from assist.conf import CHARGE_URL, GET_RESULTS_URL, SHOP_IDP, LOGIN, PASSWORD

# Названия полей, которые приходят в CSV, не совпадают с теми, что описаны в
# приложении 5.4, поэтому явно прописываем соответствие
FIELDS_MAPPING = {
    'Order Number': 'OrderNumber',
    'Result Code': 'Response_Code',
    'Recommendation': 'Recommendation',
    'Message': 'Message',
    'Comment': 'Comment',
    'Order Date': 'Date',
    'Order Total': 'Total',
    'Currency Code': 'Currency',
    'Card Type': 'CardType',
    'Card Number': 'CardNumber',
    'Lastname': 'LastName',
    'Firstname': 'FirstName',
    'Middlename': 'MiddleName',
    'Address': 'Address',
    'E-mail': 'Email',
    'Country Code': 'Country',
    'Currency rate': 'Rate',
    'Approval Code': 'ApprovalCode',
    'Mean Subtype': 'CardSubType',
    'CVC2 Exist': 'CVC2',
    'Cardholder': 'CardHolder',
    'IP-address': 'IPAddress',
    'Protocol Type': 'ProtocolTypeName',
    'Payment No.': 'BillNumber',
    'Bank issuer': 'BankName',
    'Order State': 'Status',
    'Processing System Response Code': 'Error_Code',
    'Processing System Response Code Description': 'Error_Comment',
    'Paket date': 'PacketDate',
#    'Digital Signature': '_Signature',
    'Processing System Name': 'ProcessingName',
    'Payment Type': 'PatmentType',
}


ASSIST_FORMAT_CSV = 1
ASSIST_FORMAT_WDDX = 2
ASSIST_FORMAT_XML = 3
ASSIST_FORMAT_SOAP = 4

def _convert_row_dates(row):
    ''' Преобразовать даты из формата ASSIST в формат Django '''
    for field in ('Date', 'PacketDate'):
        if field in row:
            dt = datetime.strptime(row[field], '%d.%m.%Y %H:%M:%S')
            row[field] = dt.strftime('%Y-%m-%d %H:%M:%S')

def parse_csv_report(data):
    ''' Разобрать CSV-ответ на запрос результатов авторизации. '''
    reader = csv.reader(data.splitlines(), delimiter=';')
    fields = reader.next()
    results = []
    for row in reader:
        d = SortedDict()
        for k,v in zip(fields, row):
            if v in ('UNKNOWN', ''):
                continue
            if k and k in FIELDS_MAPPING:
                d[FIELDS_MAPPING[k]]=unicode(v, 'utf8')
        _convert_row_dates(d)
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

    def update_auth_report(self):
        """ Получить результаты авторизации через запрос к серверу ASSIST.
            По правилам ASSIST, нельзя выполнять чаще, чем 1 раз в 10 минут.
            Получает все данные за последние 3 дня и создает/обновляет по
            ним нужные записи в БД (по одной записи на каждый BillNumber).
        """
        data = urllib.urlencode((
                   ('Shop_ID', SHOP_IDP),
                   ('Login', LOGIN),
                   ('PASSWORD', PASSWORD),
                   ('Header1', 1),
               ))
        response = urllib2.urlopen(GET_RESULTS_URL, data)
        results = parse_csv_report(response.read())
        for row in results:
            instance = self.model(**row)
            try:
                old_instance = self.get(BillNumber=instance.BillNumber)
                pk = old_instance.pk
            except self.model.DoesNotExist:
                pk = None
            instance.pk = pk
            instance.save()
        return results
