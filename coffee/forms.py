from django import forms
from .models import *

class roasterForm(forms.ModelForm):
    name = forms.ModelChoiceField(
        empty_label="Find a Roaster",
        label="",
        to_field_name="name",
        widget=forms.Select(attrs={'class': 'custom-select custom-select-md'}), 
        queryset=dim_roaster.objects.all())

    class Meta:
        model = dim_roaster
        fields = ['name']
        # labels = None
        # widgets = forms.Select()
        # queryset = dim_roaster.objects.none()

    # def __init__(self, *args, **kwargs):
    #     super(RatingForm1, self).__init__(*args,**kwargs)
    #     self.fields['name'].queryset = dim_roaster.objects.all()


class coffeeForm(forms.ModelForm):
    name = forms.ModelChoiceField(
        empty_label="Find a Coffee",
        label="",
        to_field_name="name",
        widget=forms.Select(attrs={'class': 'custom-select custom-select-md'}), 
        queryset=dim_coffee.objects.all())
 
    class Meta:
        model = dim_coffee
        fields = ['name']

    def __init__(self, *args, **kwargs):
        select_roaster = kwargs.pop('roaster', None)
        queryset = dim_roaster.objects.get(name=select_roaster)
        if select_roaster:
            queryset = queryset.coffees.all()

        super(coffeeForm, self).__init__(*args,**kwargs)
        self.fields['name'].queryset = queryset

    
class RatingForm3(forms.ModelForm):
    class Meta:
        model = ratings
        fields = ['brew_method']

class RatingForm4(forms.ModelForm):
    class Meta:
        model = dim_coffee
        fields = ['roaster_notes']


class RatingForm5(forms.ModelForm):
    class Meta:
        model = ratings
        fields = ['rating']