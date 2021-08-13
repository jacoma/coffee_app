from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from coffees.models import ratings, dim_coffee
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse 

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        # base_url = 'user/{username}/'.format(username=request.user.username)
        return render(request, 'user_home.html')
    else:
        return HttpResponseRedirect(
                reverse(signup)
            )

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect(home)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


# def user_home(request):
#     return render(request, 'user_home.html', {'username':request.user.username})

@login_required
def user_coffees(request):
    coffees = dim_coffee.objects.all() #TODO FILTER FOR THE USER's COFFEES
    return render(
        request,
        'user_coffees.html',
        {'coffees':coffees}
    )

@login_required
def user_profile(request):
    return render(
        request,
        'user_profile.html'
    )