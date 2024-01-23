
from django import forms
from .models import PetMedicalVisit
from django.contrib.auth import get_user_model

User = get_user_model()



class PetMedicalVisitForm(forms.ModelForm):
    class Meta:
        model = PetMedicalVisit
        fields = ['pet', 'date_of_visit', 'symptoms', 'diagnosis', 'treatment', 'notes', 'vet_staff']

    def __init__(self, *args, **kwargs):
        super(PetMedicalVisitForm, self).__init__(*args, **kwargs)
        self.fields['vet_staff'].queryset = User.objects.filter(is_vetstaff=True)