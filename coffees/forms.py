from django import forms
from .models import dim_coffee, ratings

roasters = dim_coffee.objects.values_list('roaster', flat = True).distinct()
roaster_choices = zip(roasters, roasters)
roasters = dim_coffee.objects.values_list('roaster', flat = True).distinct()
roaster_choices = zip(roasters, roasters)

class RatingForm1(forms.ModelForm):
    class Meta:
        model = dim_coffee
        fields = ['roaster']
        labels = None
        widgets = {
            'roaster': forms.Select(choices=roaster_choices)
        }

    
class RatingForm2(forms.ModelForm):
 
    class Meta:
        model = dim_coffee
        fields = ['name']

    def __init__(self, *args, **kwargs):
        select_roaster = kwargs.pop('step0_form_field', None)

        queryset = dim_coffee.objects.all()
        if select_roaster:
            queryset = dim_coffee.objects.filter(roaster=select_roaster)

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
        
        
        # c_names = dim_coffee.objects.filter(roaster=self.select_roaster).values_list('name', flat = True).distinct()
        # new_choices = zip(c_names, c_names)
        # self.fields['name'].choices = [new_choices]

class RatingForm3(forms.ModelForm):
    class Meta:
        model = ratings
        fields = ['brew_method']

class RatingForm4(forms.ModelForm):
    class Meta:
        model = ratings
        fields = ['tasting_notes']


class RatingForm5(forms.ModelForm):
    class Meta:
        model = ratings
        fields = ['rating']