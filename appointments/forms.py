# appointments/forms.py
from django import forms
from .models import Appointment, AppointmentSlot
from pets.models import Pet
from userprofile.models import User
from services.models import PetRequestService



class AppointmentForm(forms.ModelForm):
    slot = forms.ModelChoiceField(queryset=AppointmentSlot.objects.none(), required=True)

    class Meta:
        model = Appointment
        fields = ['pet', 'pet_request_service', 'slot', 'notes']  # Removed the extra space after 'pet_request_service'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        service_request = kwargs.pop('service_request', None)
        super(AppointmentForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['pet'].queryset = Pet.objects.filter(petowner=user)

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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SlotCreationForm, self).__init__(*args, **kwargs)

        # Assuming 'is_vetstaff' is a boolean field in the User model
        if user and user.is_vetstaff:
            self.fields['vet_staff'].queryset = User.objects.filter(is_vetstaff=True)

