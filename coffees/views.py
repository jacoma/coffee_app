from coffees.forms import NewCoffeeForm
import re
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from coffees.models import ratings, User, dim_coffee
from .forms import NewCoffeeForm, NewRatingForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def add_coffee(request):
    if request.method == 'POST':
        form=NewCoffeeForm(request.POST)
        if form.is_valid():
            coffee = form.save(commit=False)
            coffee.name = ''
            coffee.roaster = ''
            coffee.save()
            return redirect(
                'user_coffees'
            )
    else:
        form=NewCoffeeForm()
    return render(
        request,
        'add_coffee.html',
        {'form': form}
    )

@login_required
def add_rating(request):
    coffees = dim_coffee.objects.all()
    if request.method == 'POST':
        form=NewRatingForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            # rate.coffee_id
            rate.user = request.user
            rate.brew_method = ''
            rate.rating = ''
            rate.save()
            return redirect(
                'user_coffees'
            )
    else:
        form=NewRatingForm()
    return render(
        request,
        'add_rating.html',
        {'coffee': coffees, 'form': form}
    )