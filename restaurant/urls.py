from django.urls import path
from .views import test_invoice

urlpatterns = [
    path('test', test_invoice),
]