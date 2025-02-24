from django import forms
from .models import Order


class AddOrderForm(forms.ModelForm):
    # status = forms.ModelChoiceField()

    class Meta:
        model = Order
        fields = ['client_name', 'client_phone', 'client_phone1', 'client_telegram', 'client_viber', 'client_whatsapp', 'device',
                       'time_demand', 'defect', 'device_password', 'device_exterior', 'initial_price',
                       'prepaid', 'notes',]

        widgets = {
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