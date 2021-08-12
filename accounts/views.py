from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm

#from django.utils.timezone import datetime
#from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(
        request,
        'home.html'
    )

def user_home(request, username):
    #active_user = get_object_or_404(User, username = username)
    return render(
        request,
        'user_home.html',
        {'username':username}
    )

def user_profile(request, username):
    active_user = get_object_or_404(User, username = username)
    return render(
        request,
        'user_profile.html',
        {'username':active_user.username}
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

def login(request):
    return render(request, 'user_home.html')

#TODO
def reset_password(request):
    return render(request, 'user_home.html')

def change_password(request):
    return render(request, 'user_home.html')