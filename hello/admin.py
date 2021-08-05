from django.contrib import admin
from .models import coffee_details, coffee_ratings

# Register your models here.
admin.site.register(coffee_details)
admin.site.register(coffee_ratings)
