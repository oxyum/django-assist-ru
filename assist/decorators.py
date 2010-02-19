#coding: utf-8
from functools import wraps
from django.utils.encoding import force_unicode

UTF8_HEADER = "text/html; charset=UTF-8"
CP1251_HEADER = "text/html; charset=windows-1251"

def cp1251(func):
    @wraps(func)
    def view(*args, **kwargs):
        response = func(*args, **kwargs)
        if response.status_code == 200 and 'text/html' in response['Content-Type']:
            response['Content-Type'] = CP1251_HEADER
            response.content = force_unicode(response.content).encode('1251')
            response.content = response.content.replace(UTF8_HEADER, CP1251_HEADER, 1)
        return response
    return view
