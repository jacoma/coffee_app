from django.forms.models import fields_for_model
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from coffee.models import *
from coffee.forms import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import FormView, CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

##
# USER RATINGS
##

@method_decorator(login_required, name='dispatch')
class coffeeList(LoginRequiredMixin, ListView):
    template_name = "ratings_list.html"
    context_object_name = 'coffees'
    model = ratings

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['coffees'] = context['coffees'].filter(user_id=self.request.user)

        return context

##
# CHANGE RATINGS
##
@method_decorator(login_required, name='dispatch')
class updateRating(UpdateView):
    model = ratings
    fields = ['coffee', 'brew_method', 'rating', 'reaction']
    template_name = 'update.html'
    success_url = reverse_lazy('user_coffees')

@method_decorator(login_required, name='dispatch')
class deleteRating(DeleteView):
    model = ratings
    context_object_name = 'rating'
    template_name = 'delete.html'
    success_url = reverse_lazy('user_coffees')



##
# RATE COFFEE
##

@method_decorator(login_required, name='dispatch')
class selectRoaster(FormView):
    """ A view to start the 'Rate Coffee' process; user should pick Roaster first."""
    template_name = "add_rating.html"
    form_class = roasterForm
    success_url=reverse_lazy('select_coffee')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()

        """ If 'Add Coffee' clicked, then capture roaster and direct to 'Add Coffee' URL"""
        if request.POST.get('add_roaster'):
            self.request.session['redirect_url']='select_brew'
            return redirect(reverse('add_roaster'))
        ### If form is valid, capture the roaster and coffee names for the final form submit
        else:
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    def form_valid(self, form):
        """
        Takes the POST data from the Roaster Form and stores it in the session
        """
        form.save(commit = False)
        self.request.session["roaster"] = form.cleaned_data["name"].roaster_id
        return super(selectRoaster, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """ Adds to the context the roaster for the 'Add Coffee' button; also sets form-step to 1 """
        context = super().get_context_data(**kwargs)
        context["rate_roasterStep"] = True

        return context

@method_decorator(login_required, name='dispatch')
class selectCoffee(FormView):
    """ A view to start the 'Rate Coffee' process """
    template_name = "add_rating.html"
    form_class = coffeeForm
    success_url=reverse_lazy('select_brew')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()

        """ If 'Add Coffee' clicked, then capture roaster and direct to 'Add Coffee' URL"""
        if request.POST.get('add_coffee'):
            print('add coffee button value: ', request.POST.get('add_coffee'))
            ### Set session variable to selected roaster in previous step.
            self.request.session['create_coffee_roasterId']=request.POST.get('add_coffee')
            ### Set session variable to next step after coffee is created.
            self.request.session['redirect_url']='select_brew'
            return redirect(reverse('add_coffee1'))
        ### If form is valid, capture the roaster and coffee names for the final form submit
        else:
            if form.is_valid():
                self.request.session["rate_coffeeId"]=form.cleaned_data['coffee'].coffee_id

                # DELETE 'roaster' SESSION VARIABLE SET IN THE 'select_roaster' STAGE
                del self.request.session['roaster']

                return self.form_valid(form)
            else:
                return self.form_invalid(form)
    
    def get_form_kwargs(self, step=None):
        """ Use roaster value saved from previous form to filter the modelform instance """
        kwargs = super(selectCoffee, self).get_form_kwargs()
        kwargs.update({'roaster': self.request.session["roaster"]})
        return kwargs

    def get_context_data(self, **kwargs):
        """ Adds to the context the roaster for the 'Add Coffee' button; also sets form-step to 1 """
        context = super().get_context_data(**kwargs)
        context['roaster'] = self.request.session["roaster"]
        context['rate_coffeeStep'] = True
        return context

@method_decorator(login_required, name='dispatch')
class selectBrew(FormView):
    """ A view to start the 'Rate Coffee' process """
    template_name = "add_rating.html"
    form_class = RatingForm3
    success_url=reverse_lazy('select_rating')

    def form_valid(self, form):
        self.request.session["rate_brew"] = form.cleaned_data['brew_method']
        return super(selectBrew, self).form_valid(form)

    def get_context_data(self, **kwargs):
        if self.request.session.get('create_coffee_roaster', None):
            print("Return from Creating Coffee")

        """ Adds to the context the roaster for the 'Add Coffee' button; also sets form-step to 1 """
        context = super().get_context_data(**kwargs)
        context["rate_brewStep"] = True
        return context

@method_decorator(login_required, name='dispatch')
class selectRating(FormView):
    """ A view to start the 'Rate Coffee' process """
    template_name = "add_rating.html"
    form_class = RatingForm5
    success_url=reverse_lazy('user_coffees')

    def form_valid(self, form):
        coffee_x = dim_coffee.objects.get(coffee_id = self.request.session["rate_coffeeId"])
        rate = ratings(
            coffee = coffee_x,
            brew_method = self.request.session["rate_brew"],
            reaction = form.cleaned_data['reaction'],
            rating = form.cleaned_data['rating'],
            rating_date = form.cleaned_data['rating_date'],
            user_id=self.request.user
        )

        rate.save()

        # DELETE SESSION VARIABLES
        del self.request.session["rate_brew"]
        if self.request.session.get('rate_coffee', None):
            del self.request.session["rate_coffee"]

        return super(selectRating, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """ Adds to the context the roaster for the 'Add Coffee' button; also sets form-step to 1 """
        context = super().get_context_data(**kwargs)
        context["rate_finalStep"] = True
        return context

##
# CREATE ROASTER
##
@method_decorator(login_required, name='dispatch')
class roasterCreate(FormView):
    template_name = "add_coffee.html"
    form_class = createRoasterForm
    success_url=reverse_lazy('add_coffee1')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()

        """ If 'Add Coffee' clicked, then capture roaster and direct to 'Add Coffee' URL"""
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save(commit=False)
        roaster = dim_roaster(
            name = form.cleaned_data['name']
        )
        roaster.save()
        self.request.session['create_coffee_roaster']=roaster.name
        self.request.session['create_coffee_roasterId']=roaster.roaster_id

        # DELETE SESSION VARIABLES

        # RETURN FORM_VALID
        return super(roasterCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """ Adds to the context the roaster for the 'Add Coffee' button; also sets form-step to 1 """
        context = super().get_context_data(**kwargs)
        context["add_roaster"] = True
        return context


##
# CREATE COFFEE
##
@method_decorator(login_required, name='dispatch')
class coffeeCreate1(FormView):
    # specify the model for create view
    template_name = "add_coffee.html"
    form_class = createCoffeeForm1 
    success_url=reverse_lazy('add_coffee2')

    def get_context_data(self, **kwargs):
        """ Adds to the context the roaster for the 'Add Coffee' button; also sets form-step to 1 """
        context = super().get_context_data(**kwargs)

        # IF CREATE_COFFEE_ROASTER EXISTS, ADD CONTEXT TO REMOVE "Add Roaster" BUTTON
        if self.request.session.get('create_coffee_roasterId', None):
            context['hasRoaster'] = True
        context["roasterStep"] = True
        
        return context

    def get_form_kwargs(self, step=None):
        kwargs = super(coffeeCreate1, self).get_form_kwargs()
        return kwargs

    def get_initial(self):
        # pre-populate form if someone goes back and forth between forms
        initial = super(coffeeCreate1, self).get_initial()
        initial = initial.copy()
        roaster = self.request.session.get('create_coffee_roasterId', None) 
        if roaster == None:
            return initial
        else:
            roaster = dim_roaster.objects.filter(roaster_id=self.request.session['create_coffee_roasterId']).values_list('roaster_id', flat=True)[0]
            initial['roaster'] = roaster
            return initial

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if request.POST.get('add_roaster'):
            self.request.session['add_roaster']=True
            return redirect(reverse('add_roaster'))
        ### If form is valid, capture the roaster and coffee names for the final form submit
        else:
            if form.is_valid():
                form.save(commit=False)
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    def form_valid(self, form):
        self.request.session['rate_coffee'] = form.cleaned_data['name']
        return super(coffeeCreate1, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class coffeeCreate2(FormView):
    template_name = "add_coffee.html"
    form_class = createCoffeeForm2
    success_url=reverse_lazy('add_coffee3')

    def get_context_data(self, **kwargs):
        """ Adds to the context the roaster for the 'Add Coffee' button; also sets form-step to 1 """
        context = super().get_context_data(**kwargs)
        context["createStep"] = 1
        return context

    def form_valid(self, form):
        form.save(commit=False)
        self.request.session['rate_elevation'] = form.cleaned_data['elevation']
        self.request.session['rate_farmer'] = form.cleaned_data['farmer']
        self.request.session['rate_process']= form.cleaned_data['process']
        self.request.session['rate_country']= form.cleaned_data['country'].country_code
        return super(coffeeCreate2, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class coffeeCreate3(FormView):
    template_name = "add_coffee.html"
    form_class=createVarietalsForm 
    success_url=reverse_lazy('add_coffee4')

    def form_valid(self, form):
        variety=form.cleaned_data['varietals'].values_list('varietal', flat=True).distinct()
        self.request.session['rate_varietals'] = list(variety)
        return super(coffeeCreate3, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """ Adds to the context the roaster for the 'Add Coffee' button; also sets form-step to 1 """
        context = super().get_context_data(**kwargs)
        context["varietalStep"] = 2
        return context

@method_decorator(login_required, name='dispatch')
class coffeeCreate4(FormView):
    template_name = "add_coffee.html"
    form_class = createNotesForm
    success_url=reverse_lazy('home')

    def get_context_data(self, **kwargs):
        """ Adds to the context the roaster for the 'Add Coffee' button; also sets form-step to 1 """
        context = super().get_context_data(**kwargs)
        context["noteStep"] = 3
        context['finalStep'] = 1
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            form.save(commit=False)

            # OBTAIN OBJECTS FOR FOREIGNKEY VARIABLES
            varietals_x=dim_varietal.objects.filter(varietal__in=self.request.session['rate_varietals'])
            roaster_x = dim_roaster.objects.get(roaster_id=self.request.session['create_coffee_roasterId'])
            country_x = countries.objects.get(country_code=self.request.session['rate_country'])
            notes_x = form.cleaned_data['roaster_notes']

            # CREATE NEW COFFEE OBJECT
            coffee=dim_coffee(
                roaster=roaster_x,
                name=self.request.session['rate_coffee'],
                country=country_x,
                elevation=self.request.session['rate_elevation'],
                farmer=self.request.session['rate_farmer'],
                process=self.request.session['rate_process'],
                )
            coffee.save()
            dim_coffee.objects.get(coffee_id=coffee.pk).roaster_notes.set(notes_x)
            coffee.varietals.set(varietals_x)
            
            # DELETE SESSION VARIABLES
            del self.request.session['rate_varietals']
            del self.request.session['create_coffee_roasterId']
            del self.request.session['rate_country']
            del self.request.session['rate_elevation']
            del self.request.session['rate_farmer']
            del self.request.session['rate_process']

            # SEND BACK TO RATING FLOW IF COMING FROM THERE (i.e. "redirect_url exists")
            if self.request.session.get('redirect_url', None):
                rate = ratings.objects.create(coffee=coffee, user_id=self.request.user)
                self.request.session["rating_id"]=rate.rating_id
                self.request.session["rate_coffeeId"]=coffee.coffee_id
                self.success_url=reverse_lazy(self.request.session['redirect_url'])
                
                # DELETE SESSION VARIABLES BUT KEEP 'rate_coffee' FOR THE FINAL RATING OBJECT
                del self.request.session['redirect_url']
                del self.request.session['rate_coffee']
                return self.form_valid(self)
            else:
                # IF NOT SENDING BACK TO RATING, DELETE 'rate_coffee'
                if self.request.session.get('rate_coffee', None):
                    del self.request.session['rate_coffee']
                return self.form_valid(form)
        else:
            return self.form_invalid(form)
        