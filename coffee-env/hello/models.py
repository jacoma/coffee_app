from django.db import models

# Create your models here.

class coffee_details(models.Model):

    class coffeeProcess(models.TextChoices):
        WASHED = 'WA', ('Washed')
        NATURAL = 'NA', ('Natrual')
        EA = 'EA', ('EA Decaf')
        SWISSWATER = 'SW', ('Swiss Water Decaf')

    class coffeeRating (models.IntegerChoices):
        No = 1
        Tolerable = 2
        Good = 3
        Like = 4
        Love = 5

    coffee_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    roaster = models.CharField(max_length=100)
    farmer = models.CharField(max_length = 50, null = True)
    region = models.CharField(max_length = 50)
    country = models.CharField(max_length = 50)
    varietals = models.CharField(max_length = 100, null = True)
    process = models.CharField(
        max_length=2,
        choices=coffeeProcess.choices
    )
    elevation = models.IntegerField()
    tasting_notes = models.TextField(max_length=4000)
    rating = models.IntegerField(
        choices = coffeeRating.choices
    )

    def __str__(self):
        return self.name
