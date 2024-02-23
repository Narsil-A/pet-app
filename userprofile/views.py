# signup form 
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .models import Notification, VetStaff, PetOwner, User
from .forms import PetOwnerSignUpForm, VetStaffSignUpForm, PetOwnerEditForm, VetStaffEditForm, PasswordChangeForm



def signup(request, role='petowner'):
    if role == 'petowner':
        form_class = PetOwnerSignUpForm
    elif role == 'vetstaff':
        form_class = VetStaffSignUpForm
    else:
        return redirect('dashboard:dashboard')

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return redirect('/log-in/')
    else:
        form = form_class()

    return render(request, 'userprofile/signup.html', {'form': form, 'role': role})



@login_required
def myaccount(request):
    return render(request, 'userprofile/myaccount.html')

@login_required
def edit_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Corrected field name

    if user.is_vetstaff:
        vetstaff = VetStaff.objects.get(user=user)
        form_class = VetStaffEditForm
        instance = vetstaff
    elif user.is_petowner:
        petowner = PetOwner.objects.get(user=user)
        form_class = PetOwnerEditForm
        instance = petowner
    else:
        return redirect('dashboard:dashboard')

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=instance.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('userprofile:myaccount')
    else:
        form = form_class(instance=instance.user)

    return render(request, 'userprofile/edit_profile.html', {'form': form, 'user': user})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = request.user
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            # Redirect to a success page, e.g., login page
            return redirect('/log-in/')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'userprofile/change_password.html', {'form': form})


@login_required
def get_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user, read=False).values('id', 'message')
    return JsonResponse({'notifications': list(notifications)})


@login_required
def mark_notification_as_read(request, notification_id):
    if request.method == "POST":
        try:
            notification = Notification.objects.get(id=notification_id, recipient=request.user)
            notification.read = True 
            notification.save()
            return JsonResponse({"status": "success"})
        except Notification.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Notification not found"}, status=404)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

