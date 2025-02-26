from django import template
from django.templatetags.static import static

from fixorder.models import Company

register = template.Library()

@register.simple_tag
def logo_url():
    return static('img/logo.png')

@register.simple_tag
def filled_fields_verbose(pk):
    instance = Company.objects.get(pk=pk)
    field_dict = {}
    for field in instance._meta.fields:
        if field.name not in ['id', 'photo']:  # Исключаем поля 'id' и 'photo'
            value = getattr(instance, field.name)
            if value:
                field_dict[field.verbose_name] = value
    return field_dict

