from django import forms

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


class RatingForm5(forms.ModelForm):
    class Meta:
        model = ratings
        fields = ['reaction', 'rating']


###
# CREATE COFFEE FORMS
###

class createCoffeeForm1(forms.ModelForm):
    class Meta:
        model=dim_coffee
        fields=['roaster', 'name',]

class createCoffeeForm2(forms.ModelForm):
    class Meta:
        model=dim_coffee
        fields=['country','farmer','elevation','process']

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
        widget=forms.SelectMultiple(
            attrs={"class":"myClass"}), 
        queryset=dim_notes.objects.all())