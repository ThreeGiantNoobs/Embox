from rest_framework import serializers
from .models import CustUser, CorpUser


class CustSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustUser
        fields = ('username', 'email', 'password')


class CorpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorpUser
        fields = ('username', 'business_name', 'email', 'password')
