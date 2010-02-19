#coding: utf-8

from django.test import TestCase

from assist.managers import parse_csv_response
from assist.forms import AssistMode1Form, AssistMode2Form
from assist.conf import SHOP_IDP

csv1 = """Order Number;Comment\r\n123;test\r\n345;UNKNOWN\r\n""".encode('1251')

class ParsersTest(TestCase):
    def testParseCsvResponse(self):
        results = parse_csv_response(csv1)
        self.assertEqual(results, [{'OrderNumber':'123', 'Comment':'test'},
                                   {'OrderNumber':'345'}])


class FormsTest(TestCase):

    def testMode1Form(self):
        form = AssistMode1Form()
        self.assertEqual(form.fields['Shop_IDP'].initial, SHOP_IDP)
        self.assertEqual(form.fields['Shop_IDP'].widget.is_hidden, True)

    def testMode2Form(self):
        form = AssistMode2Form()
        self.assertEqual(form.fields['Shop_IDP'].initial, SHOP_IDP)
        self.assertEqual(form.fields['Shop_IDP'].widget.is_hidden, True)
