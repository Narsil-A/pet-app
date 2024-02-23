# appointments/forms.py
from django import forms
from django.forms.widgets import DateInput, TimeInput
from .models import Appointment, AppointmentSlot
from pets.models import Pet
from userprofile.models import User
from services.models import PetRequestService



class AppointmentForm(forms.ModelForm):
    slot = forms.ModelChoiceField(queryset=AppointmentSlot.objects.none(), required=True)

    class Meta:
        model = Appointment
        fields = ['pet_request_service', 'slot', 'notes']  

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        service_request = kwargs.pop('service_request', None)
        super(AppointmentForm, self).__init__(*args, **kwargs)

        if user:
            # Filter the pet_request_service queryset to only include services requested by this user
            self.fields['pet_request_service'].queryset = PetRequestService.objects.filter(petowner=user)

            # If a specific service request is provided, set it as the initial value and filter slots accordingly
            if service_request:
                self.fields['pet_request_service'].initial = service_request
                self.fields['slot'].queryset = AppointmentSlot.objects.filter(
                    service_type=service_request.service, is_booked=False)
                





class SlotCreationForm(forms.ModelForm):
    class Meta:
        model = AppointmentSlot
        fields = ['date', 'start_time', 'end_time', 'vet_staff', 'service_type']
        widgets = {
            'date': DateInput(attrs={'type': 'date', 'class': 'mt-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-blue-300'}),
            'start_time': TimeInput(attrs={'type': 'time', 'class': 'mt-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-blue-300'}),
            'end_time': TimeInput(attrs={'type': 'time', 'class': 'mt-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-blue-300'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SlotCreationForm, self).__init__(*args, **kwargs)
        if user and user.is_vetstaff:
            self.fields['vet_staff'].queryset = User.objects.filter(is_vetstaff=True)


