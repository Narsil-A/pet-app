
from django import forms
from .models import Pet



class PetOwnerForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'species', 'breed', 'age', 'medical_history', 'image', 'gender', 'spayed_neutered']
        widgets = {
            'medical_history': forms.CheckboxSelectMultiple(),
            'breed': forms.Select(),  # Ensure this is a standard select field
        }

    def __init__(self, *args, **kwargs):
        super(PetOwnerForm, self).__init__(*args, **kwargs)
        # Initialize species choices
        self.fields['species'].choices = Pet.SPECIES_CHOICES
        # Initially, breed choices are empty since they depend on species selection
        self.fields['breed'].choices = []

        # If editing an existing instance, pre-populate breeds based on species
        if 'instance' in kwargs and kwargs['instance']:
            species = kwargs['instance'].species
            self.fields['breed'].choices = Pet.BREED_CHOICES_DICT.get(species, [])