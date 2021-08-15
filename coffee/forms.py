from django import forms
from .models import *

# roasters = dim_coffee.objects.values_list('roaster', flat = True).distinct()
# roaster_choices = zip(roasters, roasters)
# roasters = dim_coffee.objects.values_list('roaster', flat = True).distinct()
# roaster_choices = zip(roasters, roasters)

class RatingForm1(forms.Form):
    name = forms.ModelChoiceField(
        empty_label=None,
        to_field_name="name",
        widget=forms.Select(), 
        queryset=dim_roaster.objects.none())
    class Meta:
        model = dim_roaster
        fields = ['name']
        # labels = None
        # widgets = forms.Select()
        # queryset = dim_roaster.objects.none()

    def __init__(self, *args, **kwargs):
        super(RatingForm1, self).__init__(*args,**kwargs)
        self.fields['name'].queryset = dim_roaster.objects.all()

    
class RatingForm2(forms.ModelForm):
 
    class Meta:
        model = dim_coffee
        fields = ['name']

    def __init__(self, *args, **kwargs):
        select_roaster = kwargs.pop('step0_form_field', None)

        queryset = dim_roaster.objects.get(name=select_roaster)
        if select_roaster:
            queryset = queryset.coffees.all()

        names = queryset.values_list('name', flat = True).distinct()
        name_choices = zip(names, names)

        super(RatingForm2, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.ModelChoiceField(
            queryset=queryset,
            widget = forms.Select(
                choices = name_choices,
                attrs={'class':'form-control'}
                )
        )

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