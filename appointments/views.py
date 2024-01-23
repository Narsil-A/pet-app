
import datetime
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .forms import AppointmentForm, SlotCreationForm
from services.models import PetRequestService
from pets.models import Pet
from userprofile.models import Notification, User
from .models import Appointment, AppointmentSlot, book_slot, is_slot_available, get_available_slots


@login_required
def schedule_appointment_view(request, service_id):
    service_request = get_object_or_404(PetRequestService, id=service_id)
    user = request.user

    available_slots = []

    if request.method == 'POST':
        appointment_form = AppointmentForm(request.POST, user=user, service_request=service_request)

        if appointment_form.is_valid():
            # No need to get 'selected_slot_id' from request.POST again, use 'form.cleaned_data'
            selected_slot_id = appointment_form.cleaned_data['slot'].id
            if is_slot_available(selected_slot_id):
                # Now you can directly use the 'slot' from 'appointment_form.cleaned_data'
                appointment = appointment_form.save(commit=False)
                appointment.service = service_request
                appointment.petowner = user
                # appointment.slot is already set by the form, no need to fetch and set it again
                appointment.save()
                book_slot(selected_slot_id)
                return redirect('services:payment')
            else:
                # Inform user the slot is no longer available
                messages.error(request, "Selected slot is no longer available.")
    else:
        appointment_form = AppointmentForm(user=user, service_request=service_request)  

        
    context = {
        'form': appointment_form,
        'available_slots': available_slots,  
        'service': service_request,
    }

    return render(request, 'appointments/schedule_appointment.html', context)



@login_required
def available_slots(request):
    selected_date = request.GET.get('date')
    service_id = request.GET.get('service_id', None)

    # Ensure selected_date is a string in the correct format
    if selected_date:
        try:
            # Attempt to convert selected_date to a date object and back to a string
            # This is to validate that selected_date is in the correct format
            valid_date = datetime.date.fromisoformat(selected_date).isoformat()
            slots = get_available_slots(valid_date, service_id)
        except ValueError:
            # Handle the case where selected_date is not in the correct format
            return JsonResponse({'error': 'Invalid date format'}, status=400)
    else:
        return JsonResponse({'error': 'No date provided'}, status=400)

    slots_data = [
        {
            "id": slot.id,
            "start_time": f"{slot.date} {slot.start_time.strftime('%H:%M')}",
            "end_time": f"{slot.date} {slot.end_time.strftime('%H:%M')}"
        } 
        for slot in slots
    ]
    print("Selected Date:", selected_date, type(selected_date))
    return JsonResponse(slots_data, safe=False)





@login_required 
def create_slot_view(request):
    if request.method == 'POST':
        form = SlotCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:dashboard')  
    else:
        form = SlotCreationForm()

    return render(request, 'appointments/create_slot.html', {'form': form})



@login_required
def view_appointments(request):
    user = request.user
    if user.is_vetstaff:
        appointments = Appointment.objects.select_related('petowner').all()
    else:
        appointments = Appointment.objects.filter(
            petowner=request.user
        ).select_related('slot').order_by('slot__date')

    return render(request, 'appointments/view_appointments.html', {'appointments': appointments})
