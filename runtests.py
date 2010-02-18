#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.management import call_command

settings.configure(
    INSTALLED_APPS=('assist',),
    DATABASE_ENGINE = 'sqlite3',

    ASSIST_SHOP_IDP = 'test_shop',
    ASSIST_LOGIN = 'test_login',
    ASSIST_PASSWORD = 'test_password',
)

if __name__ == "__main__":
    call_command('test', 'assist')
