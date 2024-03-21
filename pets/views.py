import json
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from pet_app.decorators import vetstaff_required, petowner_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PetOwnerForm, WeightRecordPetForm, WeightRecordPetInitialForm, GoalWeightForm
from .models import WeightRecord
from .models import Pet
from userprofile.models import PetOwner, VetStaff



from .models import Pet


@login_required
def pets_list(request):

    if request.user.is_vetstaff:
        pets_queryset = Pet.objects.prefetch_related('medical_history')
    else:
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
def pet_detail(request, pet_id):
    # Fetch pet details, ensuring it's owned by the logged-in user or accessible by vet staff
    if request.user.is_vetstaff:
        pet = get_object_or_404(Pet, id=pet_id)
    else:
        pet = get_object_or_404(Pet, id=pet_id, petowner=request.user)

    # Fetch weight records for the pet
    records = WeightRecord.objects.filter(pet=pet).order_by('-date')

    # Preparing the data for the graph
    dates = [record.date.strftime("%Y-%m-%d") for record in records]
    weights = [float(record.weight) for record in records]
    goal_weights = [float(record.goal_weight) for record in records if record.goal_weight]

    # Assuming the most recent record contains the current weight and goal weight
    if records:
        current_weight = weights[0]  # Most recent weight due to '-date' ordering
        goal_weight = goal_weights[0] if goal_weights else None  # Most recent goal weight, if available
        to_goal_weight = current_weight - goal_weight if goal_weight is not None else None
    else:
        current_weight, goal_weight, to_goal_weight = None, None, None

    # Serialize data for safe JavaScript use
    dates_json = json.dumps(dates)
    weights_json = json.dumps(weights)
    goal_weights_json = json.dumps(goal_weights)

    return render(request, 'pets/detail_pet.html', {
        'pet': pet,
        'records': records,
        'dates_json': dates_json,
        'weights_json': weights_json,
        'goal_weights_json': goal_weights_json,
        'current_weight': current_weight,
        'goal_weight': goal_weight,
        'to_goal_weight': to_goal_weight,
    })


@login_required
def edit_goal_weight(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, petowner=request.user)  # Ensure the pet belongs to the user
    weight_record = WeightRecord.objects.filter(pet=pet).order_by('-date').first()  # Get the most recent record

    if request.method == 'POST':
        form = GoalWeightForm(request.POST, instance=weight_record)
        if form.is_valid():
            form.save()
            return redirect('pets:detail', pet_id=pet.id)
    else:
        form = GoalWeightForm(instance=weight_record)  # Pass the most recent record to prepopulate the form

    return render(request, 'pets/edit_goal_weight.html', {
        'form': form,
        'pet': pet
    })
    
@login_required
def add_weight_record(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, petowner=request.user)  # Adjusted to use 'petowner' instead of 'owner'

    # Check if this is the first weight record for the pet
    first_record = not WeightRecord.objects.filter(pet=pet).exists()

    if request.method == 'POST':
        # Use the initial form if this is the first weight record, else use the regular form
        if first_record:
            form = WeightRecordPetInitialForm(request.POST, pet=pet)
        else:
            form = WeightRecordPetForm(request.POST, pet=pet)
        
        if form.is_valid():
            weight_record = form.save(commit=False)
            weight_record.pet = pet
            weight_record.save()
            messages.success(request, "Weight record added successfully.")
            return redirect('pets:detail', pet_id=pet.id)
    else:
        # Initialize the appropriate form based on whether it's the first record
        if first_record:
            form = WeightRecordPetInitialForm(pet=pet)  # Create form instance with pet
        else:
            form = WeightRecordPetForm(pet=pet)  # Create form instance with pet

    return render(request, 'pets/add_weight_record.html', {'form': form, 'pet': pet})


@login_required
def delete_weight_record(request, record_id):
    record = get_object_or_404(WeightRecord, pk=record_id, pet__petowner=request.user)
    record.delete()
    messages.success(request, "The weight record was deleted successfully.")
    return redirect('pets:detail', pet_id=record.pet.id)



@login_required
def weighttracker(request):
    pets = Pet.objects.filter(petowner=request.user)
    return render(request, 'pets/weight_tracker.html', {'pets': pets})

@login_required
def petowner_detail(request, petowner_id):
   
    petowner = get_object_or_404(PetOwner, pk=petowner_id)
    
    pets = Pet.objects.filter(petowner__id=petowner_id)

    context = {
        'petowner': petowner, 
        'pets': pets
    }
    return render(request, 'pets/petowner_detail.html', context)

@login_required
def vetstaff_detail(request, vetstaff_id):
    vetstaff = get_object_or_404(VetStaff, pk=vetstaff_id)

    context = {
        'vetstaff': vetstaff,  
    }
    return render(request, 'pets/vetstaff_detail.html', context)

@login_required
def petowner_list(request):
    petowners = PetOwner.objects.all()

    context = {
        'petowners': petowners, 
    }
    return render(request, 'pets/petowner_list.html', context)




@login_required
def search(request):
    query = request.GET.get('query', '')
    petowners = PetOwner.objects.none()
    pets = Pet.objects.none()
    vetstaff = VetStaff.objects.none()

    user = request.user

    # Utilize the custom boolean fields in your User model for role determination
    if user.is_vetstaff:
        # Vet staff search logic for petowners and pets
        petowners = PetOwner.objects.filter(
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()
        pets = Pet.objects.filter(name__icontains=query).distinct()

    elif user.is_petowner:
        # Pet owner search logic for vetstaff
        vetstaff = VetStaff.objects.filter(
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()

    context = {
        'petowners': petowners,
        'pets': pets,
        'vetstaff': vetstaff,
        'query': query
    }

    return render(request, 'pets/search_results.html', context)

