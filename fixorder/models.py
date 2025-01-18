from django.db import models
from django.urls import reverse


class Order(models.Model):
    class Statuses(models.TextChoices):
        ACTIVE = ('AC', "Активен")
        READY = ("RD", "Готов")
        AWAY = ("AW", "Выдан ")
        NOTPAID = ("NP", "Выдан без оплаты")
        WARRANTY = ("WR", "Гарантийный")

    client_name = models.CharField(max_length=255, unique=True, db_index=True, verbose_name='ФИО клиента')
    client_phone = models.CharField(max_length=20, db_index=True, verbose_name='Контактный номер')
    client_telegram = models.CharField(max_length=40, blank=True, null=True, verbose_name='Telegram клиента')
    client_viber = models.CharField(max_length=20, blank=True, null=True, verbose_name='Viber клиента')
    client_whatsapp = models.CharField(max_length=20, blank=True, null=True, verbose_name='Whattsapp клиента')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    time_demand = models.DateField(blank=True, null=True, verbose_name='Срок ремонта')
    device = models.CharField(max_length=255, verbose_name='Устройство')
    defect = models.TextField(max_length=400, verbose_name='Неисправность')
    device_password = models.CharField(max_length=50, blank=True, null=True, verbose_name='Пароль')
    device_exterior = models.TextField(max_length=400, blank=True, null=True, verbose_name='Внешний вид')
    initial_price = models.CharField(max_length=10, blank=True, null=True, verbose_name='Ориентировочная стоимость ремонта')
    prepaid = models.FloatField(max_length=10, blank=True, null=True, verbose_name='Предоплата')
    notes = models.TextField(max_length=500, blank=True, null=True, verbose_name='Заметки')
    status = models.CharField(max_length=2, choices=Statuses.choices, default=Statuses.ACTIVE, verbose_name='Статус ремонта')
    work = models.CharField(max_length=255, blank=True, null=True, verbose_name='Выполненная работа')
    work_price = models.FloatField(max_length=10, blank=True, null=True, verbose_name='Цена')
    work_warranty = models.FloatField(max_length=2, blank=True, null=True)
    work1 = models.CharField(max_length=255, blank=True, null=True, verbose_name='Выполненная работа')
    work_price1 = models.FloatField(max_length=10, blank=True, null=True, verbose_name='Цена')
    work_warranty1 = models.FloatField(max_length=2, blank=True, null=True, verbose_name='Гарантия')
    work2 = models.CharField(max_length=255, blank=True, null=True, verbose_name='Выполненная работа')
    work_price2 = models.FloatField(max_length=10, blank=True, null=True, verbose_name='Цена')
    work_warranty2 = models.FloatField(max_length=2, blank=True, null=True, verbose_name='Гарантия')
    work3 = models.CharField(max_length=255, blank=True, null=True, verbose_name='Выполненная работа')
    work_price3 = models.FloatField(max_length=10, blank=True, null=True, verbose_name='Цена')
    work_warranty3 = models.FloatField(max_length=2, blank=True, null=True, verbose_name='Гарантия')
    work4 = models.CharField(max_length=255, blank=True, null=True, verbose_name='Выполненная работа')
    work_price4 = models.FloatField(max_length=10, blank=True, null=True, verbose_name='Цена')
    work_warranty4 = models.FloatField(max_length=2, blank=True, null=True, verbose_name='Гарантия')
    work5 = models.CharField(max_length=255, blank=True, null=True, verbose_name='Выполненная работа')
    work_price5 = models.FloatField(max_length=10, blank=True, null=True, verbose_name='Цена')
    work_warranty5 = models.FloatField(max_length=2, blank=True, null=True, verbose_name='Гарантия')
    work6 = models.CharField(max_length=255, blank=True, null=True, verbose_name='Выполненная работа')
    work_price6 = models.FloatField(max_length=10, blank=True, null=True, verbose_name='Цена')
    work_warranty6 = models.FloatField(max_length=2, blank=True, null=True, verbose_name='Гарантия')

    # def get_total_price(self):
    #     return sum(self.work_price, self.work_price1)

    def __str__(self):
        return f'{self.client_name} {self.device}'


    class Meta:
        verbose_name = 'Заказы'
        verbose_name_plural = 'Заказы'
        ordering = ['-time_create']
        indexes = [models.Index(fields=['-time_create'])
                   ]


    def get_absolute_url(self):
        return reverse('order', kwargs={'pk': self.pk})
