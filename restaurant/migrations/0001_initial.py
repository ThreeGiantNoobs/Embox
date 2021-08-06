# Generated by Django 3.2.6 on 2021-08-06 14:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cuisines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cuisine_name', models.CharField(default=None, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('restaurant_id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Restaurant ID')),
                ('restaurant_name', models.CharField(max_length=100, verbose_name='Restaurant Name')),
                ('country', models.IntegerField(default=1, verbose_name='Country ID')),
                ('city', models.CharField(max_length=100, verbose_name='City Name')),
                ('address', models.CharField(max_length=255, verbose_name='Address')),
                ('locality', models.CharField(max_length=255, verbose_name='Locality')),
                ('locality_verbose', models.CharField(max_length=255, verbose_name='Locality Landmarks')),
                ('longitude', models.FloatField(validators=[django.core.validators.MaxValueValidator(-180), django.core.validators.MinValueValidator(180)])),
                ('latitude', models.FloatField(validators=[django.core.validators.MaxValueValidator(-85.05), django.core.validators.MinValueValidator(85.05)])),
                ('avg_cost', models.IntegerField(verbose_name='Average cost for two')),
                ('currency', models.CharField(default='Indian Rupees(Rs.)', max_length=50)),
                ('has_table_booking', models.BooleanField(verbose_name='Allow Table Booking')),
                ('is_delivering_now', models.BooleanField(verbose_name='Delivering now')),
                ('rating', models.FloatField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)], verbose_name='Rating')),
                ('votes', models.IntegerField(default=0, verbose_name='Number of votes')),
                ('price_range', models.IntegerField(default=2, validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(1)], verbose_name='Price Range')),
                ('cuisines', models.ManyToManyField(to='restaurant.Cuisines')),
            ],
        ),
    ]
