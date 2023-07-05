from django.db import models
from django.contrib.auth.models import AbstractUser


statuses = [
    ("NICE", "Nice"),
    ("BAD", "Bad"),
]
car_types = [
    ("BIG", "Big"),
    ("SMALL", "Small"),
]
usertypes = [
    ("ADMIN", "Admin"),
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
    documents = models.ManyToManyField('DeliveryDocs', verbose_name="Документы доставки")
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
    orders = models.IntegerField(verbose_name="Количество заказов")
    status = models.CharField(max_length=255, choices=statuses, verbose_name="Статус")
    documents = models.ManyToManyField('DriverDocument', verbose_name="Документы водителя")
    driver_license = models.FileField(verbose_name="Водительские права", upload_to='files/drivers/')
    qualification = models.FileField(verbose_name="Квалификация", upload_to='files/drivers/')
    medical_sertificate = models.FileField(verbose_name="Медицинское свидетельство", upload_to='files/drivers/')
    employeement = models.FileField(verbose_name="Трудоустройство", upload_to='files/drivers/')
    recomment = models.FileField(verbose_name="Рекомендация", upload_to='files/drivers/')

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = "Водитель"
        verbose_name_plural = "Водители"


class Price(models.Model):
    title = models.IntegerField(verbose_name="Цена")

    def __str__(self):
        return str(self.title)

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
    type_order = models.CharField(max_length=255, verbose_name="Тип заказа")
    distance = models.FloatField(verbose_name="Расстояние")
    price = models.OneToOneField(verbose_name="Цена", to=Price, on_delete=models.PROTECT)
    type_car = models.CharField(max_length=255, choices=car_types, verbose_name="Тип автомобиля")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    status = models.CharField(max_length=255, choices=statuses, verbose_name="Статус")

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
