from django.urls import path
from .views import custRegister, corpRegister, accLogin, accLogout, me

urlpatterns = [
    path('ping/', me),
    path('login/', accLogin),
    # path('clogin/', corpLogin),
    path('register/', custRegister),
    path('cregister/', corpRegister),
    path('logout/', accLogout),
]
