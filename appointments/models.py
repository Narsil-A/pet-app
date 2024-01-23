import logging
from django.db import transaction
from django.db import models
from pets.models import Pet
from userprofile.models import User
from services.models import PetRequestService, PetService

logger = logging.getLogger(__name__)

class AppointmentSlot(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    vet_staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    service_type = models.ForeignKey(PetService, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.date} {self.start_time}-{self.end_time}"
    
from datetime import datetime

def get_available_slots(date, service_id=None):
    logger.debug(f"get_available_slots called with date: {date}, service_id: {service_id}")
    # Check if the date argument is a string and convert it to a datetime.date object
    if isinstance(date, str):
        try:
            date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            print("Invalid date format. Date should be in 'YYYY-MM-DD' format.")
            return AppointmentSlot.objects.none()
    
    # If the date is already a datetime.date object, use it directly in the query
    query = AppointmentSlot.objects.filter(date=date, is_booked=False)
    if service_id is not None:
        query = query.filter(service_type_id=service_id)

    return query

    
def is_slot_overlapping(date, start_time, end_time, vet_staff_id):
    overlapping_slots = AppointmentSlot.objects.filter(
        date=date,
        vet_staff_id=vet_staff_id,
        end_time__gt=start_time,  
        start_time__lt=end_time   
    ).exists()

    return overlapping_slots


def is_slot_available(slot_id):
    return not AppointmentSlot.objects.filter(id=slot_id, is_booked=True).exists()

def book_slot(slot_id):
    with transaction.atomic():
        slot = AppointmentSlot.objects.select_for_update().get(id=slot_id)
        if slot.is_booked:
            raise ValueError("Slot is already booked")
        slot.is_booked = True
        slot.save()


class Appointment(models.Model):
    petowner = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='appointments')
    pet_request_service = models.ForeignKey(PetRequestService, on_delete=models.PROTECT, related_name='appointments')
    slot = models.ForeignKey(AppointmentSlot, on_delete=models.CASCADE, related_name='appointments')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Appointment for {self.pet.name} - {self.pet_request_service } on {self.slot.date} {self.slot.start_time}-{self.slot.end_time}"

