from django import forms
from .models import dim_coffee

class NewCoffeeForm(forms.ModelForm):
    class Meta:
        model = dim_coffee
        fields = ['name', 'roaster']