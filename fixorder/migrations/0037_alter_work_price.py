# Generated by Django 5.1.5 on 2025-04-05 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fixorder', '0036_alter_work_warranty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, verbose_name='Цена'),
        ),
    ]
