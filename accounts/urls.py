from django.urls import path
from .views import custRegister, corpRegister, login, accLogout, me

urlpatterns = [
    path('ping/', me),
    path('login/', login),
    # path('clogin/', corpLogin),
    path('register/', custRegister),
    path('cregister/', corpRegister),
    path('logout/', accLogout),
]