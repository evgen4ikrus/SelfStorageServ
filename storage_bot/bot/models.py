from django.db import models


class User(models.Model):

    status_choices = [
        (0, "Free"),
        (1, "Booked"),
        (2, "Paid"),
        (3, "Occupied"),
    ]

    renter = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        verbose_name='Арендатор',
        related_name='boxes',
        blank=True,
    )
    rent_period = models.DateTimeField('Дата окончания аренды', blank=True)
    storage = models.ForeignKey(
        Storage,
        on_delete=models.CASCADE,
        verbose_name='Склад',
        related_name='boxes',
    )
    status = models.CharField(
        max_length=2,
        choices=status_choices,
        default=status_choices[0]
    )

    def __str__(self):
        return 'Коробка {self.id}, склад {self.storage.id}'

    class Meta:
        verbose_name_plural = "Boxes"


class Order(models.Model):
    """Модель заказа."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Заказчик',
        related_name='orders'
    )
    creation_date = models.DateTimeField('Дата создания заказа')
    box = models.ForeignKey(
        Box,
        on_delete=models.CASCADE,
        verbose_name='Номер ячейки',
        related_name='orders'
    )
    comment = models.CharField(blank=True, max_length=100)
