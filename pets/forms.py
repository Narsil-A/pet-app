
from django import forms
from .models import Pet, WeightRecord, MedicalHistory



class PetOwnerForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'species', 'breed', 'age', 'medical_history', 'image', 'gender', 'spayed_neutered']
        widgets = {
            'medical_history': forms.CheckboxSelectMultiple(),
            'breed': forms.Select(),  
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


class WeightRecordPetInitialForm(forms.ModelForm):
    class Meta:
        model = WeightRecord
        fields = ['pet', 'weight', 'date', 'goal_weight', 'notes']  
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        pet = kwargs.pop('pet', None)
        super(WeightRecordPetInitialForm, self).__init__(*args, **kwargs)

        # Conditionally manipulate the 'pet' field if it exists
        if pet and 'pet' in self.fields:
            self.fields['pet'].queryset = Pet.objects.filter(id=pet.id)  # This sets the queryset to only include the specified pet, effectively "pre-selecting" it if the field is rendered
            self.fields['pet'].initial = pet  # Set initial value to the specific pet instance
            self.fields['pet'].widget = forms.HiddenInput()  # Hide the 'pet' field to not render it in the form

class WeightRecordPetForm(forms.ModelForm):
    class Meta:
        model = WeightRecord
        fields = ['pet', 'weight', 'date', 'notes']  # Ensure 'pet' is included if you intend to manipulate it
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        pet = kwargs.pop('pet', None)
        super(WeightRecordPetForm, self).__init__(*args, **kwargs)

        # Conditionally manipulate the 'pet' field if it exists
        if pet and 'pet' in self.fields:
            self.fields['pet'].queryset = Pet.objects.filter(id=pet.id)  # This sets the queryset to only include the specified pet, effectively "pre-selecting" it if the field is rendered
            self.fields['pet'].initial = pet  # Set initial value to the specific pet instance
            self.fields['pet'].widget = forms.HiddenInput()  # Hide the 'pet' field to not render it in the form

class GoalWeightForm(forms.ModelForm):
    class Meta:
        model = WeightRecord
        fields = ['goal_weight']


class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ['category']
        labels = {
            'category': 'Medical History Category',
        }
        help_texts = {
            'category': 'Select the appropriate category for the medical history record.',
        }
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
        }