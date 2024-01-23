from django.contrib import admin

from .models import PetServiceCategory, PetService, PetRequestService, PetServiceTracker

admin.site.register(PetServiceCategory)
admin.site.register(PetService)
admin.site.register(PetRequestService)
admin.site.register(PetServiceTracker)