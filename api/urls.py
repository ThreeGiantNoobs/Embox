from django.urls import path
from .views import search, cart, order, clear_cart, import_database

urlpatterns = [
    path('search', search),
    path('cart', cart),
    path('order', order),
    path('clear-cart', clear_cart),
    path('import_database', import_database),
]
