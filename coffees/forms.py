from django import forms
from .models import dim_coffee, ratings

class NewCoffeeForm(forms.ModelForm):
    class Meta:
        model = dim_coffee
        fields = ['name', 'roaster']

class NewRatingForm(forms.ModelForm):
    class Meta:
        model = ratings
        fields = ['brew_method', 'rating', 'tasting_notes']