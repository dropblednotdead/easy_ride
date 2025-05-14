from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.


class UserInformation(models.Model):
    id = models.BigAutoField(primary_key=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Аватар')
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_info', verbose_name='Пользователь')
    phone_num = models.CharField(max_length=20, verbose_name='Номер телефона')
    age = models.SmallIntegerField(verbose_name='Возраст')
    passport_series = models.SmallIntegerField(verbose_name='Серия паспорта')
    passport_num = models.IntegerField(verbose_name='Номер паспорта')
    surname = models.CharField(max_length=100, null=True, blank=True, verbose_name='Фамилия')
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Имя')
    patronymic = models.CharField(max_length=100, null=True, blank=True, verbose_name='Отчество')

    class Meta:
        managed = True
        db_table = 'user_information'
        verbose_name = 'Информация о пользователе'
        verbose_name_plural = 'Информация о пользователях'
        ordering = ['id']

    def __str__(self):
        return f'{self.surname} {self.name}'


class Reviews(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateTimeField(verbose_name='Дата', auto_now_add=True)
    message = models.TextField(verbose_name='Сообщение')
    client = models.ForeignKey('UserInformation', models.DO_NOTHING, blank=True, null=True, verbose_name='Клиент')
    is_published = models.BooleanField(blank=True, null=True, verbose_name='Опобликован')

    class Meta:
        managed = True
        db_table = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-id']

    def __str__(self):
        return f'{self.client} {self.date}'


class Rent(models.Model):
    id = models.BigAutoField(primary_key=True)
    create_date = models.DateTimeField(verbose_name='Дата начала аренды', auto_now_add=True)
    start_date = models.DateTimeField(verbose_name='Дата начала аренды')
    end_date = models.DateTimeField(verbose_name='Дата конца аренды')
    accepted = models.BooleanField(blank=True, null=True, verbose_name='Подтверждение')
    client = models.ForeignKey('UserInformation', models.DO_NOTHING, verbose_name='Клиент')
    car = models.ForeignKey('Cars', models.DO_NOTHING, blank=True, null=True, verbose_name='Автомобиль')

    class Meta:
        managed = True
        db_table = 'rent'
        verbose_name = 'Аренда'
        verbose_name_plural = 'Аренды'
        ordering = ['id']

    def save(self, *args, **kwargs):
        if not self.car.check_availability(self.start_date, self.end_date):
            raise ValidationError("Автомобиль уже забронирован на этот период")
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.client} {self.car}'


class Cars(models.Model):
    id = models.BigAutoField(primary_key=True)
    cost = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Стоимость', blank=True, null=True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True, verbose_name='Фото')
    transmission = models.CharField(max_length=30, verbose_name='Трансмиссия')
    horse_powers = models.SmallIntegerField(verbose_name='Лошадиных сил')
    engine_volume = models.DecimalField(max_digits=2, decimal_places=1, verbose_name='Объем двигателя')
    colour = models.CharField(verbose_name='Цвет', max_length=50)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    is_free = models.BooleanField(verbose_name='Свободен')
    license_plate = models.CharField(max_length=15, verbose_name='Номера')
    model = models.ForeignKey('CarModels', models.DO_NOTHING, blank=True, null=True, verbose_name='Модель')
    category = models.ForeignKey('Categories', models.DO_NOTHING, blank=True, null=True, verbose_name='Категория')

    class Meta:
        managed = True
        db_table = 'cars'
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
        ordering = ['id']

    def check_availability(self, start_date, end_date):
        """Проверяет, свободна ли машина в указанный период"""
        overlapping_rents = Rent.objects.filter(
            car=self,
            accepted=True,
            start_date__lt=end_date,
            end_date__gt=start_date
        ).exists()
        return not overlapping_rents

    def __str__(self):
        return f'{self.model} {self.license_plate}'


class Categories(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=15, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    sale_active = models.BooleanField(verbose_name='Действие скидки')
    sale = models.ForeignKey('Sales', models.DO_NOTHING, blank=True, null=True, verbose_name='Скидка')

    class Meta:
        managed = True
        db_table = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

    def __str__(self):
        return f'{self.name}'


class Sales(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name='Название', blank=True, null=True, max_length=50)
    description = models.TextField(verbose_name='Описание')
    sale_percent = models.SmallIntegerField(verbose_name='Процент скидки', blank=True, null=True)
    start_date = models.DateTimeField(verbose_name='Дата начала')
    end_date = models.DateTimeField(verbose_name='Дата конца')

    class Meta:
        managed = True
        db_table = 'sales'
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'
        ordering = ['id']

    def __str__(self):
        return f'{self.start_date} {self.sale_percent}'


class CarModels(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Название')
    mass = models.SmallIntegerField(verbose_name='Масса')
    drive = models.CharField(max_length=20, verbose_name='Привод')
    brand = models.ForeignKey('Brand', models.DO_NOTHING, blank=True, null=True, verbose_name='Марка')
    bodywork = models.ForeignKey('Bodywork', models.DO_NOTHING, blank=True, null=True, verbose_name='Кузов')

    class Meta:
        managed = True
        db_table = 'car_model'
        verbose_name = 'Модель авто'
        verbose_name_plural = 'Модели авто'
        ordering = ['id']

    def __str__(self):
        return f'{self.brand} {self.name}'


class Brand(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        managed = True
        db_table = 'brand'
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ['id']

    def __str__(self):
        return f'{self.name}'


class Bodywork(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=50, verbose_name='Тип')

    class Meta:
        managed = True
        db_table = 'bodywork'
        verbose_name = 'Кузов'
        verbose_name_plural = 'Кузовы'
        ordering = ['id']

    def __str__(self):
        return f'{self.type}'