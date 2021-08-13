from django import forms
from .models import dim_coffee, ratings

class RatingForm1(forms.ModelForm):
    roaster_choices = dim_coffee.objects.order_by('roaster').values_list('roaster', flat=True)
    
    class Meta:
        model = dim_coffee
        fields = ['name', 'roaster']

class RatingForm2(forms.ModelForm):
    class Meta:
        model = ratings
        fields = ['brew_method', 'rating', 'tasting_notes']