from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from pet_app.decorators import vetstaff_required
from .forms import PetMedicalVisitForm
from .models import PetMedicalVisit


@vetstaff_required
def add_medical_visit(request):
    if request.method == 'POST':
        form = PetMedicalVisitForm(request.POST, request.FILES)
        if form.is_valid():
            medical_visit = form.save(commit=False)
            medical_visit.vet_staff = request.user
            medical_visit.save()
            messages.success(request, "The medical visit record saved successfully.")
            return redirect('medicalvisit:medical_visit_list')
    else:
        form = PetMedicalVisitForm()

    return render(request, 'medicalvisit/medicalvisitform.html', {'form': form})


@login_required
def medical_visit_list(request):
    user = request.user
    if user.is_vetstaff:
        medical_visits = PetMedicalVisit.objects.select_related('pet').all()
    
    else:
        medical_visits = PetMedicalVisit.objects.filter(pet__petowner=request.user).order_by('date_of_visit')
    
    return render(request, 'medicalvisit/recordsmedicalvisit.html', {'medical_visits': medical_visits})



@login_required
def medical_visit_detail(request, medical_visit_id):
    medical_visit = get_object_or_404(PetMedicalVisit, id=medical_visit_id)  
    return render(request, 'medicalvisit/medicalvisit_detail.html', {'medical_visit': medical_visit})
    


@vetstaff_required
def medical_visit_delete(request, medical_visit_id):
    medical_visit = get_object_or_404(PetMedicalVisit, pk=medical_visit_id)
    medical_visit.delete()
    messages.success(request, "The medical visit was deleted")

    return redirect('medicalvisit:medical_visit_list')


@vetstaff_required
def medical_visit_edit(request, medical_visit_id):
    medical_visit = get_object_or_404(PetMedicalVisit, pk=medical_visit_id)

    if request.method == 'POST':
        form = PetMedicalVisitForm(request.POST, request.FILES)
        if form.is_valid():
            medical_visit = form.save(commit=False)
            medical_visit.vet_staff = request.user
            medical_visit.save()
            messages.success(request, "The medical visit record saved edited successfully.")
            return redirect('medicalvisit:medical_visit_list')
    else:
        form = PetMedicalVisitForm(instance=medical_visit)
    
    return render(request, 'medicalvisit/medicalvisit_edit.html', {
        'form': form,
    })

   