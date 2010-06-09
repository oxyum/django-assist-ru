#coding: utf-8
from django.contrib import admin
from django import forms
from assist.models import AssistAuthResult, AssistResultChange

class AssistResultChangeInline(admin.TabularInline):
    model = AssistResultChange
    extra = 0

class AssistResultChangeAdmin(admin.ModelAdmin):
    list_display=['auth_result', 'changed_at', 'changes']

class AssistAuthResultAdmin(admin.ModelAdmin):
    list_display = ['BillNumber', 'OrderNumber', 'Date', 'Total', 'Status',
                    'Response_Code', 'Recommendation', 'PatmentType']
    list_filter = ['Status', 'Response_Code']
    date_hierarchy = 'Date'
    search_fields = ['OrderNumber', 'BillNumber']
    search_fields_verbose = [u'Номер заказа', u'Номер платежа']
    inlines = [AssistResultChangeInline]

admin.site.register(AssistAuthResult, AssistAuthResultAdmin)
admin.site.register(AssistResultChange, AssistResultChangeAdmin)