from django.db import models
from django.contrib.auth.models import AbstractUser


class CustUser(AbstractUser):
    email = models.EmailField(blank=False, null=False)


class CorpUser(CustUser):
    business_name = models.CharField(max_length=100)

