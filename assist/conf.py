#coding: utf-8
from django.conf import settings

from assist.constants import *

# обязательные параметры - реквизиты магазина
SHOP_IDP = settings.ASSIST_SHOP_IDP
LOGIN = settings.ASSIST_LOGIN
PASSWORD = settings.ASSIST_PASSWORD

# тестовый режим или нет
TEST_MODE = getattr(settings, 'ASSIST_TEST_MODE', False)

if TEST_MODE:
    MODE1_URL = TEST_MODE1_URL
    MODE2_URL = TEST_MODE2_URL
    GET_RESULTS_URL = TEST_GET_RESULTS_URL
else:
    MODE1_URL = REAL_MODE1_URL
    MODE2_URL = REAL_MODE2_URL
    GET_RESULTS_URL = REAL_GET_RESULTS_URL
