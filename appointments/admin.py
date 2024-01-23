from django.contrib import admin
from .models import Appointment,  AppointmentSlot

admin.site.register(Appointment)
admin.site.register(AppointmentSlot)