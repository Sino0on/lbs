# Generated by Django 4.2.2 on 2023-07-06 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_driver_documents_alter_driver_driver_license_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='documents',
            field=models.ManyToManyField(blank=True, null=True, to='app.deliverydocs', verbose_name='Документы доставки'),
        ),
    ]
