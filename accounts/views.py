from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from .forms import SignUpForm
from coffee.models import *
from endpoints.ml.recommender import Recommendations
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        context = ratings.objects.filter(user_id=request.user)
        num_ratings = context.count()
        num_coffees = context.values('coffee__coffee_id').distinct().count()
        num_roasters = context.values('coffee__roaster__roaster_id').distinct().count()
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
                'num_roasters':num_roasters
                })
    else:
        return HttpResponseRedirect(
                reverse(signup)
            )

class ChartData(APIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = []

    def get(self, request, format=None):
        """
        Return counts per country for Chart.js pie chart
        """
        context = countries.objects.filter(coffees__ratings__user_id=request.user)
        pie_qs = context.values('region').order_by('region').annotate(
            num_country=Count('name'),
             num_coffees=Count('coffees__name'),
              num_ratings=Count('coffees__ratings__rating_id')
              )
        labels = pie_qs.values_list('region', flat = True).distinct()
        data = pie_qs.values_list('num_ratings', flat = True).distinct()
        my_context = {
            'labels': labels,
            'data': data
        }
        return Response(my_context)

class lineData(APIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = []

    def get(self, request, format=None):
        """
        Return counts per country for Chart.js pie chart
        """
        context = ratings.objects.filter(user_id=request.user)
        qs = context.values('rating_date').order_by('rating_date').annotate(num_ratings=Count('rating_id'))
        labels = qs.values_list('rating_date', flat = True).distinct()
        data = qs.values_list('num_ratings', flat = True).distinct()
        my_context = {
            'labels': labels,
            'data': data
        }
        return Response(my_context)

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

@method_decorator(login_required, name='dispatch')
class recsList(LoginRequiredMixin, ListView):
    template_name = "recs_list.html"
    context_object_name = 'recs'

    def get_queryset(self, **kwargs):
        recs = Recommendations()
        my_recs = recs.get_recs(self.request.user)

        return my_recs

@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email', )
    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user