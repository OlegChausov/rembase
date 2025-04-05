from dal import autocomplete
from django import forms
from django.utils import timezone

from .models import Order, Client, Employee, Work, TypicalWork


class AddClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name','phone','phone1',]

class WorkForm(forms.ModelForm):
    description = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "form-control work-select"}), label="")

    price = forms.DecimalField(
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Введите цену"}),
        label="")

    def clean_price(self):
        price = self.cleaned_data.get("price")
        return price if price is not None else 0  # Если пустое, заменяем на 0

    warranty = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Гарантия"}),
        label=""
    )

    def clean_warranty(self):
        warranty = self.cleaned_data.get("warranty")
        return None if not warranty.strip() else warranty # Если пустое, заменяем на ""

    class Meta:
        model = Work
        fields = ["description", "price", "warranty"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].choices = [('', 'Выбор услуги')] + [
            (typical_work.description, typical_work.description) for typical_work in TypicalWork.objects.all()
        ]





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
        fields = ['client', 'executor', 'name', 'phone', 'phone1', 'telegram', 'viber', 'whatsapp', 'device', 'time_demand', 'defect', 'device_password',
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
        self.fields['executor'].choices = [('', 'Не выбран')] + [(employee.id, str(employee)) for employee in Employee.objects.filter(status='1')]
        self.fields['client'].choices = [(client.id, f"{client.name} ({client.phone})") if client.phone else (client.id, f"{client.name}") for client in Client.objects.all()]

class AddEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'position', 'status', ]
        widgets = {
            'time_fire': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }