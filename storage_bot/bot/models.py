from django.db import models

class User(models.Model):
    name = models.CharField(
        verbose_name='Имя и Фамилия пользователя',
        max_length=50
    )
    email = models.CharField(max_length=50)


