#coding: utf-8
import urllib
import urllib2
import csv
import socket
from datetime import datetime
from django.utils.datastructures import SortedDict

from assist import AssistChargeError
from assist.conf import GET_RESULTS_URL, REFUND_URL, CHARGE_URL, SHOP_IDP, LOGIN, PASSWORD
from assist.constants import FIELDS_MAPPING, ASSIST_FORMAT_CSV, ASSIST_RVR_SHOP, ASSIST_LANGUAGE_EN

def _load_url(url, data=None, timeout=None):
    """ Поддержка таймаутов для python < 2.6 """
    old_timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(timeout)
    try:
        response = urllib2.urlopen(url, data)
        return response.read()
    finally:
        socket.setdefaulttimeout(old_timeout)


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


def parse_csv_action_response(data):
    ''' Разобрать CSV-ответ на запрос финансового подтверждения или
        разблокировки/возврата средств.
    '''

    # В ответ приходит почему-то не список полей с результатами,
    # а только текст ошибки. Поэтому пока так.

    reader = csv.reader(data.splitlines(), delimiter=';')
    row = reader.next()
    d = SortedDict()
    for param in row:
        try:
            name, value = param.split(':', 1)
            d[name] = unicode(value, 'utf8')
        except ValueError:
            pass
    return d


def charge_bill(Billnumber, Subtotal_P=None, Currency=None,
                Language=ASSIST_LANGUAGE_EN, Format=ASSIST_FORMAT_CSV, S_FIELDS='*'):
    """ Отправить запрос на финансовое подтверждение при двустадийном режиме работы."""

    if Format != ASSIST_FORMAT_CSV:
        raise NotImplementedError('Only CSV responses are supported')

    data = [
        ('Shop_ID', SHOP_IDP),
        ('Login', LOGIN),
        ('PASSWORD', PASSWORD),
        ('Billnumber', Billnumber),
        ('Language', Language),
        ('Format', Format),
        ('S_FIELDS', S_FIELDS),
    ]

    if (Subtotal_P is not None):
        data.append(('Subtotal_P', Subtotal_P,))
    if (Currency is not None):
        data.append(('Currency', Currency,))

    response = _load_url(CHARGE_URL, urllib.urlencode(data), 60)

    # Данные, по идее, хорошо бы отпарсить и создать модель из них, но т.к.
    # приходят не данные, а признак ошибки, возвращаем просто что есть.
    result = parse_csv_action_response(response)
    if ("ERROR" in result) and (result['ERROR']):
        raise AssistChargeError(str(Billnumber)+' '+result['ERROR'].encode('utf8'))

    return result


def fetch_auth_report():
    """ Получить результаты авторизации через запрос к серверу ASSIST.
        По правилам ASSIST, нельзя выполнять чаще, чем 1 раз в 10 минут.
    """
    data = urllib.urlencode((
        ('Shop_ID', SHOP_IDP),
        ('Login', LOGIN),
        ('PASSWORD', PASSWORD),
        ('Header1', 1),
    ))
    response = _load_url(GET_RESULTS_URL, data, 60)
    return parse_csv_report(response)


def refund(Billnumber, Subtotal_P=None, Currency=None, Language=ASSIST_LANGUAGE_EN,
           Format=ASSIST_FORMAT_CSV, S_FIELDS='*', RVRReason=ASSIST_RVR_SHOP):
    """ Отменить авторизацию по кредитной карте или сделать возврат средств. """

    data = urllib.urlencode((
        ('Shop_ID', SHOP_IDP),
        ('Login', LOGIN),
        ('PASSWORD', PASSWORD),
        ('Billnumber', Billnumber),
        ('Language', Language),
        ('Format', Format),
        ('S_FIELDS', S_FIELDS),
    ))
    response = _load_url(REFUND_URL, data, 60)
    result = parse_csv_action_response(response)

    if ("ERROR" in result) and (result['ERROR']):
        raise AssistChargeError(str(Billnumber)+' '+result['ERROR'].encode('utf8'))

    return result