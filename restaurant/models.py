from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import CorpUser, CustUser


class Cuisines(models.Model):
    cuisine_name = models.CharField(default=None, max_length=50)

    def __str__(self):
        return f'cuisine_name: {self.cuisine_name}'


class Currency(models.Model):
    name = models.CharField(default=None, max_length=30)

    def __str__(self):
        return '%s' % self.name


class Restaurant(models.Model):
    # TODO: REMOVE BLANK=True and null=True
    restaurant_id = models.BigAutoField(verbose_name='Restaurant ID', primary_key=True)
    owner = models.ForeignKey(CorpUser, on_delete=models.CASCADE)
    restaurant_name = models.CharField(null=False, verbose_name='Restaurant Name', max_length=100)
    pictures = models.ImageField(upload_to='images/restaurant', blank=True, null=True)
    country = models.IntegerField(default=1, verbose_name='Country ID')
    city = models.CharField(null=False, verbose_name='City Name', max_length=100)
    address = models.CharField(null=False, verbose_name='Address', max_length=255)
    locality = models.CharField(null=False, verbose_name='Locality', max_length=255)
    locality_verbose = models.CharField(null=False, verbose_name='Locality Landmarks', max_length=255)
    longitude = models.FloatField(validators=[MaxValueValidator(180), MinValueValidator(-180)])
    latitude = models.FloatField(validators=[MaxValueValidator(85.05), MinValueValidator(-85.05)])
    avg_cost = models.IntegerField(verbose_name='Average cost for two')
    currency = models.ManyToManyField(Currency)
    cuisines = models.ManyToManyField(Cuisines)
    has_table_booking = models.BooleanField(verbose_name='Allow Table Booking')
    is_delivering_now = models.BooleanField(verbose_name='Delivering now')
    rating = models.FloatField(verbose_name='Rating', validators=[MaxValueValidator(5), MinValueValidator(0)],
                               default=0)
    votes = models.IntegerField(verbose_name='Number of votes', default=0)
    price_range = models.IntegerField(verbose_name='Price Range', default=2,
                                      validators=[MaxValueValidator(4), MinValueValidator(1)])

    def __str__(self):
        return f'restaurant_id: {self.restaurant_id}, restaurant_name: {self.restaurant_name}'


class Dishes(models.Model):
    name = models.CharField(verbose_name='Dish Name', max_length=200)
    veg = models.BooleanField(verbose_name='Veg or not')
    eta = models.IntegerField(verbose_name='ETA to make the dish')
    price = models.IntegerField(verbose_name='Price')
    picture = models.ImageField(upload_to='images/dishes/', verbose_name='Picture of Dish', blank=True, null=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f'{self.name}: {self.restaurant.restaurant_name}'


class Order(models.Model):
    order_id = models.BigAutoField(verbose_name='Order ID', primary_key=True)
    restaurant = models.ForeignKey(Restaurant, null=True, on_delete=models.SET_NULL)
    buyer = models.ForeignKey(CustUser, null=True, on_delete=models.SET_NULL)
    instruction = models.TextField(blank=True, null=True)
    delivery_address = models.TextField(verbose_name='Address', null=True, blank=True)
    delivery_charges = models.IntegerField(verbose_name='delivery_charges')
    price = models.IntegerField(validators=[MinValueValidator(0)])
    total_price = models.IntegerField(validators=[MinValueValidator(0)])
    
    def __str__(self):
        return f'{self.order_id} {self.buyer} {self.price}'


class DishOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='Quantity', default=1, validators=[MinValueValidator(1)])
    dish = models.ForeignKey(Dishes, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.order.order_id} {self.dish}'


class CartDishOrder(models.Model):
    quantity = models.IntegerField(verbose_name='Quantity', default=1, validators=[MinValueValidator(1)])
    dish = models.ForeignKey(Dishes, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(CustUser, verbose_name='Cart', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.dish}'
