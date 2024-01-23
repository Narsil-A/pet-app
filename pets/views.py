import json
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PetOwnerForm
from pet_app.decorators import petowner_required
from django.contrib.auth.decorators import login_required


from .models import Pet


@login_required
def pets_list(request):
    pets_queryset = Pet.objects.filter(petowner=request.user).prefetch_related('medical_history')

    # Custom serialization
    pets_data = []
    for pet in pets_queryset:
        pet_data = {
            'id': pet.id,
            'name': pet.name,
            'species': pet.species,
            'breed': pet.breed,
            'age': pet.age,
            'image_url': pet.image.url if pet.image else '',
            'gender':pet.gender,
            'spayed_neutered': 'Yes' if pet.spayed_neutered else 'No',
            'medical_history': [str(history) for history in pet.medical_history.all()]
        }
        pets_data.append(pet_data)

    pets_json = json.dumps(pets_data)  

    return render(request, 'pets/pets_list.html', {'pets': pets_json})


@login_required
def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, petowner=request.user)  # Ensure the pet belongs to the logged-in user
    return render(request, 'pets/detail_pet.html', {'pet': pet})
    


@login_required
def pet_delete(request, pet_id):
    pet = get_object_or_404(Pet, petowner=request.user, pk=pet_id)
    pet.delete()
    messages.success(request, "The pet was deleted")

    return redirect('pets:list')


@login_required
def pet_edit(request, pet_id):
    pet = get_object_or_404(Pet, petowner=request.user, pk=pet_id)

    if request.method == 'POST':
        form = PetOwnerForm(request.POST, instance=pet)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.petowner = request.user
            pet.save()
            form.save_m2m() 
            messages.success(request, "The pet information was edited")
            return redirect('pets:list')
    else:
        form = PetOwnerForm(instance=pet)  
    
    breed_choices_dict = Pet.BREED_CHOICES_DICT
    breed_choices_json = json.dumps(breed_choices_dict)
    
    return render(request, 'pets/edit_mypet.html', {
        'form': form,
        'breed_choices_json': breed_choices_json  
    })


@login_required
def add_pet(request):
    if request.method == 'POST':
        form = PetOwnerForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.petowner = request.user
            pet.save()
            form.save_m2m()  # Save the many-to-many data for 'medical_history'
            messages.success(request, "The pet was successfully added.")
            return redirect('pets:list')
    else:
        form = PetOwnerForm()

    breed_choices_dict = Pet.BREED_CHOICES_DICT
    breed_choices_json = json.dumps(breed_choices_dict)
    return render(request, 'pets/add_pet.html', {
        'form': form,
        'breed_choices_json': breed_choices_json  
    })