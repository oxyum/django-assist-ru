#coding: utf-8
from django.db.models import fields

def get_changes_between_models(model1, model2, excludes = []):
    ''' Вернуть отличия между 2 моделями. Взято отсюда:
    http://www.indirecthit.com/2008/04/29/django-difference-between-two-model-instances/
    '''
    changes = {}
    for field in model1._meta.fields:
        if not (isinstance(field, (fields.AutoField, fields.related.RelatedField))
                or field.name in excludes):
            value1 = field.value_from_object(model1)
            value2 = field.value_from_object(model2)
            if unicode(value1) != unicode(value2):
                changes[field.verbose_name] = (value1, value2)
    return changes
