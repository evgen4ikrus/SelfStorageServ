from django.db import models
from django.db.models.fields import DateTimeField, TimeField


class User(models.Model):
    tgid = models.IntegerField()
    name = models.CharField(
        max_length=50,
        blank=True
    )
    surname = models.CharField(
        max_length=50,
        blank=True
    )
    email = models.EmailField(
        blank=True
    )
    adress = models.CharField(
        max_length=100,
        blank=True
    )
    phone = models.CharField(
        max_length=20,
        blank=True
    )

    def __str__(self):
        return self.name
    

class Storage(models.Model):
    address = models.CharField(
        max_length=100
    )
    work_time = models.CharField(
        max_length=50
    )

    def __str__(self):
        return f'склад по адресу: {self.address}'
    
    
class Cell(models.Model):
    storage = models.ForeignKey(
        Storage,
        verbose_name='Склад',
        related_name='boxes',
        on_delete=models.CASCADE
    )
    size = models.CharField(
        max_length=100
    )
    price = models.FloatField()
    booked = models.BooleanField(
        default=False
        )
    lease_time = DateTimeField()

    def __str__(self):
        return 'Коробка {self.id}, склад {self.storage.id}'

    class Meta:
        verbose_name_plural = 'Boxes'


class Order(models.Model):
    create_time = models.DateTimeField()
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
        default=False
    )
    comment = models.CharField(
        max_length=100,
        blank=True
    )

