from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from coffee.models import ratings, dim_coffee
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.db.models import Count


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        context = ratings.objects.filter(user_id=request.user)
        num_ratings = context.count()
        num_coffees = context.values('coffee__coffee_id').distinct().count()
        num_roasters = context.values('coffee__roaster__roaster_id').distinct().count()
        pie_qs = context.values('coffee__country__name').annotate(count=Count('coffee__country__name'))
        base_url = 'user/{username}/'.format(username=request.user.username)
        if request.method=='POST':
            if request.POST.get('my_coffee'):
                return redirect(reverse('user_coffees'))
            elif request.POST.get('rate_coffee'):
                return redirect(reverse('select_roaster'))
        return render(
            request, 
            'index.html', 
            {
                'num_ratings':num_ratings, 
                'num_coffees':num_coffees, 
                'num_roasters':num_roasters,
                'pie_qs':pie_qs
                })
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

@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email', )
    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user