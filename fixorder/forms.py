from dal import autocomplete
from django import forms
from .models import Order,Client

class AddClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name','phone','phone1',]


class AddOrderForm(forms.ModelForm):

    client = forms.ChoiceField(
        choices=[],
        required=False,
        label='Выберите клиента',
        widget=forms.Select(attrs={'class': 'js-example-basic-single',  'id': 'client-select'}),
        initial='1',
    )

    new_client_name = forms.CharField(required=False, label='Добавить имя клиента', widget=forms.TextInput(attrs={'id': 'new-client-name'})
    )
    new_client_phone = forms.CharField(required=False, label='Добавить телефон клиента', widget=forms.TextInput(attrs={'id': 'new-client-phone'})
    )

    class Meta:
        model = Order
        fields = ['client', 'new_client_name', 'new_client_phone', 'device','time_demand', 'defect', 'device_password',
                  'device_exterior', 'initial_price', 'prepaid', 'notes',]

        widgets = {'order_client': forms.Select(attrs={'class': 'js-example-basic-single'}),
                    'defect': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
                    'device_exterior': forms.Textarea(attrs={'cols': 40, 'rows': 1}),
                    'notes': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
                    'time_demand': forms.DateInput(
                         format=('%d/%m/%Y'),
                        attrs={'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                      }),
                    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Динамическое заполнение списка клиентов
        self.fields['client'].choices = [(client.id, f"{client.name} ({client.phone})") for client in Client.objects.all()]

