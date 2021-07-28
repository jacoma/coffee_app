import re
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.shortcuts import render
from .models import coffee_details

def home(request):
    coffees = coffee_details.objects.all()
    return render(
        request,
        'hello/home.html',
        {'coffees':coffees}
    )

def start_coffee(request):
    return render(
        request,
        'hello/start_coffee.html'
    )