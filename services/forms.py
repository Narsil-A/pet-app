
from django import forms
from pets.models import Pet
from .models import PetService, PetServiceTracker, PetRequestService



class PetServicesForm(forms.ModelForm):
    class Meta:
        model = PetService
        fields = ['category', 'name', 'description', 'cost', 'duration']


class PetRequestServicesForm(forms.ModelForm):
    class Meta:
        model = PetRequestService
        fields = ['service', 'pet'] 
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Correctly extract the user
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