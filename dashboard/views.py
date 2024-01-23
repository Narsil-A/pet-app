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
            # Redirect to a profile setup page or show an error message
            return redirect('profile-setup')  # Example redirect
        
    elif user.is_petowner:
        context['user_type'] = 'petowner'
        # Directly filter pets based on the user instance
        context['pets'] = Pet.objects.filter(petowner=user)  # Use 'petowner' or the correct related name
        ...
    else:
        context['user_type'] = 'other'

    return render(request, 'dashboard/dashboard.html', context)




