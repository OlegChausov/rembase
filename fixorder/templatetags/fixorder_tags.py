from django import template
from django.templatetags.static import static

from fixorder.models import Company

register = template.Library()

@register.simple_tag
def logo_url():
    return static('img/logo.png')

@register.simple_tag
def get_company_name():
    return Company.objects.get(pk=1).brand_name


@register.simple_tag
def filled_fields_verbose(pk):
    instance = Company.objects.get(pk=pk)
    field_dict = {}
    for field in instance._meta.fields:
        if field.name not in ['id', 'photo', 'warranty_data', 'income_data']:  # Исключаем поля которые не нужно отображать в доках
            value = getattr(instance, field.name)
            if value:
                field_dict[field.verbose_name] = value
    return field_dict



