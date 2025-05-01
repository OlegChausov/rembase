from django.db import models
from django.db.models import Sum
from django.db.models.functions import NullIf
from django.urls import reverse
from django.utils import timezone
from datetime import date


class OrderStatus(models.Model):
    status = models.CharField(max_length=100, unique=True, db_index=True, verbose_name='Статус заказа')

    def __str__(self):
        return self.status

class Client(models.Model):

    name = models.CharField(max_length=255, unique=True, db_index=True, verbose_name='ФИО клиента') #unique=True,
    phone = models.CharField(max_length=20, db_index=True, verbose_name='Контактный номер')
    phone1 = models.CharField(max_length=20, db_index=True, blank=True, null=True, verbose_name='Дополнительный номер')
    telegram = models.CharField(max_length=40, blank=True, null=True, verbose_name='Telegram клиента')
    viber = models.CharField(max_length=20, blank=True, null=True, verbose_name='Viber клиента')
    whatsapp = models.CharField(max_length=20, blank=True, null=True, verbose_name='Whattsapp клиента')

    class Meta:
        verbose_name = 'Клиенты'
        verbose_name_plural = 'Клиенты'
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]

    def get_absolute_url(self):
        return reverse('editclient', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.name} {self.phone} {self.phone1}'

class Company(models.Model):
    brand_name = models.CharField(max_length=255, unique=True, db_index=True, verbose_name='Название компании')
    official_name = models.CharField(max_length=255, blank=True, null=True, unique=True, db_index=True, verbose_name='Юридическое наименование')
    unp = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='УНП')
    phone = models.CharField(max_length=20, unique=True, verbose_name='Контактный номер')
    phone1 = models.CharField(max_length=20, blank=True, null=True, unique=True, verbose_name='Контактный номер')
    phone2 = models.CharField(max_length=20, blank=True, null=True, unique=True, verbose_name='Контактный номер')
    telegram = models.CharField(max_length=40, blank=True, null=True, verbose_name='Telegram')
    viber = models.CharField(max_length=20, blank=True, null=True, verbose_name='Viber')
    whatsapp = models.CharField(max_length=20, blank=True, null=True, verbose_name='Whattsapp')
    email = models.EmailField(max_length=50, blank=True, null=True, verbose_name='Электронная почта')
    adress = models.CharField(max_length=255, blank=True, null=True, unique=True, db_index=True, verbose_name='Адрес')
    postal_adress = models.CharField(max_length=255, blank=True, null=True, unique=True, verbose_name='Почтовый адрес')
    official_adress = models.CharField(max_length=255, blank=True, null=True, unique=True, verbose_name='Юридический адрес')
    photo = models.ImageField(upload_to="static/img/", blank=True, null=True, verbose_name="Логотип компании")

    def __str__(self):
        return f'{self.brand_name}'

    def save(self, *args, **kwargs):
        try:
            old_instance = Company.objects.get(pk=self.pk)
            if old_instance.photo and self.photo != old_instance.photo:
                old_instance.photo.delete(save=False)
        except Company.DoesNotExist:
            pass

        self.photo.name = 'logo.png'
        super(Company, self).save(*args, **kwargs)

class Employee(models.Model):
    STATUS_CHOICES = [
        ('1', 'Работает'),
        ('2', 'Отсутствует'),
        ('3', 'Не работает'),]

    company = models.ForeignKey(Company, related_name='employees', default = 1, on_delete=models.CASCADE, verbose_name='Компания')
    name = models.CharField(max_length=255, verbose_name='Имя сотрудника')
    position = models.CharField(max_length=100, verbose_name='Должность')
    time_hire = models.DateField(default=date.today, verbose_name='Дата начала работы')
    time_fire = models.DateField(null=True, blank=True, verbose_name='Дата окончания работы')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='1',
        verbose_name='Статус')

    def __str__(self):
        return f'{self.name} ({self.position})'

    def save(self, *args, **kwargs):
        if self.status == '3':  # Если статус "Не работает"
            self.time_fire = timezone.now()  # Устанавливаем текущую дату
        else:
            self.time_fire = None  # Сбрасываем дату, если статус изменился на другой
        super().save(*args, **kwargs)  # Вызываем родительский метод save()


class Order(models.Model):
    order_client = models.ForeignKey(Client, related_name='client', null=True, on_delete=models.SET_NULL, verbose_name='Клиент')
    executor = models.ForeignKey(Employee, blank=True, null=True, related_name='executor', on_delete=models.SET_NULL, verbose_name='Исполнитель')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата прихода')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    time_demand = models.DateField(blank=True, null=True, verbose_name='Срок ремонта')
    time_away = models.DateTimeField(null=True, blank=True, verbose_name='Дата выдачи')
    device = models.CharField(max_length=255, verbose_name='Устройство')
    defect = models.TextField(max_length=400, verbose_name='Неисправность')
    device_password = models.CharField(max_length=50, blank=True, null=True, verbose_name='Пароль')
    device_exterior = models.TextField(max_length=400, blank=True, null=True, verbose_name='Внешний вид')
    initial_price = models.CharField(max_length=10, blank=True, null=True, verbose_name='Ориентировочная стоимость')
    prepaid = models.FloatField(max_length=10, blank=True, null=True, verbose_name='Предоплата')
    notes = models.TextField(max_length=500, blank=True, null=True, verbose_name='Заметки')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0, verbose_name='Итоговая стоимость')
    status = models.ForeignKey(OrderStatus, on_delete=models.DO_NOTHING, default=4, related_name='related_order', verbose_name='Статус ремонта')
    conclusion = models.TextField(max_length=500, blank=True, null=True, verbose_name='Заключение мастера')
    remain_to_pay = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0, verbose_name='Осталось оплатить')



    def save(self, *args, **kwargs):
        if self.status_id and not self.pk:
            super().save(*args, **kwargs)

        old_order = None
        if self.pk:
            old_order = Order.objects.filter(pk=self.pk).last()
            if old_order and old_order.status_id != self.status_id:
                if self.status.status in ["Выдан", "Выдан без ремонта"]:
                    self.time_away = timezone.now()
                else:
                    self.time_away = None
        super().save(*args, **kwargs)

    def calculate_price(self):
        self.total_price = self.works.aggregate(total_price=Sum("price"))["total_price"] or 0
        self.remain_to_pay = self.total_price - (self.prepaid or 0)
        self.save() # Сохраняем объект Order после пересчета цен

    def __str__(self):
        return f"{self.order_client.name} — {self.device}"

    class Meta:
        verbose_name = "Заказы"
        verbose_name_plural = "Заказы"
        ordering = ["-time_create"]
        indexes = [models.Index(fields=["-time_create"]), models.Index(fields=["status"])]

    def get_absolute_url(self):
        return reverse('order', kwargs={'pk': self.pk})

    def get_warrantydoc_url(self):
        return reverse('warrantydoc', kwargs={'pk': self.pk})

    def get_commingdoc_url(self):
        return reverse('commingdoc', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('delete', kwargs={'pk': self.pk})


class Work(models.Model):
    order = models.ForeignKey(Order, related_name='works', on_delete=models.CASCADE, verbose_name='Заказ')
    description = models.CharField(max_length=255, verbose_name='Описание работы')
    price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name='Цена')
    warranty = models.CharField(blank=True, null=True, max_length=20, verbose_name='Гарантия')


    def __str__(self):
        return f"{self.description} - {self.price} Руб"

class TypicalWork(models.Model):
    description = models.CharField(max_length=255, verbose_name='Вид работы')

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f"{self.description}"




















