from django.shortcuts import render, get_object_or_404, redirect, reverse
from coffee.models import *
from coffee.forms import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import FormView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

##
# USER COFFEE
##

@method_decorator(login_required, name='dispatch')
class coffeeList(LoginRequiredMixin, ListView):
    template_name = "ratings_list.html"
    context_object_name = 'coffees'
    model = ratings

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['coffees'] = context['coffees'].filter(user_id=self.request.user)
        # context['count'] = context['tasks'].filter(complete=False).count()

        # search_input = self.request.GET.get('search-area') or ''
        # if search_input:
        #     context['tasks'] = context['tasks'].filter(
        #         title__contains=search_input)

        # context['search_input'] = search_input

        return context



##
# RATE COFFEE
##

@method_decorator(login_required, name='dispatch')
class selectRoaster(FormView):
    """ A view to start the 'Rate Coffee' process; user should pick Roaster first."""
    template_name = "add_rating.html"
    form_class = roasterForm

    def get_success_url(self):
        """ Overides the success url when the view is run """
        return reverse("select_coffee")

    def form_valid(self, form):
        """
        Takes the POST data from the Roaster Form and stores it in the session
        """
        self.request.session["name"] = form.cleaned_data["name"].name
        return super(selectRoaster, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class selectCoffee(FormView):
    """ A view to start the 'Rate Coffee' process """
    template_name = "add_rating.html"
    form_class = coffeeForm

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if request.POST.get('roaster'):
            self.request.session['create_coffee_roaster']=request.POST.get('roaster')
            return redirect(reverse('add_coffee1'))
        else:
            if form.is_valid():
                return self.form_valid(form)
               
            else:
                return self.form_invalid(form)
    
    def get_form_kwargs(self, step=None):
        kwargs = super(selectCoffee, self).get_form_kwargs()
        kwargs.update({'roaster': self.request.session["name"]})
        return kwargs

    def get_context_data(self, **kwargs):
        """ Adds to the context the Product objects categorized as trips """
        context = super().get_context_data(**kwargs)
        context["formStep"] = 1
        context['roaster'] = self.request.session["name"]
        return context

##
# CREATE ROASTER
##
class roasterCreate(CreateView):
    template_name = "add_coffee.html"
    model = dim_roaster
    fields = ['name']
    success_url='add_coffee1'


##
# CREATE COFFEE
##

class coffeeCreate1(CreateView):
    # specify the model for create view
    template_name = "add_coffee.html"
    model = dim_coffee
  
    # specify the fields to be displayed
    fields = ['roaster', 'name']

    def get_form_kwargs(self, step=None):
        kwargs = super(coffeeCreate1, self).get_form_kwargs()
        # kwargs.update({'roaster': self.request.session["name"]})
        return kwargs

    def get_initial(self):
        # pre-populate form if someone goes back and forth between forms
        initial = super(coffeeCreate1, self).get_initial()
        initial = initial.copy()
        roaster = self.request.session.get('create_coffee_roaster', None) 
        if roaster == None:
            return initial
        else:
            roaster = dim_roaster.objects.filter(name=self.request.session['create_coffee_roaster']).values_list('roaster_id', flat=True)[0]
            initial['roaster'] = roaster
            return initial

    def get_context_data(self, **kwargs):
        """ Adds to the context the Product objects categorized as trips """
        context = super().get_context_data(**kwargs)
        context["formStep"] = 0
        return context

    def get_success_url(self):
        """ Overides the success url when the view is run """
        return reverse("add_coffee2")

class coffeeCreate2(CreateView):
    # specify the model for create view
    template_name = "add_coffee.html"
    model = dim_coffee
  
    # specify the fields to be displayed
    fields = ['country', 'elevation', 'farmer', 'process']

    def get_success_url(self):
        """ Overides the success url when the view is run """
        return reverse("add_coffee3")

class coffeeCreate3(CreateView):
    # specify the model for create view
    template_name = "add_coffee.html"
    model = dim_coffee
  
    # specify the fields to be displayed
    fields = ['varietals']

    def get_success_url(self):
        """ Overides the success url when the view is run """
        return reverse("add_coffee4")

class coffeeCreate4(CreateView):
    # specify the model for create view
    template_name = "add_coffee.html"
    model = dim_coffee
  
    # specify the fields to be displayed
    fields = ['roaster_notes']

    def get_success_url(self):
        """ Overides the success url when the view is run """
        return reverse("home")