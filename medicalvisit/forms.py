from django.forms.widgets import DateInput
from django import forms
from .models import PetMedicalVisit
from pets.models import Pet
from django.contrib.auth import get_user_model

User = get_user_model()



class PetMedicalVisitForm(forms.ModelForm):
    class Meta:
        model = PetMedicalVisit
        fields = ['pet', 'date_of_visit', 'symptoms', 'diagnosis', 'treatment', 'notes', 'vet_staff']
        widgets = {
            'date_of_visit': DateInput(attrs={'type': 'date', 'class': 'mt-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-blue-300'}),
            }

    def __init__(self, *args, **kwargs):
        pet_owner = kwargs.pop('petowner', None)
        super(PetMedicalVisitForm, self).__init__(*args, **kwargs)

        if pet_owner is not None:
            self.fields['pet'].queryset = Pet.objects.filter(petowner=pet_owner)

        self.fields['vet_staff'].queryset = User.objects.filter(is_vetstaff=True)