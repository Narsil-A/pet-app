from django.conf import settings
from django.db import models




class MedicalHistory(models.Model):
    VACCINATED = 'vaccinated'
    ALLERGY = 'allergy'
    SURGERY = 'surgery'
    NONE = 'none'
    OTHER = 'other'
    CATEGORY_CHOICES = [
        (VACCINATED, 'Vaccinated'),
        (ALLERGY, 'Allergy'),
        (SURGERY, 'Surgery'),
        (NONE, 'None'),
        (OTHER, 'Other'),
    ]

    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, unique=True)

    def __str__(self):
        return self.get_category_display()


class Pet(models.Model):
    DOG = 'dog'
    CAT = 'cat'
    BIRD = 'bird'
    OTHER = 'other'

    SPECIES_CHOICES = [
        (DOG, 'Dog'),
        (CAT, 'Cat'),
        (BIRD, 'Bird'),
        (OTHER, 'Other'),
    ]

    # Define breeds for each species
    LABRADOR = 'labrador'
    GERMAN_SHEPHERD = 'German Shepherd'
    POODLE = 'Poodle'
    PERSIAN = 'persian'
    MAINE_CONN = 'Maine Coon'
    SIAMESE = 'Siamese'
    PARROT = 'parrot'

    # This dictionary is used for JavaScript logic in templates, not for Django model field
    BREED_CHOICES_DICT = {
        DOG: [(LABRADOR, 'Labrador'), (GERMAN_SHEPHERD, 'German Shepherd'), (POODLE, 'Poodle')],
        CAT: [(PERSIAN, 'Persian Cat'), (MAINE_CONN, 'Maine Coon'), (SIAMESE, 'Siamese')],
        BIRD: [(PARROT, 'Parrot')],
        OTHER: [(OTHER, 'Other')]
    }
    MALE = 'M'
    FEMALE = 'F'
    UNKNOWN = 'U'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (UNKNOWN, 'Unknown'),
    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=UNKNOWN,
    )


    petowner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pets')
    name = models.CharField(max_length=50)
    species = models.CharField(max_length=30, choices=SPECIES_CHOICES, default=DOG)
    spayed_neutered = models.BooleanField(default=False)
    image = models.ImageField(upload_to='pet_app/', blank=True, null=True)
    breed = models.CharField(max_length=50)  # No default choices here
    age = models.IntegerField()
    medical_history = models.ManyToManyField('MedicalHistory', blank=True)

    def __str__(self):
        return f"{self.name} ({self.species})"



