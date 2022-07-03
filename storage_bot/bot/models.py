from django.db import models
from django.db.models.fields import DateTimeField, TimeField
from phonenumber_field.modelfields import PhoneNumberField


class User(models.Model):
    """Модель пользователя."""

    telegram_id = models.IntegerField(
        "ID пользователя в Telegram",
        null=True,
    )
    name = models.CharField(
        "Имя",
        max_length=50,
        blank=True,
    )
    surname = models.CharField(
        "Фамилия",
        max_length=50,
        blank=True,
        null=True,
    )
    email = models.EmailField(
        "Электронная почта",
        blank=True,
    )
    address = models.CharField(
        "Адрес",
        max_length=100,
        blank=True,
    )
    phone = PhoneNumberField(
        "Номер телефона",
        max_length=20,
        blank=True,
    )

    def __str__(self):
        return f"{self.name} {self.surname}"


class Storage(models.Model):
    """Модель скалада."""

    address = models.CharField(
        "Адрес",
        max_length=100,
    )
    work_time = models.CharField(
        "Режим работы",
        max_length=50,
    )

    def __str__(self):
        return f'Склад по адресу: {self.address}'


class Cell(models.Model):
    """Модель ячейки."""

    storage = models.ForeignKey(
        Storage,
        verbose_name='Склад',
        related_name='cells',
        on_delete=models.CASCADE
    )
    number = models.IntegerField(
        "Номер"
    )
    temperature = models.CharField(
        "Температура",
        max_length=20
    )
    height = models.FloatField(
        "Высота"
    )
    floor = models.IntegerField(
        "Этаж",
    )
    size = models.CharField(
        "Размер",
        max_length=100,
    )
    price = models.FloatField(
        "Цена",
    )
    booked = models.BooleanField(
        "Занято",
        default=False
    )
    lease_time = DateTimeField(
        "Дата окончания аренды",
        blank=True,
    )

    def __str__(self):
        return f'Ячейка №{self.id}, склад №{self.storage.id}'


class Order(models.Model):
    """Модель заказа."""

    create_date = models.DateTimeField(
        "Дата создания",
        null=True,
    )
    user = models.ForeignKey(
        User,
        verbose_name='Заказчик',
        related_name='orders',
        on_delete=models.CASCADE
    )
    cell = models.ForeignKey(
        Cell,
        verbose_name='Ячейка',
        related_name='orders',
        on_delete=models.CASCADE
    )
    measurer = models.BooleanField(
        "Нужен ли замерщик",
        default=False
    )
    comment = models.CharField(
        "Комментарий",
        max_length=100,
        blank=True
    )

    def __str__(self):
        return f"Заказ от: {self.user} по: {self.cell}"
