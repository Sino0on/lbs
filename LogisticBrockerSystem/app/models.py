from django.db import models
from django.contrib.auth.models import AbstractUser
import requests


statuses = [
    ("NICE", "Nice"),
    ("BAD", "Bad"),
]
car_types = [
    ("BIG", "Big"),
    ("SMALL", "Small"),
]
usertypes = [
    ("SENDER", "Sender"),
    ("DRIVER", "Driver"),
    ("COMPANY", "Company"),
]


class DeliveryDocs(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    document = models.FileField(verbose_name="Документ", upload_to='files/delivery/')
    created_date = models.DateField(verbose_name="Дата создания")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Документ доставки"
        verbose_name_plural = "Документы доставки"


class Delivery(models.Model):
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE, verbose_name="Водитель")
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="Пользователь")
    order = models.OneToOneField('Order', on_delete=models.SET_NULL, verbose_name="Заказ", null=True)
    documents = models.ManyToManyField('DeliveryDocs', verbose_name="Документы доставки", blank=True, null=True)
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    status = models.CharField(max_length=255, choices=statuses, verbose_name="Статус")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Доставка"
        verbose_name_plural = "Доставки"


class Driver(models.Model):
    user = models.OneToOneField('User', on_delete=models.SET_NULL, related_name='is_driver', null=True)
    orders = models.IntegerField(verbose_name="Количество заказов", blank=True, null=True)
    status = models.CharField(max_length=255, choices=statuses, verbose_name="Статус", blank=True, null=True)
    documents = models.ManyToManyField('DriverDocument', verbose_name="Документы водителя", blank=True, null=True)
    driver_license = models.FileField(verbose_name="Водительские права", upload_to='files/drivers/', blank=True, null=True)
    qualification = models.FileField(verbose_name="Квалификация", upload_to='files/drivers/', blank=True, null=True)
    medical_sertificate = models.FileField(verbose_name="Медицинское свидетельство", upload_to='files/drivers/', blank=True, null=True)
    employeement = models.FileField(verbose_name="Трудоустройство", upload_to='files/drivers/', blank=True, null=True)
    recomment = models.FileField(verbose_name="Рекомендация", upload_to='files/drivers/', blank=True, null=True)

    def __str__(self):
        return f'Водитель {self.pk}'

    class Meta:
        verbose_name = "Водитель"
        verbose_name_plural = "Водители"


class Price(models.Model):
    km = models.IntegerField(verbose_name="Цена за км")
    insurance = models.IntegerField(verbose_name='Страховка')
    express = models.IntegerField(verbose_name='Срочность')

    def __str__(self):
        return f'цены'

    class Meta:
        verbose_name = "Цена"
        verbose_name_plural = "Цены"


class DriverDocument(models.Model):
    document = models.FileField(verbose_name="Документ")

    def __str__(self):
        return self.document.name

    class Meta:
        verbose_name = "Документ водителя"
        verbose_name_plural = "Документы водителя"


class Order(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="Пользователь")
    description = models.TextField(verbose_name="Описание")
    start_date = models.DateField(verbose_name="Дата начала")
    start_time = models.TimeField(verbose_name="Время начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    end_time = models.TimeField(verbose_name="Время окончания")
    weight = models.FloatField(verbose_name="Вес")
    size = models.FloatField(verbose_name="Размер")
    comment = models.TextField(verbose_name="Комментарий")
    start_place = models.CharField(max_length=255, verbose_name="Место отправления")
    end_place = models.CharField(max_length=255, verbose_name="Место доставки")
    express = models.BooleanField(verbose_name="Срочный", default=False, blank=True)
    distance = models.FloatField(verbose_name="Расстояние", blank=True, null=True)
    price = models.OneToOneField(verbose_name="Цена", to=Price, on_delete=models.PROTECT, blank=True, null=True)
    type_car = models.CharField(max_length=255, choices=car_types, verbose_name="Тип автомобиля")
    insurance = models.BooleanField(verbose_name="Страховка", default=False, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    status = models.CharField(max_length=255, choices=statuses, verbose_name="Статус", blank=True)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        data = requests.get(str(self.start_place))
        map = data.url.split('@')[1].split(',')[:2]
        self.start_place = ''.join(map)
        data = requests.get(str(self.end_place))
        map = data.url.split('@')[1].split(',')[:2]
        self.end_place = ''.join(map)
        return super().save()


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class User(AbstractUser):
    grade = models.IntegerField(verbose_name="Оценка", blank=True, null=True)
    birth_of_date = models.DateField(verbose_name="Дата рождения", blank=True, null=True)
    status = models.CharField(max_length=255, choices=statuses, verbose_name="Статус", blank=True, null=True)
    type_user = models.CharField(max_length=255, choices=usertypes, verbose_name="Тип пользователя", blank=True, null=True)
    phone_number = models.CharField(max_length=255, verbose_name="Номер телефона", blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Feedback(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="Пользователь")
    grade = models.IntegerField(verbose_name="Оценка")
    content = models.TextField(verbose_name="Содержание")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    image = models.ManyToManyField('FeedbackImage', verbose_name="Изображение")
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name="Водитель")

    def __str__(self):
        return f"{self.user} - {self.created_date}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Company(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    drivers = models.ManyToManyField(Driver, verbose_name="Водители")
    descriptions = models.TextField(verbose_name="Описание")
    status = models.CharField(max_length=255, choices=statuses, verbose_name="Статус")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"


class Message(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="Пользователь")
    text = models.TextField(verbose_name="Текст")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, verbose_name="Чат")
    documents = models.ManyToManyField('MessageDoc', verbose_name="Документы сообщения")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class MessageDoc(models.Model):
    documet = models.FileField(verbose_name="Документ")

    def __str__(self):
        return self.documet.name

    class Meta:
        verbose_name = "Документ сообщения"
        verbose_name_plural = "Документы сообщения"


class CompanyFeedback(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    grade = models.IntegerField(verbose_name="Оценка")
    content = models.TextField(verbose_name="Содержание")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    images = models.ManyToManyField('FeedbackImage', verbose_name="Изображения")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Компания")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Отзыв о компании"
        verbose_name_plural = "Отзывы о компаниях"


class FeedbackImage(models.Model):
    image = models.ImageField(upload_to='media/feedback/', verbose_name="Изображение")

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = "Изображение отзыва"
        verbose_name_plural = "Изображения отзывов"


class Chat(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="Пользователь")
    order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name="Заказ")
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE, verbose_name="Водитель")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    status = models.CharField(max_length=255, choices=statuses, verbose_name="Статус")

    def __str__(self):
        return f"Чат {self.pk}"

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"


class PriceSingle(models.Model):
    km = models.IntegerField(verbose_name="Цена за км")
    insurance = models.IntegerField(verbose_name='Страховка')
    express = models.IntegerField(verbose_name='Срочность')
