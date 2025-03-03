from django import forms
from .models import Order


class AddOrderForm(forms.ModelForm):
    new_client_name = forms.CharField(required=False, label='Добавить имя клиента')
    new_client_phone = forms.CharField(required=False, label='Добавить телефон клиента')


    class Meta:
        model = Order
        fields = ['order_client', 'device','time_demand', 'defect', 'device_password',
                  'device_exterior', 'initial_price', 'prepaid', 'notes',]

        widgets = {'order_client': forms.Select(),
                    'defect': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
                    'device_exterior': forms.Textarea(attrs={'cols': 40, 'rows': 1}),
                    'notes': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
                    'time_demand': forms.DateInput(
                         format=('%d/%m/%Y'),
                        attrs={'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                      }),
                    }

# class UploadFileForm(forms.Form):
#     file = forms.ImageField(label="Логотип компании", required=False)