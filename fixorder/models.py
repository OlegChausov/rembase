from django.db import models
from django.urls import reverse


class Order(models.Model):
    class Statuses(models.TextChoices):
        ACTIVE = ('AC', "Активен")
        READY = ("RD", "Готов")
        AWAY = ("AW", "Выдан ")
        NOTPAID = ("NP", "Выдан без оплаты")
        WARRANTY = ("WR", "Гарантийный")

    client_name = models.CharField(max_length=255, unique=True, db_index=True)
    client_phone = models.CharField(max_length=20, db_index=True)
    client_telegram = models.CharField(max_length=40, blank=True, db_index=True)
    client_viber = models.CharField(max_length=20, blank=True, db_index=True)
    client_whatsapp = models.CharField(max_length=20, blank=True, db_index=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    time_demand = models.DateField(blank=True)
    device = models.CharField(max_length=255)
    defect = models.TextField(max_length=400)
    device_password = models.CharField(max_length=50, blank=True)
    device_exterior = models.TextField(max_length=400, blank=True)
    initial_price = models.Field(max_length=10, blank=True)
    prepaid = models.Field(max_length=10, blank=True)
    notes = models.TextField(max_length=500, blank=True)
    status = models.CharField(max_length=2, choices=Statuses.choices, default=Statuses.ACTIVE)
    work = models.CharField(max_length=255, blank=True)
    work_price = models.FloatField(max_length=10, blank=True)
    work_warranty = models.FloatField(max_length=2, blank=True)
    work1 = models.CharField(max_length=255, blank=True)
    work_price1 = models.FloatField(max_length=10, blank=True)
    work_warranty1 = models.FloatField(max_length=2, blank=True)
    work2 = models.CharField(max_length=255, blank=True)
    work_price2 = models.FloatField(max_length=10, blank=True)
    work_warranty2 = models.FloatField(max_length=2, blank=True)
    work3 = models.CharField(max_length=255, blank=True)
    work_price3 = models.FloatField(max_length=10, blank=True)
    work_warranty3 = models.FloatField(max_length=2, blank=True)
    work4 = models.CharField(max_length=255, blank=True)
    work_price4 = models.FloatField(max_length=10, blank=True)
    work_warranty4 = models.FloatField(max_length=2, blank=True)
    work5 = models.CharField(max_length=255, blank=True)
    work_price5 = models.FloatField(max_length=10, blank=True)
    work_warranty5 = models.FloatField(max_length=2, blank=True)
    work6 = models.CharField(max_length=255, blank=True)
    work_price6 = models.FloatField(max_length=10, blank=True)
    work_warranty6 = models.FloatField(max_length=2, blank=True)

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
        return reverse('orderlist', kwargs={'order_id': self.pk})
