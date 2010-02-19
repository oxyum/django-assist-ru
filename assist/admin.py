#coding: utf-8
from django.contrib import admin
from assist.models import AssistAuthResult

class AssistAuthResultAdmin(admin.ModelAdmin):
    list_display = ['BillNumber', 'OrderNumber', 'Date', 'Total', 'Status',
                    'Response_Code', 'Recommendation', 'PatmentType']
    list_filter = ['Status', 'Response_Code']
    date_hierarchy = 'Date'
    search_fields = ['OrderNumber', 'BillNumber']
    search_fields_verbose = [u'Номер заказа', u'Номер платежа']

admin.site.register(AssistAuthResult, AssistAuthResultAdmin)