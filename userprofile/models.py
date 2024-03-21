from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from pets.models import Pet
from phonenumber_field.modelfields import PhoneNumberField






class User(AbstractUser):
    
    COUNTRY_CHOICES = [
    ('US', 'United States'),
    ('CA', 'Canada'),
    ('GB', 'United Kingdom'),
   
]
    is_vetstaff = models.BooleanField(default=False)
    is_petowner = models.BooleanField(default=False)
    # for both types of user
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Address")
    state = models.CharField(max_length=255, blank=True, null=True, verbose_name="State")
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, blank=True, null=True, verbose_name="Country")
    city = models.CharField(max_length=255, blank=True, null=True, verbose_name="Zip Code")
    zip_code = models.CharField(max_length=255, blank=True, null=True, verbose_name="state")
    phone_number = PhoneNumberField(blank=True, null=True)
    


class VetStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    position = models.CharField(max_length=100, blank=True, null=True, verbose_name="Position in the medical center vet")
    image = models.ImageField(upload_to='pet_app/', blank=True, null=True)

    class Meta:
        ordering = ['user__username']

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.position})"


class PetOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='pet_app/', blank=True, null=True)
    selected_services = models.ManyToManyField('services.PetService', related_name='petowner', blank=True)
    stripe_checkout_id = models.CharField(max_length=500, blank=True, null=True, verbose_name="Stripe Checkout Session ID")
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="Stripe Customer ID") 

    class Meta:
        ordering = ['user__username']

    def __str__(self):
        return f"{self.user.get_full_name()}"
    
    @property
    def pets(self):
        return Pet.objects.filter(petowner=self.user)

class Notification(models.Model):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.username} - Read: {self.read}"