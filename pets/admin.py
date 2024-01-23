from django.contrib import admin
from .models import Pet, MedicalHistory

admin.site.register(Pet)
admin.site.register(MedicalHistory)