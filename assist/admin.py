#coding: utf-8
from django.contrib import admin
from assist.models import AssistAuthResult

class AssistAuthResultAdmin(admin.ModelAdmin):
    pass
#    list_display=['created_at', 'ORDERID', 'REFERENCE_NO', 'NAME', 'TOTAL', "CURRENCY", 'is_md5_correct', 'is_purchase_valid']
#    list_filter = ['is_purchase_valid', 'is_md5_correct', 'RESPONSE_CODE', 'PAYED_BY', 'CURRENCY', 'TEST_MODE']
#    date_hierarchy = 'created_at'
#    search_fields = ['ORDERID', 'REFERENCE_NO']
#    search_fields_verbose = [u'ID заказа', u'ID транзакции']

admin.site.register(AssistAuthResult, AssistAuthResultAdmin)