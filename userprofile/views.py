# signup form 
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import Notification, VetStaff
from .forms import PetOwnerSignUpForm, VetStaffSignUpForm



def signup(request, role='petowner'):
    if role == 'petowner':
        form_class = PetOwnerSignUpForm
    elif role == 'vetstaff':
        form_class = VetStaffSignUpForm
    else:
        return redirect('dashboard')

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/log-in/')
    else:
        form = form_class()

    return render(request, 'userprofile/signup.html', {'form': form, 'role': role})



@login_required
def myaccount(request):
    return render(request, 'userprofile/myaccount.html')

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

