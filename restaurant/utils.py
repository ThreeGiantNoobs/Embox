from .models import Restaurant, Dishes, Cuisines


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
    if latitude and longitude:
        la_diff = distance / 100
        print(la_diff)
        query_set = query_set.filter(latitude__lte=latitude + la_diff, latitude__gte=latitude - la_diff)
        print(query_set)
        query_set = query_set.filter(longitude__lte=longitude + la_diff, longitude__gte=longitude - la_diff)
    query_set = query_set.order_by(sort_by)
    print(query_set.values())
    return query_set
