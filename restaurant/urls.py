from django.urls import path
from .views import test_invoice, home

urlpatterns = [
    path('test', test_invoice),
    path('', home, name='home'),
]