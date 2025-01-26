from django import forms
from .models import Order


class AddOrderForm(forms.ModelForm):
    # status = forms.ModelChoiceField()

    class Meta:
        model = Order
        fields = ['client_name', 'client_phone', 'client_telegram', 'client_viber', 'client_whatsapp', 'device',
                       'time_demand', 'defect', 'device_password', 'device_exterior', 'initial_price',
                       'prepaid', 'notes',]





# class AddPostForm(forms.ModelForm):
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категории")#эти поля нужны, чтобы указать параметр значения по умолчанию в форме
#     husband = forms.ModelChoiceField(queryset=Husband.objects.all(), empty_label="Не замужем", required=False,label="Муж")#эти поля нужны, чтобы указать параметр значения по умолчанию в форме
#
#     class Meta:
#         model = Women
#         #fields = '__all__' #в форме появятся все поля модели, заполняемых автоматический, заголовок поля формы будет verbouse_name модели
#         fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'husband', 'tags']#лучше указать явно
#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-input'}),
#             'content': forms.Textarea(attrs={'cols': 50, 'rows': 5})}#виджеты с параметрами стилей
#         labels = {'slug': 'URL'}#переопределим заголовок с verbouse_name на свой
#
#     def clean_title(self): #все методы с ключевым словом cleaned вызываются автоматически при созадния экземпляра класса формы
#         title = self.cleaned_data['title']
#         if len(title) > 50:
#             raise ValidationError('Длина превышает 50 символов')
#
#         return title