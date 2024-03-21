
import datetime
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from pet_app.decorators import vetstaff_required
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
            selected_slot_id = appointment_form.cleaned_data.get('slot').id  # Retrieve slot ID from form data
            if is_slot_available(selected_slot_id):
                appointment = appointment_form.save(commit=False)
                appointment.service = service_request
                appointment.petowner = user
                appointment.save()
                book_slot(selected_slot_id)
                return redirect('services:payment')
            else:
                messages.error(request, "Selected slot is no longer available.")
    else:
        appointment_form = AppointmentForm(user=user, service_request=service_request)
        # If a GET request, initialize the slot queryset
        appointment_form.fields['slot'].queryset = AppointmentSlot.objects.filter(
            service_type=service_request.service, is_booked=False)
        available_slots = appointment_form.fields['slot'].queryset

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
            #valid_date = datetime.date.fromisoformat(selected_date).isoformat()
            slots = get_available_slots(service_id)
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
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, petowner=request.user)

    # Check if the appointment belongs to the logged-in user
    if appointment.petowner != request.user:
        messages.error(request, "You do not have permission to cancel this appointment.")
        return redirect('dashboard:dashboard')

    # Unbook the slot
    slot = appointment.slot
    slot.is_booked = False
    slot.save()

    # Delete or update the appointment as per your requirement

    appointment.delete()

    # For updating (e.g., setting a 'cancelled' flag):
    # appointment.save()

    messages.success(request, "Your appointment has been successfully cancelled.")
    return redirect('dashboard:dashboard') 



@login_required 
def create_slot_view(request):
    if request.method == 'POST':
        form = SlotCreationForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard:dashboard')  
    else:
        form = SlotCreationForm(user=request.user)

    return render(request, 'appointments/create_slot.html', {'form': form})



@vetstaff_required 
def slots_view(request):
    slots_appointments = AppointmentSlot.objects.all()

    return render(request, 'appointments/slots_appointments.html', {'slots_appointments': slots_appointments})


@vetstaff_required 
def delete_slots(request, appointmentslot_id):
    try:
        slot_appointment = AppointmentSlot.objects.get(id=appointmentslot_id)

        # Check if the slot is booked before deleting
        if slot_appointment.is_booked:
            slot_appointment.is_booked = False
            slot_appointment.save()  # Save the changes to the slot appointment

        slot_appointment.delete()  # Delete the slot appointment

        messages.success(request, "Appointment slot successfully deleted.")
    except AppointmentSlot.DoesNotExist:
        messages.error(request, "Appointment slot not found.")

    # Redirect to a view that lists all slots, or to another appropriate page
    return redirect('appointments:slots_view')  



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
