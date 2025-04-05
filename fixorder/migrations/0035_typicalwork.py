# Generated by Django 5.1.5 on 2025-04-03 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fixorder', '0034_work_remove_order_work_remove_order_work1_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypicalWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255, verbose_name='Ваши работы')),
            ],
            options={
                'ordering': ['description'],
            },
        ),
    ]
