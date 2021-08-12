from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from coffees.models import ratings, dim_coffee
from django.contrib.auth.decorators import login_required

#from django.utils.timezone import datetime
#from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(
        request,
        'home.html'
    )

@login_required
def user_home(request):
    #active_user = get_object_or_404(User, username = username)
    return render(
        request,
        'user_home.html',
        {'username':request.user}
    )

@login_required
def user_coffees(request):
    # active_user = get_object_or_404(User, username = username)
    coffees = dim_coffee.objects.all() #TODO FILTER FOR THE USER's COFFEES
    return render(
        request,
        'user_coffees.html',
        {'user':request.user, 'coffees':coffees}
    )

@login_required
def user_profile(request):
    # active_user = get_object_or_404(User, username = username)
    return render(
        request,
        'user_profile.html',
        {'username':request.user}
    )

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            base_url = '^user/(?P<username>[\w.@+-]+)/$' 
            user_name =  user.username 
            return redirect(base_url, {'username':user_name})
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})