from django.contrib import admin
from .models import Restaurant, Cuisines, Dishes, Currency, Order, DishOrder, CartDishOrder

# Register your models here.

admin.site.register(Order)
admin.site.register(DishOrder)
admin.site.register(Restaurant)
admin.site.register(Cuisines)
admin.site.register(Dishes)
admin.site.register(CartDishOrder)
admin.site.register(Currency)
