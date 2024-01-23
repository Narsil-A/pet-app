import datetime
from .models import is_slot_overlapping, AppointmentSlot




def generate_slots(start_date, end_date, working_hours, slot_duration, vet_staff_id):
    # Assume working_hours is a dict like {'start': time(9, 0), 'end': time(17, 0)}
    # slot_duration in minutes, e.g., 30
    slot_length = datetime.timedelta(minutes=slot_duration)
    date = start_date

    while date <= end_date:
        current_time = datetime.datetime.combine(date, working_hours['start'])
        end_working_time = datetime.datetime.combine(date, working_hours['end'])

        while current_time + slot_length <= end_working_time:
            end_time = current_time + slot_length
            if not is_slot_overlapping(date, current_time.time(), end_time.time(), vet_staff_id):
                AppointmentSlot.objects.create(
                    date=date,
                    start_time=current_time.time(),
                    end_time=end_time.time(),
                    vet_staff_id=vet_staff_id
                )
            current_time += slot_length

        date += datetime.timedelta(days=1)
