from dal import autocomplete
from django import forms
from django.utils import timezone

from .models import Order,Client

class AddClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name','phone','phone1',]


class AddOrderForm(forms.ModelForm):
    #при создании формы поля 'client', 'name', 'phone', 'phone1', 'telegram', 'viber', 'whatsapp' создаются
    #на лету (их нет в модели).

    #Это свойство мы указали здесь и дополнительно переопределили в
    client = forms.ChoiceField(
        choices=[],
        required=False,
        label='Выберите клиента',
        widget=forms.Select(attrs={'class': 'js-example-basic-single', 'id': 'client-select'}),
        initial='1',  # Устанавливаем значение по умолчанию
    )

    name = forms.CharField(
        required=False,
        label='Имя клиента',
        widget=forms.TextInput(attrs={'id': 'client-name'})
    )
    phone = forms.CharField(
        required=False,
        label='Телефон клиента',
        widget=forms.TextInput(attrs={'id': 'client-phone'})
    )

    phone1 = forms.CharField(
        required=False,
        label='Дополнительный телефон',
        widget=forms.TextInput(attrs={'id': 'client-phone1'})
    )
    telegram = forms.CharField(
        required=False,
        label='Telegram',
        widget=forms.TextInput(attrs={'id': 'client-telegram'})
    )
    viber = forms.CharField(
        required=False,
        label='Viber',
        widget=forms.TextInput(attrs={'id': 'client-viber'})
    )
    whatsapp = forms.CharField(
        required=False,
        label='WhatsApp',
        widget=forms.TextInput(attrs={'id': 'client-whatsapp'})
    )

    class Meta:
        model = Order
        fields = ['client', 'name', 'phone', 'phone1', 'telegram', 'viber', 'whatsapp', 'device', 'time_demand', 'defect', 'device_password',
                  'device_exterior', 'initial_price', 'prepaid', 'notes']
#так как связано с моделью, в fields указываем поля модели и наши виртуально созданные при ините поля 'client', 'name', 'phone', 'phone1', 'telegram', 'viber', 'whatsapp',
        widgets = {
            'order_client': forms.Select(attrs={'class': 'js-example-basic-single'}),
            'defect': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
            'device_exterior': forms.Textarea(attrs={'cols': 40, 'rows': 1}),
            'notes': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
            'time_demand': forms.DateInput(
                format=('%d/%m/%Y'),
                attrs={
                    'type': 'date',
                    'value': timezone.now().strftime('%Y-%m-%d'),  # Устанавливаем значение по умолчанию
                }
            ),
        }
#заполняем наши на лету созданное поле client данными за БД Client.objects...
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].choices = [(client.id, f"{client.name} ({client.phone})") for client in Client.objects.all()]
