from django.db import models


class User(models.Model):
    name = models.CharField(
        verbose_name='Имя',
        max_length=50
    )
    surname = models.CharField(
        verbose_name='Фамилия',
        max_length=50
    )
    email = models.EmailField(
        verbose_name='Email',
    )
    adress = models.CharField(
        max_length=100,
        verbose_name='Адрес',
    )
    # phone = models.
    

class Stock:
    adress = models.CharField(
        max_length=100,
        verbose_name='Адрес',
    )
    # working_mode = 
    
    
class Storage_cell(models.Model):
    stock = models.ForeignKey(
        Stock,
        verbose_name='Склад',
        on_delete=models.CASCADE
    )
    size = models.FloatField(
        verbose_name='Размер',
    )
    price = models.FloatField(
        verbose_name='Цена аренды',
    )
    booked = models.BooleanField(
        verbose_name='Забронировано',
    )


class Order(models.Model):
    create_date = models.DateField(
        verbose_name='Дата создания заказа'
    )
    # rental_period = 
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    storage_cell = models.ForeignKey(
        Storage_cell,
        verbose_name='Ячейка',
        on_delete=models.CASCADE
    )


