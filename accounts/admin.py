from django.contrib import admin
from .models import CorpUser, CustUser

# Register your models here.
admin.site.register(CustUser)
admin.site.register(CorpUser)
