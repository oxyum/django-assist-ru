#coding: utf-8
from django.db import models
from assist.api import fetch_auth_report

class AssistAuthResultManager(models.Manager):

    def update_auth_report(self):
        """ Получает результаты авторизации платежей за последние 3 дня и
            создает/обновляет по ним нужные записи в БД (по одной записи на
            каждый BillNumber).
        """
        results = fetch_auth_report()
        for row in results:
            instance = self.model(**row)
            try:
                old_instance = self.get(BillNumber=instance.BillNumber)
                pk = old_instance.pk
            except self.model.DoesNotExist:
                pk = None
            instance.pk = pk
            instance.save()
        return results
