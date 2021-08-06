from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Cuisines(models.Model):
    cuisine_name = models.CharField(default=None, max_length=50)

    def __str__(self):
        return f'cuisine_name: {self.cuisine_name}'


class Dishes(models.Model):
    name = models.CharField(verbose_name='Dish Name', max_length=200)
    veg = models.BooleanField(verbose_name='Veg or not')
    price = models.IntegerField(verbose_name='Price')
    picture = models.ImageField(upload_to='images/dishes/', verbose_name='Picture of Dish', blank=True, null=True)


class Restaurant(models.Model):
    restaurant_id = models.BigAutoField(verbose_name='Restaurant ID', primary_key=True)
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
    currency = models.CharField(default='Indian Rupees(Rs.)', max_length=50)
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
