from django.db import models
from django.conf import settings
from pets.models import Pet
from userprofile.models import User




class PetMedicalVisit(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='medical_visits')
    vet_staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='recorded_visits')
    date_of_visit = models.DateTimeField()
    symptoms = models.TextField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Medical Visit for {self.pet.name} of the petowner {self.pet.petowner} on {self.date_of_visit.strftime('%Y-%m-%d')}"
