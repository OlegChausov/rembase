# Generated by Django 5.1.5 on 2025-03-03 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fixorder', '0019_alter_company_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, unique=True, verbose_name='ФИО клиента')),
                ('phone', models.CharField(db_index=True, max_length=20, verbose_name='Контактный номер')),
                ('phone1', models.CharField(blank=True, db_index=True, max_length=20, verbose_name='Дополнительный номер')),
                ('telegram', models.CharField(blank=True, max_length=40, null=True, verbose_name='Telegram клиента')),
                ('viber', models.CharField(blank=True, max_length=20, null=True, verbose_name='Viber клиента')),
                ('whatsapp', models.CharField(blank=True, max_length=20, null=True, verbose_name='Whattsapp клиента')),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='client_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='client_phone',
        ),
        migrations.RemoveField(
            model_name='order',
            name='client_phone1',
        ),
        migrations.RemoveField(
            model_name='order',
            name='client_telegram',
        ),
        migrations.RemoveField(
            model_name='order',
            name='client_viber',
        ),
        migrations.RemoveField(
            model_name='order',
            name='client_whatsapp',
        ),
        migrations.AddField(
            model_name='order',
            name='order_client',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Срок'),
        ),
    ]
