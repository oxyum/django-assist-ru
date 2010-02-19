#coding: utf-8

from django.test import TestCase

from assist.api import parse_csv_report, parse_csv_action_response
from assist.forms import AssistMode1Form, AssistMode2Form
from assist.conf import SHOP_IDP

csv1 = u"Order Number;Comment;Paket date\r\n123;проверка;\r\n345;UNKNOWN;19.02.2010 04:59:14\r\n".encode('utf8')

class ParsersTest(TestCase):
    def testParseCsvReport(self):
        results = parse_csv_report(csv1)
        self.assertEqual(results, [{'OrderNumber':'123', 'Comment':u'проверка'},
                                   {'OrderNumber':'345', 'PacketDate': '2010-02-19 04:59:14'}])


class FormsTest(TestCase):

    def testMode1Form(self):
        form = AssistMode1Form()
        self.assertEqual(form.fields['Shop_IDP'].initial, SHOP_IDP)
        self.assertEqual(form.fields['Shop_IDP'].widget.is_hidden, True)

    def testMode2Form(self):
        form = AssistMode2Form()
        self.assertEqual(form.fields['Shop_IDP'].initial, SHOP_IDP)
        self.assertEqual(form.fields['Shop_IDP'].widget.is_hidden, True)


class ChargeTest(TestCase):

    def testErrorParsing(self):
        response = u'ERROR:Невозможно выполнить операцию по платежу!'.encode('utf8')
        data = parse_csv_action_response(response)
        self.assertEqual(data, {'ERROR': u'Невозможно выполнить операцию по платежу!'})

        self.assertEqual(parse_csv_action_response('ERROR:'.encode('utf8')), {'ERROR': u''})

