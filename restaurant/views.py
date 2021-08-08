from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from restaurant.models import Restaurant
from .models import Order
from .utils import export_invoice_pdf
from .utils import search

# Create your views here.


@api_view()
def test_invoice(request: Request):
    if request.method == 'GET':
        order_id = request.GET.get('id')
        debug = True if request.GET.get('debug') else False
        order = Order.objects.get(order_id=order_id)
        print(order)
        export_invoice_pdf(order=order, path='output.pdf')
    return Response({'sd': ''}, status=status.HTTP_200_OK)


def home(request):
    user = request.user
    data = {}
    rest = search()
    data.update({'restaurants': rest.values()})
    print(data)
    return render(request, 'home.html', data)


def restaurant_page(request, restaurant_id=1):
    query = Restaurant.objects.filter(restaurant_id=restaurant_id)
    if not query.exists():
        return HttpResponse('404')
    restaurant = query[0]


