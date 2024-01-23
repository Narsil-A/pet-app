# userprofile/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Notification, VetStaff, PetOwner

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'is_vetstaff', 'petowner',]

admin.site.register(User, CustomUserAdmin)
admin.site.register(Notification)
admin.site.register(VetStaff)
admin.site.register(PetOwner)

