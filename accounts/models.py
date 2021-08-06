from django.db import models
from restaurant.models import Restaurant
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustUser(AbstractUser):
    ...


class BusinessUser(AbstractUser):
    name = models.CharField()
    business_name = models.CharField()
    restaurants = models.ForeignKey(Restaurant, blank=True, null=True, on_delete=models.CASCADE)
