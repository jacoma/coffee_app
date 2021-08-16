from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.conf import settings
from django.contrib.auth.models import User

class countries(models.Model):
    country_code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30, null=True)	
    country_code_alpha= models.CharField(max_length=2, null=True)	
    country_code_alpha3	= models.CharField(max_length=3, null=True)
    name_long= models.CharField(max_length=50, null=True)	
    latitude= models.FloatField(null=True)	
    longitude= models.FloatField(null=True)

    def __str__(self):
        return self.name

class dim_roaster(models.Model):
    roaster_id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.name

class dim_notes(models.Model):
    flavor_notes = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.flavor_notes

class dim_varietal(models.Model):
    varietal = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.varietal

# Create your models here.
class dim_coffee(models.Model):

    class coffeeProcess(models.TextChoices):
        WASHED = 'WA', ('Washed')
        NATURAL = 'NA', ('Natural')
        EA = 'EA', ('EA Decaf')
        SWISSWATER = 'SW', ('Swiss Water Decaf')

    # class varietal_choices(models.TextChoices):
    #     WASHED = 'WA', ('Washed')
    #     NATURAL = 'NA', ('Natural')
    #     EA = 'EA', ('EA Decaf')
    #     SWISSWATER = 'SW', ('Swiss Water Decaf')

    coffee_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=True)
    roaster = models.ForeignKey(dim_roaster, to_field='roaster_id', null=True, on_delete=models.DO_NOTHING, related_name="coffees")
    farmer = models.CharField(max_length = 50, null = True)
    country = models.ForeignKey(countries, to_field='country_code', null=True, on_delete=models.DO_NOTHING, related_name="coffees")
    # region = models.CharField(max_length = 50, null = True)
    varietals = models.ManyToManyField(dim_varietal, related_name = 'varieties')
    process = models.CharField(
        max_length=2,
        choices=coffeeProcess.choices,
        null = True
    )
    elevation = models.IntegerField(null = True)
    roaster_notes = models.ManyToManyField(dim_notes)

    def __str__(self):
        return self.coffee_id

class ratings(models.Model):

    class ratings_scale(models.IntegerChoices):
        [
            (1,1),
            (2,2),
            (3,3),
            (4,4),
            (5,5)
        ]

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
    coffee = models.ForeignKey(dim_coffee, null=True, on_delete=models.DO_NOTHING)
    brew_method = models.CharField(
        max_length=2,
        choices=brewMethod.choices,
        null = True
        )
    # tasting_notes = models.ManyToManyField(dim_notes)
    reaction = models.TextField(max_length=500, null=True)
    # volume= models.IntegerField(
    #     choices = ratings_scale.choices, null=True
    #     )
    acidity= models.IntegerField(
        choices = ratings_scale.choices, null=True
        )   
    sweetness= models.IntegerField(
        choices = ratings_scale.choices, null=True
        )
    complexity = models.IntegerField(
        choices = ratings_scale.choices, null=True
        )
    balance = models.IntegerField(
        choices = ratings_scale.choices, null=True
        )
    rating = models.IntegerField(
        choices = coffeeRating.choices, null=True
        )
    last_updated = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, default='', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.rating_id




