from django import forms
from django.db.models import query

from .models import *

###
# RATE COFFEE FORMS
###

rating_choices = [
    ('', 'Select a Rating'),
    (1, 'No'),
    (2, 'Tolerable'),
    (3, 'Good'),
    (4, 'Like'),
    (5, 'Love')
    ]

class roasterForm(forms.ModelForm):

    class Meta:
        model = dim_roaster
        fields = ['name']

    name = forms.ModelChoiceField(
        empty_label="Find a Roaster",
        label="",
        to_field_name="name",
        widget=forms.Select(
            attrs={'class': 'custom-select custom-select-md'}), 
        queryset=dim_roaster.objects.all())


class coffeeForm(forms.ModelForm):

    class Meta:
        model = ratings
        fields = ['coffee']

    def __init__(self, *args, **kwargs):
        select_roaster = kwargs.pop('roaster', None)
        print(select_roaster)
        queryset = dim_roaster.objects.get(name=select_roaster)
        print(queryset)
        if select_roaster:
            queryset = queryset.coffees.all()
            print(queryset)
        super(coffeeForm, self).__init__(*args,**kwargs)
        self.fields['coffee'].queryset = queryset
        self.fields['coffee'].label = ""


    
class RatingForm3(forms.ModelForm):
    class Meta:
        model = ratings
        fields = ['brew_method']
        error_messages = {
            'brew_method': {
                'required': "Please pick a brew method.",
            },
        }


class RatingForm5(forms.ModelForm):
    class Meta:
        model = ratings
        fields = ['rating', 'reaction', 'rating_date']

    rating=forms.ChoiceField(
        choices=rating_choices,
        label="",
        error_messages={'required': 'Please give it a rating.'},
        required=True
    )

    reaction = forms.CharField(
        label = 'Write your thoughts',
        required=False)


###
# CREATE COFFEE FORMS
###

class createCoffeeForm1(forms.ModelForm):
    class Meta:
        model=dim_coffee
        fields=['roaster', 'name',]
        error_messages = {
            'roaster': {
                'required': "Please pick a roaster or create a new one.",
            },
            'name': {
                'required': "Please give us a name for this coffee.",
            }
        }

class createCoffeeForm2(forms.ModelForm):
    class Meta:
        model=dim_coffee
        fields=['country','farmer','elevation','process']
        error_messages = {
            'country': {
                'required': "Which country are these beans from? If a blend, choose 'Blend'.",
            },
            'process': {
                'required': "Please pick how the beans were processed.",
            }
        }


class createVarietalsForm(forms.ModelForm):

    class Meta:
        model=dim_coffee
        fields=['varietals']

    varietals = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={"class":"myClass"}), 
        queryset=dim_varietal.objects.all())

class createNotesForm(forms.ModelForm):

    class Meta:
        model=dim_coffee
        fields=['roaster_notes']

    roaster_notes = forms.ModelMultipleChoiceField(
        error_messages={'required': 'Please add the tasting notes from the roaster.'},
        widget=forms.SelectMultiple(
            attrs={"class":"myClass"}), 
        queryset=dim_notes.objects.all())