# Generated by Django 3.2.6 on 2021-08-08 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_auto_20210808_0843'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='picture_external',
            field=models.URLField(null=True, verbose_name='external image'),
        ),
    ]