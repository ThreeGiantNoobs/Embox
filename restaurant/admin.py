from django.contrib import admin
from .models import Restaurant, Cuisines, Dishes

# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Cuisines)
admin.site.register(Dishes)
