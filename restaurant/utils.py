from django.db.models import Q

from .models import Restaurant, Order

from fpdf import FPDF


# class PDF(FPDF):
#     def header(self):
#         self.image('logo.png', 10, 8, 25)



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


def search_restaurant(query='', cuisines: list = None, country_id: int = 1, latitude=None,
                      longitude=None, min_rating=0, sort_by='-rating', distance: int = 10):
    args = {}
    if cuisines:
        args.update({
            'cuisines__cuisine_name__in': cuisines
        })
    query_set = Restaurant.objects.filter(restaurant_name__contains=query, country=country_id, rating__gte=min_rating,
                                          **args)
    print(query_set)
    query_set = location_filter(query_set, latitude=latitude, longitude=longitude, distance=distance)
    query_set = query_set.order_by(sort_by)
    print(query_set.values())
    return query_set


def search_dishes(query='', cuisines: list = None, country_id: int = 1, latitude=None,
                  longitude=None, min_rating=0, sort_by='-rating', distance: int = 10, veg: bool = None):
    args = {}
    if cuisines:
        args.update({
            'cuisines__cuisine_name__in': cuisines
        })
    query_set = Restaurant.objects.filter(dishes__name__contains=query, country=country_id, rating__gte=min_rating,
                                          **args)
    print(query_set)
    query_set = location_filter(query_set, latitude=latitude, longitude=longitude, distance=distance)
    query_set = query_set.order_by(sort_by)
    return query_set


"""-----------------------------------------------------------------------------------------------------------------"""


def universal_search(query='', cuisines: list = None, country_id: int = 1, latitude=None, max_cost: int = None,
                     longitude=None, min_rating=0, sort_by='-rating', distance: int = 10, veg: bool = None,
                     has_table_booking: bool = None, is_delivering_now: bool = None, start: int = 0, chunk: int = 50):
    args = filter_args(veg=veg, has_table_booking=has_table_booking, is_delivering_now=is_delivering_now,
                       cuisines=cuisines, max_cost=max_cost)
    print(args)
    if veg is not None:
        query_set = Restaurant.objects.filter(
            (Q(dishes__name__contains=query) & Q(dishes__veg=veg)) | Q(restaurant_name__contains=query),
            country=country_id, rating__gte=min_rating,
            **args)
    else:
        query_set = Restaurant.objects.filter(
            Q(dishes__name__contains=query) | Q(restaurant_name__contains=query),
            country=country_id, rating__gte=min_rating,
            **args)
    query_set = location_filter(query_set, latitude=latitude, longitude=longitude, distance=distance)
    query_set = query_set.order_by(sort_by)
    query_set = query_set.all()[start:start + chunk]
    return query_set


def export_invoice_pdf(order: Order, path: str = None):
    dishes = list[order.dishorder_set.values().all()]
    order_id = order.order_id
    restaurant: Restaurant = order.restaurant
    
    ...
