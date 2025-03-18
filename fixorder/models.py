from django.db import models
from django.db.models.functions import NullIf
from django.urls import reverse
from django.utils import timezone


class OrderStatus(models.Model):
    status = models.CharField(max_length=100, unique=True, db_index=True, verbose_name='Статус заказа')

    def __str__(self):
        return self.status

class Client(models.Model):

    name = models.CharField(max_length=255, unique=True, db_index=True, verbose_name='ФИО клиента')
    phone = models.CharField(max_length=20, db_index=True, verbose_name='Контактный номер')
    phone1 = models.CharField(max_length=20, db_index=True, blank=True, null=True, verbose_name='Дополнительный номер')
    telegram = models.CharField(max_length=40, blank=True, null=True, verbose_name='Telegram клиента')
    viber = models.CharField(max_length=20, blank=True, null=True, verbose_name='Viber клиента')
    whatsapp = models.CharField(max_length=20, blank=True, null=True, verbose_name='Whattsapp клиента')

    def __str__(self):
        return f'{self.name} {self.phone} {self.phone1}'


class Order(models.Model):
    order_client = models.ForeignKey(Client, related_name='client', default=1, on_delete=models.DO_NOTHING, verbose_name='Клиент')
   #  order_client = models.CharField(max_length=255,blank=True, null=True, verbose_name='Срок')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
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
    work = models.CharField(max_length=255, blank=True, null=True, verbose_name='Выполненная работа')
    work_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Цена')
    work_warranty = models.FloatField(max_length=2, blank=True, null=True, verbose_name='Выполненная работа')
    work1 = models.CharField(max_length=255, blank=True, null=True, verbose_name='Выполненная работа')
    work_price1 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Цена')
    work_warranty1 = models.FloatField(max_length=2, blank=True, null=True, verbose_name='Гарантия')
    work2 = models.CharField(max_length=255, blank=True, null=True, verbose_name='Выполненная работа')
    work_price2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Цена')
    work_warranty2 = models.FloatField(max_length=2, blank=True, null=True, verbose_name='Гарантия')
    work3 = models.CharField(max_length=255, blank=True, null=True, verbose_name='Выполненная работа')
    work_price3 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Цена')
    work_warranty3 = models.FloatField(max_length=2, blank=True, null=True, verbose_name='Гарантия')
    work4 = models.CharField(max_length=255, blank=True, null=True, verbose_name='Выполненная работа')
    work_price4 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Цена')
    work_warranty4 = models.FloatField(max_length=2, blank=True, null=True, verbose_name='Гарантия')
    work5 = models.CharField(max_length=255, blank=True, null=True, verbose_name='Выполненная работа')
    work_price5 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Цена')
    work_warranty5 = models.FloatField(max_length=2, blank=True, null=True, verbose_name='Гарантия')
    work6 = models.CharField(max_length=255, blank=True, null=True, verbose_name='Выполненная работа')
    work_price6 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Цена')
    work_warranty6 = models.FloatField(max_length=2, blank=True, null=True, verbose_name='Гарантия')
    status = models.ForeignKey(OrderStatus, on_delete=models.DO_NOTHING, default = 4, related_name='related_order', verbose_name='Статус ремонта')
    conclusion = models.TextField(max_length=500, blank=True, null=True, verbose_name='Заключение мастера')
    remain_to_pay = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0,
                                      verbose_name='Осталось оплатить')

    def save(self, *args, **kwargs):
        old_order = None
        old_order = Order.objects.filter(pk=self.pk).last()
        print(old_order)
        if old_order and old_order.status.status != self.status.status:
            if self.status.status in ["Выдан", "Выдан без ремонта"]:
                self.time_away = timezone.now()
            else:
                self.time_away = None

        self.total_price = (
                (self.work_price or 0) + (self.work_price1 or 0) + (self.work_price2 or 0) + (self.work_price3 or 0) + (
                    self.work_price4 or 0) + (self.work_price5 or 0) + (self.work_price6 or 0))
        self.remain_to_pay = (self.total_price or 0) - (self.prepaid or 0)
        super(Order, self).save(*args, **kwargs)

    def save_time(self):
        old_order = None
        old_order = Order.objects.get(pk=self.pk)
        if old_order and old_order.status.status != self.status.status:
            if self.status.status in ["Выдан", "Выдан без ремонта"]:
                self.time_away = timezone.now()
            else:
                self.time_away = None


    def __str__(self):
        return f'{self.order_client__name} {self.device}'

    class Meta:
        verbose_name = 'Заказы'
        verbose_name_plural = 'Заказы'
        ordering = ['-time_create']
        indexes = [models.Index(fields=['-time_create'])
                   ]

    def get_absolute_url(self):
        return reverse('order', kwargs={'pk': self.pk})

    def get_warrantydoc_url(self):
        return reverse('warrantydoc', kwargs={'pk': self.pk})

    def get_commingdoc_url(self):
        return reverse('commingdoc', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('delete', kwargs={'pk': self.pk})

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







