import json
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PetOwnerForm, WeightRecordForm
from .models import WeightRecord
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



@login_required
def add_weight_record(request):
    pet = get_object_or_404(Pet, petowner=request.user)
    if request.method == 'POST':
        form = WeightRecordForm(request.POST, user=request.user)
        if form.is_valid():
            weight_record = form.save(commit=False)
            weight_record.pet = pet
            weight_record.save()
            messages.success(request, "Weight record added successfully.")
            return redirect('pets:view_weight_records', pet_id=weight_record.pet.id)   # Replace with the appropriate view
    else:
        form = WeightRecordForm(user=request.user)
    
    return render(request, 'pets/add_weight_record.html', 
    {'form': form})



@login_required
def delete_weight_record(request, record_id):
    record = get_object_or_404(WeightRecord, pk=record_id, pet__petowner=request.user)
    record.delete()
    messages.success(request, "The weight record was deleted successfully.")
    return redirect('pets:view_weight_records', pet_id=record.pet.id)


@login_required
def view_weight_records(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, petowner=request.user)
    records = WeightRecord.objects.filter(pet=pet).order_by('-date')

    # Preparing the data for the graph
    dates = [record.date.strftime("%Y-%m-%d") for record in records]
    weights = [float(record.weight) for record in records]
    goal_weights = [float(record.goal_weight) for record in records if record.goal_weight]

    # Serialize data for safe JavaScript use
    dates_json = json.dumps(dates)
    weights_json = json.dumps(weights)
    goal_weights_json = json.dumps(goal_weights)
    print("Dates:", dates)
    print("Weights:", weights)
    print("Goal Weights:", goal_weights)

    return render(request, 'pets/view_weight_records.html', {
        'pet': pet,
        'records': records,
        'dates_json': dates_json,
        'weights_json': weights_json,
        'goal_weights_json': goal_weights_json,
    })
