import re
from itertools import combinations
from typing import List

from django.db.models import Q, QuerySet
from fpdf import FPDF
from strsimpy.normalized_levenshtein import NormalizedLevenshtein

from accounts.models import CustUser
from .Exceptions import CartDiffRestaurantError, DishDontExist
from .models import Restaurant, Order, Dishes, DishOrder, CartDishOrder

norm = NormalizedLevenshtein()


class Invoice(FPDF):
    def __init__(self, *args, debug=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.debug = debug

    def header(self, title='TGN-EATS'):
        self.image('logo.png', 80, 8, 45)
        self.set_font('helvetica', 'B', 20)
        self.ln(10)
        self.cell(80)
        self.cell(30, 10, title, border=self.debug, align='C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'{self.page_no()}/{{nb}}', align='C', border=self.debug)


def filter_args(veg: bool = None, has_table_booking: bool = None, is_delivering_now: bool = None, max_cost: int = None,
                cuisines: list = None) -> dict:
    args = {}
    if veg is not None:
        args.update({
            'dishes__veg': veg
        })
    if cuisines:
        args.update({
            'cuisines__cuisine_name__in': cuisines
        })
    if has_table_booking is not None:
        args.update({
            'has_table_booking': has_table_booking
        })
    if is_delivering_now is not None:
        args.update({
            'is_delivering_now': is_delivering_now
        })
    if max_cost:
        args.update({
            'avg_cost__lte': max_cost
        })
    return args


def location_filter(query_set, latitude=None, longitude=None, distance: int = 10):
    if latitude and longitude:
        la_diff = distance / 100
        print(la_diff)
        query_set = query_set.filter(latitude__lte=latitude + la_diff, latitude__gte=latitude - la_diff)
        print(query_set)
        query_set = query_set.filter(longitude__lte=longitude + la_diff, longitude__gte=longitude - la_diff)
    return query_set


# TODO: add all params to separate search as well or remove them

"""-----------------------------------------------------------------------------------------------------------------"""
# def search_restaurant(query='', cuisines: list = None, country_id: int = 1, latitude=None,
#                       longitude=None, min_rating=0, sort_by='-rating', distance: int = 10):
#     args = {}
#     if cuisines:
#         args.update({
#             'cuisines__cuisine_name__in': cuisines
#         })
#     query_set = Restaurant.objects.filter(restaurant_name__icontains=query, country=country_id, rating__gte=min_rating,
#                                           **args)
#     print(query_set)
#     query_set = location_filter(query_set, latitude=latitude, longitude=longitude, distance=distance)
#     query_set = query_set.order_by(sort_by)
#     print(query_set.values())
#     return query_set
#
#
# def search_dishes(query='', cuisines: list = None, country_id: int = 1, latitude=None,
#                   longitude=None, min_rating=0, sort_by='-rating', distance: int = 10, veg: bool = None):
#     args = {}
#     if cuisines:
#         args.update({
#             'cuisines__cuisine_name__in': cuisines
#         })
#     query_set = Restaurant.objects.filter(dishes__name__icontains=query, country=country_id, rating__gte=min_rating,
#                                           **args)
#     print(query_set)
#     query_set = location_filter(query_set, latitude=latitude, longitude=longitude, distance=distance)
#     query_set = query_set.order_by(sort_by)
#     return query_set

"""-----------------------------------------------------------------------------------------------------------------"""


def universal_search(query='', cuisines: list = None, country_id: int = 1, latitude=None, max_cost: int = None,
                     longitude=None, min_rating=0, sort_by='-rating', distance: int = 10, veg: bool = None,
                     has_table_booking: bool = None, is_delivering_now: bool = None, start: int = 0, chunk: int = 20):
    args = filter_args(veg=veg, has_table_booking=has_table_booking, is_delivering_now=is_delivering_now,
                       cuisines=cuisines, max_cost=max_cost)
    print(args)
    if veg is not None:
        query_set = Restaurant.objects.filter(
            (Q(dishes__name__icontains=query) & Q(dishes__veg=veg)) | Q(restaurant_name__icontains=query),
            country=country_id, rating__gte=min_rating,
            **args)
    else:
        query_set = Restaurant.objects.filter(
            Q(dishes__name__icontains=query) | Q(restaurant_name__icontains=query),
            country=country_id, rating__gte=min_rating,
            **args)
    query_set = location_filter(query_set, latitude=latitude, longitude=longitude, distance=distance)
    query_set = query_set.order_by(sort_by)
    query_set = query_set.all()[start:start + chunk]
    return query_set


def make_regex(comb: tuple):
    res = ''
    for i in comb:
        res += f'(?=.*{i})'
    return res


def search(query='', cuisines: list = None, country_id: int = 1, latitude=None, max_cost: int = None,
           longitude=None, min_rating=0, sort_by=None, distance: int = 10, veg: bool = None,
           has_table_booking: bool = None, is_delivering_now: bool = None, start: int = 0, chunk: int = 20):
    args = filter_args(veg=veg, has_table_booking=has_table_booking, is_delivering_now=is_delivering_now,
                       cuisines=cuisines, max_cost=max_cost)
    print(args)

    # panner tikka samosa Please don't remove this

    final_query_set = Restaurant.objects.none()
    query = query.lower()
    query = re.sub(' +', ' ', query)
    query = re.sub(r'[^a-z ]', '', query).strip()
    query_list = query.split()
    query_list = list(filter(lambda t: len(t) > 2, query_list))
    for i in range(len(query_list), 0, -1):
        for comb in combinations(query_list, i):
            regex_pattern = make_regex(comb)
            if veg is not None:
                sm_query_set = Restaurant.objects.filter(
                    (Q(dishes__name__iregex=regex_pattern) & Q(dishes__veg=veg)) | Q(
                        restaurant_name__iregex=regex_pattern),
                    country=country_id, rating__gte=min_rating)
            else:
                sm_query_set = Restaurant.objects.filter(
                    Q(dishes__name__iregex=regex_pattern) | Q(restaurant_name__iregex=regex_pattern),
                    country=country_id, rating__gte=min_rating)
            final_query_set = final_query_set | sm_query_set
    query_set = Restaurant.objects.filter(
        country=country_id, rating__gte=min_rating,
        **args)
    query_set = location_filter(query_set, latitude=latitude, longitude=longitude, distance=distance)
    final_query_set = final_query_set & query_set
    final_query_set = final_query_set.distinct()
    if sort_by:
        final_query_set = final_query_set.order_by(sort_by)
    final_query_set = final_query_set.all()[start:start + chunk]
    final_query_set: QuerySet
    return final_query_set


def export_invoice_pdf(order: Order, path: str = None, debug: bool = False):
    print(order, 'sds')
    dishes: List[QuerySet] = list(order.dishorder_set.all())
    order_id = order.order_id
    restaurant: Restaurant = order.restaurant
    currency = restaurant.currency.get().name
    # price: int, total_price: int, restaurant_name: str, order_id: int, delivery_address: str,
    # delivery_charges: int, dishes: List[DishOrder]
    invoice = Invoice('P', 'mm', 'Letter', debug=debug)
    invoice.add_page()
    invoice.alias_nb_pages()
    invoice.set_auto_page_break(auto=True, margin=15)
    invoice.ln(10)
    invoice.set_font('helvetica', 'IB', 15)
    invoice.cell(80, 14, 'Order Details:')
    invoice.ln(10)
    for dish_order in dishes:
        dish_order: DishOrder
        quantity = dish_order.quantity
        dish: Dishes = dish_order.dish
        invoice.set_font('times', '', 12)
        invoice.cell(0, 10, f'{dish.name}', align='L')
        invoice.ln(5)
        invoice.set_font('times', '', 10)
        invoice.cell(80, 10, f'  [{quantity}] x {currency}{dish.price}', align='L')
        invoice.cell(80, 10, f'{currency}{dish.price * quantity}', align='R')
        invoice.ln(10)
    print(restaurant)
    print(currency)
    invoice.set_font('times', 'B', 12)
    invoice.cell(80, 10, f'Subtotal', align='L')
    invoice.cell(80, 10, f'{currency}{order.price}', align='R', ln=True)

    invoice.cell(80, 10, f'Delivery Charges', align='L')
    invoice.cell(80, 10, f'{currency}{order.delivery_charges}', align='R', ln=True)

    y_cord = invoice.get_y()
    # noinspection PyTypeChecker
    invoice.set_line_width(0.5)
    invoice.set_draw_color(r=255, g=128, b=0)
    invoice.line(x1=0, y1=y_cord, x2=220, y2=y_cord)

    invoice.cell(80, 10, f'Total Price', align='L')
    invoice.cell(80, 10, f'{currency}{order.total_price}', align='R')

    invoice.output(path)

    ...


def add_cart(user: CustUser, dish_id: int, inc_by: int = 1, delete=False):
    dish = Dishes.objects.filter(id=dish_id)
    if not dish.exists():
        raise DishDontExist()
    dish = dish[0]
    cart = user.cartdishorder_set.all()
    if cart.exists():
        cart_restaurant_id = cart[0].dish.restaurant_id
        if dish.restaurant_id != cart_restaurant_id:
            if not delete:
                raise CartDiffRestaurantError()
            cart.delete()
    for _dish in cart:
        _dish: CartDishOrder
        if _dish.dish_id == dish_id:
            _dish.quantity = _dish.quantity + inc_by
            _dish.save()
            return

    if inc_by > 0:
        CartDishOrder.objects.create(user=user, dish=dish, quantity=inc_by).save()
