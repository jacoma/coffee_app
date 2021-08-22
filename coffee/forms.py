from django import forms
from django.db.models import query

from .models import *

###
# RATE COFFEE FORMS
###

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

# class roasterForm(forms.ModelForm):
#     name = forms.ModelChoiceField(
#         empty_label="Find a Roaster",
#         label="",
#         to_field_name="name",
#         widget=forms.Select(
#             attrs={'class': 'custom-select custom-select-md'}), 
#         queryset=dim_roaster.objects.all())

#     class Meta:
#         model = dim_roaster
#         fields = ['name']

    # def __init__(self, *args, **kwargs):
    #     roasters=[]
    #     for k in dim_roaster.objects.values('roaster_id', 'name'):
    #         a = (k['roaster_id'], k['name'])
    #         roasters.append(a)
    #     super(roasterForm, self).__init__(*args, **kwargs)
    #     self.fields['name'].choices = roasters


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
        fields = ['rating', 'reaction']

    rating=forms.ModelChoiceField(
        queryset=ratings.objects.all(),
        empty_label="What did you think?",
        label="",
        to_field_name="rating",
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