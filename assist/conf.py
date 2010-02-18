#coding: utf-8
from django.conf import settings

# обязательные параметры - реквизиты магазина
SHOP_IDP = settings.ASSIST_SHOP_IDP
LOGIN = settings.ASSIST_LOGIN
PASSWORD = settings.ASSIST_PASSWORD

# тестовый режим или нет
TEST_MODE = getattr(settings, 'ASSIST_TEST_MODE', False)

# константы с адресами различных сервисов ASSIST
TEST_MODE1_URL = "https://test.assist.ru/shops/purchase.cfm"
TEST_MODE2_URL = "https://test.assist.ru/shops/cardpayment.cfm"
TEST_GET_RESULTS_URL = "https://test.assist.ru/results/results.cfm"
MODE1_URL = "https://secure.assist.ru/shops/purchase.cfm"
MODE2_URL = "https://secure.assist.ru/shops/cardpayment.cfm"
GET_RESULTS_URL = "https://secure.assist.ru/results/results.cfm"
CHARGE_URL = "https://secure.assist.ru/postauths/postauth.cfm"
REFUND_URL = "https://secure.assist.ru/rvr/rvr.cfm"