import csv

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.decorators import auth
from accounts.models import CustUser, CorpUser
from restaurant.Exceptions import DishDontExist, CartDiffRestaurantError
from restaurant.models import Order, Restaurant, DishOrder, Dishes, Cuisines, Currency
from restaurant.utils import search as se, add_cart
from .serializer import SearchSerializer, RestaurantSerializer, CartDishOrderSerializer, CartChangesSerializer, \
    OrderInputSerializer
from django.contrib import auth as dj_auth


def manipulate_search_params(data: dict):
    list_params = ['cuisines']
    # bool_params = ['veg', 'has_table_booking', 'is_delivering_now']
    # integer_fields = ['country_id']
    for key, val in data.items():
        if type(val) is list and len(val) == 1:
            data.update({key: val[0]})
    for param in list_params:
        if data.get(param):
            val = data.get(param)
            if type(param) is not list:
                data.update({param: [val]})
    return data


@api_view()
def search(request: Request):
    data = manipulate_search_params(dict(request.GET))
    print(data)
    serialized_data = SearchSerializer(data=data)
    if not serialized_data.is_valid():
        # print(serialized_data.data)
        return Response({'error': serialized_data.errors}, status=status.HTTP_400_BAD_REQUEST)
    print(serialized_data.errors)
    ans = se(**serialized_data.data)
    print(ans)
    ser = RestaurantSerializer(data=ans, many=True)
    print(ser.is_valid())
    print(ser.data, 'dsd')
    return Response({'res': ser.data}, status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
@auth
def cart(request: Request):
    user: CustUser = request.user
    if request.method == 'POST':
        serialized_edit_data = CartChangesSerializer(data=request.data)
        if not serialized_edit_data.is_valid():
            return Response({'error': serialized_edit_data.errors}, status=status.HTTP_400_BAD_REQUEST)
        change_data = serialized_edit_data.data
        print(change_data)
        try:
            add_cart(user, dish_id=change_data['dish_id'], inc_by=change_data['inc_by'],
                     delete=change_data.get('delete'))
        except CartDiffRestaurantError:
            return Response({'error': 'cart diff restaurant'}, status=status.HTTP_400_BAD_REQUEST)
        except DishDontExist:
            return Response({'error': 'DishDontExist'}, status=status.HTTP_400_BAD_REQUEST)

    query_set = user.cartdishorder_set.all()
    if not query_set.exists():
        return Response({'res': []}, status=status.HTTP_200_OK)
    data = query_set
    serialized_data = CartDishOrderSerializer(data, many=True)
    return Response({'res': serialized_data.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@auth
def clear_cart(request: Request):
    user: CustUser = request.user
    user.cartdishorder_set.all().delete()
    return Response({'msg': 'ok'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@auth
def order(request: Request):
    serialized_input = OrderInputSerializer(data=request.data)
    if not serialized_input.is_valid():
        return Response({'error': serialized_input.errors}, status=status.HTTP_400_BAD_REQUEST)
    serialized_input_data = serialized_input.data

    user: CustUser = request.user
    query_set = user.cartdishorder_set.all()
    data = query_set
    serialized_data = CartDishOrderSerializer(data, many=True)
    if len(serialized_data.data) <= 0:
        return Response({'error': 'order empty'}, status.HTTP_400_BAD_REQUEST)

    restaurant_id = serialized_data.data[0].get('dish').get('restaurant')
    _restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)

    # FIXME: delivery charges are fixed here
    _order: Order = Order.objects.create(restaurant=_restaurant, buyer=user, delivery_charges=30,
                                         instruction=serialized_input_data.get('instruction'),
                                         delivery_address=serialized_input_data.get('delivery_address'), price=0,
                                         total_price=30)
    for obj in serialized_data.data:
        dish_id = obj.get('dish').get('id')
        dish = Dishes.objects.get(id=dish_id)
        quantity = obj.get('quantity')
        DishOrder.objects.create(order=_order, quantity=quantity, dish=dish)
        price_to_add = dish.price * quantity
        _order.price += price_to_add
        _order.total_price += price_to_add
        _order.save()

    user.cartdishorder_set.all().delete()
    return Response({'msg': 'success'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def import_database(request: Request):
    file_name = request.data.get('filename')
    # user: CorpUser = request.user
    user_id = request.user.id
    user = CorpUser.objects.get(id=user_id)
    print(type(user))
    # if not isinstance(user, CorpUser):
    #     return Response({'error': 'not a corp user'}, status=status.HTTP_400_BAD_REQUEST)
    with open(file_name, newline='') as f:
        reader = csv.reader(f)
        currency = Currency.objects.all()[0]
        for row in reader:
            if row[0].isnumeric():
                cuisines = row[9].split(',')
                cuisene = []
                for cuis in cuisines:
                    cuis = cuis.strip()
                cuisene.append(Cuisines.objects.create(cuisine_name=cuis))
                obj = Restaurant.objects.create(restaurant_name=row[1], country=int(row[2]), address=row[3],
                                                locality=row[5], longitude=float(row[7]), latitude=float(row[8]),
                                                avg_cost=int(row[10]), is_delivering_now=True,
                                                price_range=int(row[16]), owner=user,
                                                has_table_booking=True if row[13] == 'Yes' else False,
                                                rating=float(row[17]), picture_external=row[21])
                obj.currency.add(currency)
                for c in cuisene:
                    obj.cuisines.add(c)

                obj.save()
