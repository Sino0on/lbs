# Generated by Django 4.2.2 on 2023-07-06 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='documents',
            field=models.ManyToManyField(blank=True, null=True, to='app.driverdocument', verbose_name='Документы водителя'),
        ),
        migrations.AlterField(
            model_name='driver',
            name='driver_license',
            field=models.FileField(blank=True, null=True, upload_to='files/drivers/', verbose_name='Водительские права'),
        ),
        migrations.AlterField(
            model_name='driver',
            name='employeement',
            field=models.FileField(blank=True, null=True, upload_to='files/drivers/', verbose_name='Трудоустройство'),
        ),
        migrations.AlterField(
            model_name='driver',
            name='medical_sertificate',
            field=models.FileField(blank=True, null=True, upload_to='files/drivers/', verbose_name='Медицинское свидетельство'),
        ),
        migrations.AlterField(
            model_name='driver',
            name='orders',
            field=models.IntegerField(blank=True, null=True, verbose_name='Количество заказов'),
        ),
        migrations.AlterField(
            model_name='driver',
            name='qualification',
            field=models.FileField(blank=True, null=True, upload_to='files/drivers/', verbose_name='Квалификация'),
        ),
        migrations.AlterField(
            model_name='driver',
            name='recomment',
            field=models.FileField(blank=True, null=True, upload_to='files/drivers/', verbose_name='Рекомендация'),
        ),
        migrations.AlterField(
            model_name='driver',
            name='status',
            field=models.CharField(blank=True, choices=[('NICE', 'Nice'), ('BAD', 'Bad')], max_length=255, null=True, verbose_name='Статус'),
        ),
    ]