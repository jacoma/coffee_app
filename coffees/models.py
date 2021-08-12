from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class dim_coffee(models.Model):

    class coffeeProcess(models.TextChoices):
        WASHED = 'WA', ('Washed')
        NATURAL = 'NA', ('Natural')
        EA = 'EA', ('EA Decaf')
        SWISSWATER = 'SW', ('Swiss Water Decaf')

    coffee_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    roaster = models.CharField(max_length=100)
    farmer = models.CharField(max_length = 50, null = True)
    region = models.CharField(max_length = 50, null = True)
    country = models.CharField(max_length = 50, null = True)
    varietals = models.CharField(max_length = 100, null = True)
    process = models.CharField(
        max_length=2,
        choices=coffeeProcess.choices,
        null = True
    )
    elevation = models.IntegerField(null = True)
    roaster_notes = models.TextField(max_length=4000, default='', null = True)

    def __str__(self):
        return self.name

class ratings(models.Model):

    class coffeeRating (models.IntegerChoices):
        No = 1
        Tolerable = 2
        Good = 3
        Like = 4
        Love = 5

    class brewMethod(models.TextChoices):
        V60 = 'V', ('V60')
        CHEMEX = 'CX', ('Chemex')
        KALITA = 'KA', ('Kalita Wave')
        CLOVER = "CR", ('Clover')
        AEROPRESS = 'AP', ('AeroPress')
        FRENCHPRESS = 'FP', ('French Press')

    rating_id = models.AutoField(primary_key=True)
    coffee_id = models.ForeignKey(dim_coffee, null=False, on_delete=models.DO_NOTHING)
    brew_method = models.CharField(
        max_length=2,
        choices=brewMethod.choices,
        null = True
    )
    tasting_notes = models.TextField(max_length=4000, null = True)
    rating = models.IntegerField(
        choices = coffeeRating.choices
    )
    last_updated = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, default='', null=True, blank=True, on_delete=models.SET_NULL)





