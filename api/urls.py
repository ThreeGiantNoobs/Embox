from django.urls import path
from .views import search, cart, order

urlpatterns = [
    path('search/', search),
    path('cart/', cart),
    path('order/', order),
]
