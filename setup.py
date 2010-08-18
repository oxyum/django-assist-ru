#!/usr/bin/env python
#coding: utf-8
from distutils.core import setup

import sys
reload(sys).setdefaultencoding("UTF-8")

setup(
    name='django-assist-ru',
    version='0.6.0',
    author='Mikhail Korobov',
    author_email='kmike84@gmail.com',

    packages=['assist', 'assist.migrations'],

    url='http://bitbucket.org/kmike/django-assist-ru/',
    download_url = 'http://bitbucket.org/kmike/django-assist-ru/get/tip.zip',
    license = 'MIT license',
    description = u'Приложение для интеграции платежной системы ASSIST в проекты на Django.'.encode('utf8'),
    long_description = open('README.rst').read().decode('utf8'),

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Natural Language :: Russian',
    ],
)
