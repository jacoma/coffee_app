import re
from django.utils.timezone import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from coffees.models import ratings, User, dim_coffee
from coffees.forms import *
from django.contrib.auth.decorators import login_required
from formtools.wizard.views import SessionWizardView
from django.utils.decorators import method_decorator

FORMS = [
    ("roaster", RatingForm1),
    ("coffee", RatingForm2),
    ("brew", RatingForm3),
    ("notes", RatingForm4),
    ("rate", RatingForm5)
]

TEMPLATES = {
    "roaster": "rating_roaster.html",
    "coffee": "rating_coffee.html",
    "brew": "rating_brew.html",
    "notes": "rating_notes.html",
    "rate": "rating_rate.html"
}

@method_decorator(login_required, name='dispatch')
class RatingWizard(SessionWizardView):
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def get_form_kwargs(self, step=None):
        kwargs = {}
        if step == 'coffee':
            step0_form_field = self.get_cleaned_data_for_step('roaster')['roaster']
            kwargs.update({'step0_form_field': step0_form_field})
        return kwargs 
    
    def done(self, form_list, **kwargs):
        # do_something_with_the_form_data(form_list)
        return redirect('home')
        # return render(self.request, 'done.html', {
        #     'form_data': [form.cleaned_data for form in form_list],
        # })

# def do_something_with_the_form_data(form_list):
#     """
#     Do something, such as sending mail
#     """
#     form_data = [form.cleaned_data for form in form_list]

#     print('#####')
#     print('Subject: %s' % form_data[0]['subject'])
#     print('Sender: %s' % form_data[0]['sender'])
#     print('Message: %s' % form_data[1]['message'])
#     print('#####')

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

# @login_required
# def add_rating(request):
#     # coffees = dim_coffee.objects.all()
#     if request.method == 'POST':
#         form=RatingForm2(request.POST)
#         if form.is_valid():
#             rate = form.save(commit=False)
#             # rate.coffee_id
#             # rate.user = request.user
#             # rate.brew_method = ''
#             # rate.rating = ''
#             # rate.roaster
                #rate.last_updated = timezone.now()
#             rate.save()
#             return redirect(
#                 'user_coffees'
#             )
#     else:
#         form=RatingForm2()
#     return render(
#         request,
#         'add_rating.html',
#         {'form': form}
#     )