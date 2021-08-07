from .models import CorpUser, CustUser
from .decorators import auth, checkLoggedIn
from .serializers import CorpSerializer, CustSerializer
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout, authenticate


@api_view(['GET', 'POST'])
@checkLoggedIn
def custRegister(request: Request, backend='django.contrib.auth.backends.ModelBackend'):
    serialed = CustSerializer(data=request.data)
    if serialed.is_valid():
        user: CustUser = CustUser.objects.create_user(username=serialed.data.get('username'),
                                                      email=serialed.data.get('email'),
                                                      password=serialed.data.get('password'))
        user.save()
        login(request, user)
        return Response(f'{user}', status=status.HTTP_201_CREATED)
    else:
        return Response(serialed.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@checkLoggedIn
def corpRegister(request: Request, backend='django.contrib.auth.backends.ModelBackend'):
    serialed = CorpSerializer(data=request.data)
    if serialed.is_valid():
        user: CorpUser = CorpUser.objects.create_user(username=serialed.data.get('username'),
                                                      business_name=serialed.data.get('business_name'),
                                                      email=serialed.data.get('email'),
                                                      password=serialed.data.get('password'))
        user.save()
        login(request, user)
        return Response(f'{user}', status=status.HTTP_201_CREATED)
    else:
        return Response(serialed.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@checkLoggedIn
def accLogin(request: Request):
    serialed = authenticate(username=request.data.get('username'),
                            password=request.data.get('password'))
    isUser = CustUser.objects.filter(username=request.data.get('username'))
    
    if serialed is not None and isUser:
        login(request, serialed)
        return Response({'message': 'Successfully logged in'}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_403_FORBIDDEN)


# @api_view(['POST'])
# @checkLoggedIn
# def corpLogin(request: Request):
#     serialed = authenticate(username=request.data.get('username'),
#                             business_name=request.data.get('business_name'),
#                             password=request.data.get('password'))
#     isUser = CorpUser.objects.filter(username=request.data.get('username'),
#                                      business_name=request.data.get('business_name'))
#
#     if serialed is not None and isUser:
#         login(request, serialed)
#         return Response({'message': 'Successfully logged in'}, status=status.HTTP_200_OK)
#     return Response({'error': 'Invalid Credentials'}, status=status.HTTP_403_FORBIDDEN)


@api_view()
def accLogout(request: Request):
    if request.user.is_anonymous:
        return Response({'message': 'User not logged in'}, status=status.HTTP_204_NO_CONTENT)
    logout(request)
    return Response({'message': 'YAY'}, status=status.HTTP_200_OK)


@api_view()
@auth
def me(request: Request):
    user: CustUser = request.user
    return Response({'id': user.id, 'username': user.username}, status=status.HTTP_200_OK)
