#coding: utf-8

from django.conf import settings

SHOP_IDP = settings.ASSIST_SHOP_IDP
TEST_MODE = getattr(settings, 'ASSIST_TEST_MODE', True)

TEST_MODE1_URL = "https://test.assist.ru/shops/purchase.cfm"
TEST_MODE2_URL = "https://test.assist.ru/shops/cardpayment.cfm"

MODE1_URL = "https://secure.assist.ru/shops/purchase.cfm"
MODE2_URL = "https://secure.assist.ru/shops/cardpayment.cfm"

TEST_RESULTS_URL = "https://test.assist.ru/results/results.cfm"
RESULTS_URL = "https://secure.assist.ru/results/results.cfm"

CONFIRM_URL = "https://secure.assist.ru/postauths/postauth.cfm"

RETURN_URL = "https://secure.assist.ru/rvr/rvr.cfm"
