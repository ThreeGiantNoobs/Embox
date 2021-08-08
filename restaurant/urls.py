from django.urls import path
from .views import test_invoice, home, restaurant_page

urlpatterns = [
    path('test', test_invoice),
    path('', home, name='home'),
    path('restaurant/<int:restaurant_id>', restaurant_page, name='restaurant'),
]