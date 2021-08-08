from rest_framework import serializers

from restaurant.models import Restaurant, Currency, Dishes, CartDishOrder


class SearchSerializer(serializers.Serializer):
    choices = [
        ('-rating', 'rating'),
        ('avg_cost', 'avg_cost'),
        ('-avg_cost', 'avg_cost_rich'),
        ('-votes', 'votes'),
    ]
    query = serializers.CharField(max_length=200, allow_blank=True, required=False)
    cuisines = serializers.ListField(child=serializers.CharField(), required=False)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)
    distance = serializers.IntegerField(required=False)
    country_id = serializers.IntegerField(required=False)
    is_delivering_now = serializers.BooleanField(required=False)
    max_cost = serializers.IntegerField(required=False)
    start = serializers.IntegerField(required=False)
    chunk = serializers.IntegerField(max_value=70, required=False)
    has_table_booking = serializers.BooleanField(required=False)
    veg = serializers.BooleanField(required=False)
    sort_by = serializers.ChoiceField(choices=choices, required=False)
    min_rating = serializers.IntegerField(min_value=0, max_value=5, required=False)


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        read_only = True
        fields = ['name']


class RestaurantSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        read_only = True
        fields = ['restaurant_id', 'restaurant_name', 'pictures', 'address', 'avg_cost', 'currency',
                  'has_table_booking', 'is_delivering_now', 'rating', 'votes']


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes
        fields = ['name', 'veg', 'eta', 'price', 'picture', 'restaurant', 'id']


class CartDishOrderSerializer(serializers.ModelSerializer):
    dish = DishSerializer()

    class Meta:
        model = CartDishOrder
        fields = ['quantity', 'dish']


class CartChangesSerializer(serializers.Serializer):
    inc_by = serializers.IntegerField(required=True)
    dish_id = serializers.IntegerField(required=True)
    delete = serializers.BooleanField(required=False)


class OrderInputSerializer(serializers.Serializer):
    delivery_address = serializers.CharField(required=True)
    instruction = serializers.CharField(required=False)
