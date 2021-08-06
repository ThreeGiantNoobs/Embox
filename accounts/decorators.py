from .models import CustUser, CorpUser
from rest_framework import status
from rest_framework.response import Response


def auth(func, message='You are not logged in'):
    def wrapper(*args, **kwargs):
        req = args[0]
        user = req.user
        if user.is_authenticated:
            return func(*args, **kwargs)
        else:
            return Response({'message': message}, status=status.HTTP_401_UNAUTHORIZED)
    return wrapper


def checkLoggedIn(func, message='Already Logged In'):
    def wrapper(*args, **kwargs):
        req = args[0]
        user = req.user
        if user.is_authenticated:
            return Response({'message': message}, status=status.HTTP_200_OK)
        else:
            return func(*args, **kwargs)
    return wrapper