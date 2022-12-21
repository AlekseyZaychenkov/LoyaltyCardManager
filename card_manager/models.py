from datetime import datetime

from django.db import models
from djmoney.models.fields import MoneyField


class Card(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField()
    series = models.IntegerField()
    release_date = models.DateTimeField()
    end_date = models.DateTimeField()

    NOT_ACTIVATED = 'Not activated'
    ACTIVATED = 'Activated'
    EXPIRED = 'Expired'
    STATUS_CHOICES = [
        (NOT_ACTIVATED, 'Not activated'),
        (ACTIVATED, 'Activated'),
        (EXPIRED, 'Expired'),
    ]

    status = models.CharField(
        max_length=13,
        choices=STATUS_CHOICES,
        default=NOT_ACTIVATED,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['series', 'number'], name='unique_series_number_combination'
            )
        ]


class Purchase(models.Model):
    id = models.AutoField(primary_key=True)
    sum = MoneyField(max_digits=14, decimal_places=2, default_currency='RUB')
    date_time = models.DateTimeField(default=datetime.now())
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

