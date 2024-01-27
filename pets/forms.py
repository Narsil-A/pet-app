
from django import forms
from .models import Pet, WeightRecord



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






class WeightRecordForm(forms.ModelForm):
    class Meta:
        model = WeightRecord
        fields = ['pet', 'weight', 'date', 'goal_weight', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract the user from the kwargs
        super(WeightRecordForm, self).__init__(*args, **kwargs)
        
        # Now we filter the 'pet' field's queryset to only include pets owned by the user
        if user is not None:
            self.fields['pet'].queryset = Pet.objects.filter(petowner=user)
