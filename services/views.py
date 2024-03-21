import stripe
import time
import logging
from django.conf import settings
from django.db.models import Subquery, OuterRef, Exists
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from userprofile.models import Notification, User, PetOwner
from .forms import PetServicesForm, PetRequestServicesForm, PetServiceTrackerUpdateForm, PetServiceCategoryForm
from .models import PetService, PetServiceTracker, PetRequestService

logger = logging.getLogger(__name__)


@login_required
def service_list(request):
    services = PetService.objects.all()

    return render(request, 'services/services_list.html', {
        'services': services
    })


@login_required
def service_detail(request, pk):
    service = get_object_or_404(
        PetService, created_by=request.user, pk=pk)

    return render(request, 'services/service_detail.html', {
        'service': service
    })


@login_required
def service_delete(request, pk):
    service = get_object_or_404(
        PetService, created_by=request.user, pk=pk)
    service.delete()
    messages.success(request, "The service was deleted")

    return redirect('services:list')


@login_required
def service_edit(request, pk):
    service = get_object_or_404(
       PetService, created_by=request.user, pk=pk)

    if request.method == 'POST':
        form = PetServicesForm(request.POST, instance=service)
        if form.is_valid():
            service.save()
            messages.success(request, "The service was created")

            return redirect('services:list')

    else:
        form = PetServicesForm(instance=service)

    return render(request, 'services/service_edit.html', {

        'form': form

    })

def create_pet_service_category(request):
    if request.method == 'POST':
        form = PetServiceCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            
    else:
        form = PetServiceCategoryForm()
    
    return render(request, 'services/create_category.html', {'form': form})

@login_required
def add_service(request):
    if request.method == 'POST':
        form = PetServicesForm(request.POST)

        if form.is_valid():
            service = form.save(commit=False)
            service.created_by = request.user
            service.save()
            messages.success(request, "The service was created")

            return redirect('services:list')
    else:
        form = PetServicesForm()

    return render(request, 'services/add_services.html', {

        'form': form

    })


@login_required
def request_service_list(request):
    user = request.user
    if user.is_vetstaff:
        requests_services = PetRequestService.objects.select_related('petowner').all()
    else:
        requests_services = PetRequestService.objects.filter(petowner=user)

    # Annotate with tracking information
    requests_services = requests_services.annotate(
        latest_status_update=Subquery(
            PetServiceTracker.objects.filter(
                requested_service=OuterRef('pk')
            ).order_by('-created_at').values('status')[:1]
        ),
        is_tracked=Exists(
            PetServiceTracker.objects.filter(
                requested_service=OuterRef('pk')
            )
        )
    )

    return render(request, 'services/request_list.html', {'requests_services': requests_services})


@login_required
def request_detail(request, request_id):
    user = request.user
    request_detail_qs = PetRequestService.objects.filter(id=request_id).annotate(
        latest_status_update=Subquery(
                PetServiceTracker.objects.filter(
                requested_service=OuterRef('pk')
            ).order_by('-created_at').values('status')[:1]
        )
    )
    request_detail = get_object_or_404(request_detail_qs, id=request_id)

    # Allow only the petowner who made the request or lab staff to view the details
    if not (user.is_vetstaff or request_detail.petowner == user):
        messages.error(
            request, "You do not have permission to access this request.")
        return redirect('services:dashboard')

    # Fetch all updates for the request
    updates = request_detail.service_updates.order_by('-created_at')

    # Handle status update by vet staff
    if user.is_vetstaff and request.method == 'POST':
        form = PetServiceTrackerUpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.requested_service = request_detail
            update.updated_by = user
            update.save()

            Notification.objects.create(
                recipient=request_detail.petowner,
                message=f"Status of your request '{request_detail.service.name}' has been updated."
            )
            messages.success(request, "Status updated successfully.")
            return redirect('services:request_list')
    else:
        form = PetServiceTrackerUpdateForm() if user.is_vetstaff else None

    return render(request, 'services/request_detail.html', {
        'request_detail': request_detail,
        'latest_status_update': request_detail.latest_status_update,
        'updates': updates,
        'form': form,
        'paid_status': request_detail.paid,
    })

