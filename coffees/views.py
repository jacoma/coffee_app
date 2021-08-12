from coffees.forms import NewCoffeeForm
import re
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import ratings, User, dim_coffee
from .forms import NewCoffeeForm

# Create your views here.

def user_coffees(request, username):
    active_user = get_object_or_404(User, username = username)
    coffees = dim_coffee.objects.all() #TODO FILTER FOR THE USER's COFFEES
    return render(
        request,
        'user_coffees.html',
        {'user':active_user, 'coffees':coffees}
    )

def add_coffee(request, username):
    active_user = get_object_or_404(User, username = username)
    if request.method == 'POST':
        form=NewCoffeeForm(request.POST)
        if form.is_valid():
            coffee = form.save()
            return redirect(
                'user_coffees',
                username=active_user.username
            )
    else:
        form=NewCoffeeForm()
    return render(
        request,
        'add_coffee.html',
        {'user':active_user, 'form': form}
    )