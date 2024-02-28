from enum import unique
from django.db import models

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[], help_text='Percentage value (0 to 100)')
    active = models.BooleanField()

    def __str__(self):
        return self.code
