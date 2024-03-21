
from django import forms
from django.forms import Textarea
from pets.models import Pet
from .models import PetService, PetServiceTracker, PetRequestService, PetServiceCategory





class PetServiceCategoryForm(forms.ModelForm):
    class Meta:
        model = PetServiceCategory
        fields = ['name']
        labels = {
            'name': 'Service Category',
        }
        help_texts = {
            'name': 'Select a category for the pet service.',
        }

class PetServicesForm(forms.ModelForm):
    class Meta:
        model = PetService
        fields = ['category', 'name', 'description', 'cost', 'duration']


class PetRequestServicesForm(forms.ModelForm):
    class Meta:
        model = PetRequestService
        fields = ['service', 'pet'] 
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  
        super(PetRequestServicesForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['pet'].queryset = Pet.objects.filter(petowner=user)

class PetServiceTrackerForm(forms.ModelForm):
    class Meta:
        model = PetServiceTracker
        fields = '__all__'


class PetServiceTrackerUpdateForm(forms.ModelForm):
    class Meta:
        model = PetServiceTracker
        fields = ['status', 'notes']
        widgets = {
            'notes': Textarea(attrs={
                'class': 'shadow appearance-none border rounded w-full py-1 px-2 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'rows': 1, 
            }),
        }