from django.urls import path
from .views import search, cart, order, clear_cart

urlpatterns = [
    path('search/', search),
    path('cart/', cart),
    path('order/', order),
    path('order/', clear_cart),
]
