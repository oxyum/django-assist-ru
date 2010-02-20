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

    def actual_for_order(self, OrderNumber):
        """ Возвращает действующий результат авторизации для данного заказа.
            Просто последнюю транзакцию брать нельзя, см. причины в README.

            Игнорируются транзакции со статусом 'in progress', а также
            транзакции с 'негативными' статусами при наличии транзакций с
            соответствующими 'позитивными' статусами.
        """

        results = list(self.get_query_set().filter(OrderNumber = OrderNumber).order_by('-BillNumber'))

        to_remove = set(['in progress'])
        for bill in results:
            if bill.Status == 'Authorized': to_remove.add('Not authorized')
            if bill.Status == 'Preauthorized': to_remove.add('Not preauthorized')
            if bill.Status == 'Captured':   to_remove.add('Not captured')
            if bill.Status == 'Voided':     to_remove.add('Not Voided')
            if bill.Status == 'Refunded':   to_remove.add('Not Refunded')
            if bill.Status == 'Reversaled': to_remove.add('Not Reversaled')

        results = [b for b in results if b.Status not in to_remove]

        if not results:
            return None
        return results[0]