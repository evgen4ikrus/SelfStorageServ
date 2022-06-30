from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import DateTimeField
from django.db.models.fields.related import ForeignKey

class User(models.Model):
    name = models.CharField(
        verbose_name='Имя и Фамилия пользователя',
        max_length=50
    )
    email = models.CharField(max_length=50)

class Box(models.Model):
    adress = models.CharField(max_length=200)
    number = models.IntegerField()
    user = ForeignKey(User, on_delete=models.CASCADE)
    period = DateTimeField()

