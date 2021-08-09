from coffees.forms import NewCoffeeForm
import re
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import ratings, User, dim_coffee
from .forms import NewCoffeeForm

# Create your views here.

def home(request):
    return render(
        request,
        'home.html'
    )

def user_home(request, username):
    active_user = get_object_or_404(User, username = username)
    coffees = dim_coffee.objects.all()
    return render(
        request,
        'user_home.html',
        {'user':active_user, 'coffees':coffees}
    )

def user_coffees(request, username):
    active_user = get_object_or_404(User, username = username)
    coffees = dim_coffee.objects.all()
    return render(
        request,
        'user_coffees.html',
        {'user':active_user, 'coffees':coffees}
    )

def add_coffee(request, username):
    active_user = get_object_or_404(User, username = username)
    # user = User.objects.first()  # TODO: get the currently logged in user
    
    if request.method == 'POST':
        form=NewCoffeeForm(request.POST)
        if form.is_valid():
            # name = form.cleaned_data['coffee_name']
            # roaster = form.cleaned_data['roaster_name']
            # #rating = request.POST['rating']
            # coffee = dim_coffee(name=name,
            #     roaster=roaster
            # )
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