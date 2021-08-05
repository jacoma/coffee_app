import re
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import coffee_details, coffee_ratings, User

def home(request):
    return render(
        request,
        'hello/home.html'
    )

def user_home(request, username):
    active_user = get_object_or_404(User, username = username)
    coffees = coffee_details.objects.all()
    return render(
        request,
        'hello/user_home.html',
        {'user':active_user, 'coffees':coffees}
    )

def add_coffee(request, username):
    active_user = get_object_or_404(User, username = username)

    if request.method == 'POST':
        name = request.POST['coffee_name']
        roaster = request.POST['roaster_name']
        #rating = request.POST['rating']

        user = User.objects.first()  # TODO: get the currently logged in user

        coffee = coffee_details.objects.create(
            name=name,
            roaster=roaster
        )

        return redirect('user_home', username=active_user.username)
    
    return render(
         request,
        'hello/add_coffee.html',
        {'user':active_user}
    )

def user_profile(request, username):
    active_user = get_object_or_404(User, username = username)
    return render(
        request,
        'hello/user_profile.html',
        {'user':active_user}
    )