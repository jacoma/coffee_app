import re
from django.utils.timezone import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from coffees.models import ratings, User, dim_coffee
from coffees.forms import RatingForm1, RatingForm2
from django.contrib.auth.decorators import login_required
from formtools.wizard.views import SessionWizardView

class RatingWizard(SessionWizardView):
    template_name = 'ratings.html'
    form_list = [RatingForm1, RatingForm2]
    
    def done(self, form_list, **kwargs):
        return render(self.request, 'done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })

# Create your views here.
@login_required
def add_coffee(request):
    if request.method == 'POST':
        form=RatingForm1(request.POST)
        if form.is_valid():
            coffee = form.save(commit=False)
            coffee.name = ''
            coffee.roaster = ''
            coffee.save()
            return redirect(
                'user_coffees'
            )
    else:
        form=RatingForm1()
    return render(
        request,
        'add_coffee.html',
        {'form': form}
    )

@login_required
def add_rating(request):
    # coffees = dim_coffee.objects.all()
    if request.method == 'POST':
        form=RatingForm2(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            # rate.coffee_id
            # rate.user = request.user
            # rate.brew_method = ''
            # rate.rating = ''
            # rate.roaster
            rate.save()
            return redirect(
                'user_coffees'
            )
    else:
        form=RatingForm2()
    return render(
        request,
        'add_rating.html',
        {'form': form}
    )