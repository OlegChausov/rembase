# Generated by Django 5.1.5 on 2025-04-22 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fixorder', '0035_typicalwork'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='warranty',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Гарантия'),
        ),
    ]
