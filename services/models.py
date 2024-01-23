from django.db import models
from userprofile.models import User
from pets.models import Pet


class PetServiceCategory(models.Model):
    DIAGNOSTIC = 'DIAG'
    IMAGING = 'IMG'
    VETERINARY = 'VET'
    GROOMING = 'GRO'

    CATEGORY_CHOICES = [
        (DIAGNOSTIC, 'Diagnostic'),
        (IMAGING, 'Imaging'),
        (VETERINARY, 'Veterinary Appointment'),
        (GROOMING, 'Grooming'),
    ]

    name = models.CharField(max_length=4, choices=CATEGORY_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()


class PetService(models.Model):
    category = models.ForeignKey(PetServiceCategory, on_delete=models.CASCADE, related_name='petservices')
    name = models.CharField(max_length=100, blank=True)  
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, help_text="Cost in dollars")
    duration = models.IntegerField(help_text="Duration in days")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_services', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name} - {self.category.get_name_display()}"

    

class PetRequestService(models.Model):
    petowner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, null=True, related_name='requests_services')
    service = models.ForeignKey(PetService, on_delete=models.CASCADE, null=True)
    paid = models.BooleanField(default=False, verbose_name="Paid Status")
    stripe_session_id = models.CharField(max_length=500, blank=True, null=True, verbose_name="Stripe Session ID")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service} for {self.pet.name}"

        
class PetServiceTracker(models.Model):
    REQUESTED = 'REQUESTED'
    CONFIRMED_PAID = 'CONFIRMED_PAID'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'
    

    STATUS_CHOICES = [
        (REQUESTED, 'Requested'),
        (CONFIRMED_PAID, 'Confirmed Paid'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=REQUESTED)
    requested_service = models.ForeignKey(PetRequestService, on_delete=models.CASCADE, null=True, related_name='service_updates')
    is_tracked = models.BooleanField(default=False)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='service_updates')
    notes = models.TextField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='tracked_services', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.requested_service.service.name} - {self.get_status_display()}"