from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from pets.models import Pet





class User(AbstractUser):

    
    is_vetstaff = models.BooleanField(default=False)
    is_petowner = models.BooleanField(default=False)
    # for both types of user
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Address")


class VetStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    position = models.CharField(max_length=100, verbose_name="Position in the medical center vet")
    profession = models.CharField(max_length=100, verbose_name="Profession")
    degrees = models.CharField(max_length=200, verbose_name="Degrees/Certifications")

    class Meta:
        ordering = ['user__username']

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.position})"


class PetOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    description = models.TextField(blank=True, null=True)
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