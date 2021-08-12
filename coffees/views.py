from coffees.forms import NewCoffeeForm
import re
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import ratings, User, dim_coffee
from .forms import NewCoffeeForm, NewRatingForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def add_coffee(request):
    # active_user = username
    if request.method == 'POST':
        form=NewCoffeeForm(request.POST)
        if form.is_valid():
            coffee = form.save(commit=False)
            coffee.name = ''
            coffee.roaster = ''
            coffee.save()
            # ratings.objects.create(
            #     message=form.cleaned_data.get('message'),
            #     topic=topic,
            #     rated_by=request.user  # <- and here
            # )
            return redirect(
                'user_coffees',
                username=request.user
            )
    else:
        form=NewCoffeeForm()
    return render(
        request,
        'add_coffee.html',
        {'username':request.user, 'form': form}
    )

# TODO 
@login_required
def add_rating(request, coffee_id):
    # active_user = username
    if request.method == 'POST':
        form=NewRatingForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.coffee_id = coffee_id
            rate.user = request.user
            rate.brew_method = ''
            rate.rating = ''
            rate.save()
            return redirect(
                'user_coffees',
                username=request.user
            )
    else:
        form=NewRatingForm()
    return render(
        request,
        'add_rating.html',
        {'username':request.user, 'coffee':coffee_id, 'form': form}
    )