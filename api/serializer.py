from rest_framework import serializers


class SearchSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=200, allow_blank=False, required=False)
    cuisine = serializers.CharField(max_length=50, allow_blank=False, required=False)
    country = serializers.CharField(max_length=20, allow_blank=False, required=False)
    distance = serializers.IntegerField()
