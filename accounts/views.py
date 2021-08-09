from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm

#from django.utils.timezone import datetime
#from django.http import HttpResponse

# Create your views here.
def user_home(request, username):
    active_user = get_object_or_404(SignUpForm, username = username)
    return render(
        request,
        'user_home.html',
        {'user':active_user}
    )

def signup(request):
    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            auth_login(request,user)
            return redirect('user_home')
    else:
        form=SignUpForm()
    return render(request, 'signup.html', {'form': form})



def login(request):
    return render(request, 'user_home.html')

#TODO
def logout(request):
    return render(request, 'user_home.html')

def signup(request):
    return render(request, 'user_home.html')

#TODO
def reset_password(request):
    return render(request, 'user_home.html')

def change_password(request):
    return render(request, 'user_home.html')