#!/usr/bin/env python
#coding: utf-8
from distutils.core import setup

setup(
    name='django-assist-ru',
    version='0.1.0',
    author='Mikhail Korobov',
    author_email='kmike84@gmail.com',
    packages=['assist', 'assist.migrations'],
    url='http://bitbucket.org/kmike/django-assist-ru/',
    download_url = 'http://bitbucket.org/kmike/django-assist-ru/get/tip.zip',
    license='MIT license',
    description=u'Приложение для интеграции платежной системы ASSIST в проекты на Django.',
    long_description=open('README.txt').read(),

    classifiers=(
        'Development Status :: Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Natural Language :: Russian',
    ),
)