@login_required
def request_service(request):
    services = PetService.objects.all()

    if request.method == 'POST':
        form = PetRequestServicesForm(request.POST, user=request.user)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.petowner = request.user
            service_request.save()

            # Notify staff members about the new request
            staff_members = User.objects.filter(is_vetstaff=True)
            for staff_member in staff_members:
                Notification.objects.create(
                    recipient=staff_member,
                    message=f"A new request has been made by {request.user.username}."
                )

            # Store the selected service ID for subsequent steps
            request.session['selected_service_id'] = service_request.service.id

            # Redirect to appointment scheduling
            return redirect('services:request_detail', request_id=service_request.id) 
    else:
        form = PetRequestServicesForm(user=request.user)  

    context = {
        'form': form,
        'services': services
    }
    return render(request, 'services/request_service.html', context)

@login_required
def cancel_service_request(request, request_id):
    service_request = get_object_or_404(PetRequestService, id=request_id)

    # Check if the current user is the petowner or a vet staff member
    if request.user == service_request.petowner:
        service_request.delete()
        messages.success(request, "The service request has been successfully cancelled.")
    else:
        messages.error(request, "You do not have permission to cancel this service request.")


    return redirect('services:request_list')




@login_required
def make_payment(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Retrieve or create the client profile
    petowner, created = PetOwner.objects.get_or_create(user=request.user)
    
    # Check if Stripe customer exists, create if not
    if not petowner.stripe_customer_id:
        stripe_customer = stripe.Customer.create(email=request.user.email)
        petowner.stripe_customer_id = stripe_customer.id
        petowner.save()

    # Retrieve unpaid service requests for the client
    service_requests = PetRequestService.objects.filter(petowner=request.user, paid=False).all()

    if not service_requests.exists():
        return redirect('services:request_service')

    line_items = [
    {
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': service_request.service.name},
                'unit_amount': int(service_request.service.cost * 100),
            },
            'quantity': 1,
        } for service_request in service_requests
    ]


    if request.method == 'POST':
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                customer=petowner.stripe_customer_id,  # Use the Stripe customer ID
                success_url=request.build_absolute_uri(reverse('services:payment_successful')) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri(reverse('services:payment_cancelled')),
            )
            for sr in service_requests:
                sr.stripe_session_id = checkout_session.id
                sr.save()
            return redirect(checkout_session.url, code=303)
        except stripe.error.StripeError as e:
            return HttpResponse(status=400)

    return render(request, 'services/payment.html', {
    'service_requests': service_requests,
    'total_cost': sum(sr.service.cost for sr in service_requests)
})

@login_required
def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    user_id = request.user.id 
    petowner = PetOwner.objects.get(user=request.user)
    petowner.stripe_checkout_id = checkout_session_id
    petowner.save()

    return render(request, 'services/payment_successfull.html', {'customer': customer})

@login_required
def payment_cancelled(request):
    return render(request, 'services/payment_cancelled.html')

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    time.sleep(15)
    payload = request.body.decode('utf-8')
    signature_header = request.META.get('HTTP_STRIPE_SIGNATURE', '') 
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET, 
            tolerance=600   # Use the webhook secret
        )
    except ValueError as e:
        # Invalid payload
        logger.error(f'Invalid payload: {e}')
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        logger.error(f'Invalid signature: {e}')
        return HttpResponse(status=400)
    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        return HttpResponse(status=500)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session.get('id', None)
        time.sleep(15)

        # Fetch client before updating DiagnosticRequest
        petowner = PetOwner.objects.get(stripe_customer_id=session.customer)
        updated_count = PetRequestService.objects.filter(stripe_session_id=session_id).update(paid=True)
        logger.info(f"Updated {updated_count} Setvice Request records to paid.")


        # Notify staff members
        staff_members = User.objects.filter(is_vetstaff=True)
        for staff_member in staff_members:
            Notification.objects.create(
                recipient=staff_member,
                message=f"A payment has been made by {petowner.user.username}."
            )
        
        petowner.payment_bool = True
        petowner.save()

    return HttpResponse('Webhook received and processed', status=200)