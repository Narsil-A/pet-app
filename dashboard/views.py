from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from userprofile.models import VetStaff, PetOwner

from django.shortcuts import render, redirect
from userprofile.models import PetOwner
from pets.models import Pet


@login_required
def dashboard(request):
    user = request.user
    context = {}

    if user.is_vetstaff:
        context['user_type'] = 'vetstaff'
        try:
            context['vetstaff_info'] = VetStaff.objects.get(user=user)
        except ObjectDoesNotExist:
            return redirect('dashboard:dashboard') 
        
    else:
        user.is_petowner
        context['user_type'] = 'petowner'
       
        context['pets'] = Pet.objects.filter(petowner=user)  

    return render(request, 'dashboard/dashboard2.html', context)




