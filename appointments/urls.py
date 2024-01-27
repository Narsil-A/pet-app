from django.urls import path


from . import views

app_name = 'appointments'

urlpatterns = [
    path('add-schedule/<int:service_id>/', views.schedule_appointment_view, name='add_schedule'),
    path('cancel-appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('available-slots/', views.available_slots, name='available_slots'),
    path('appointments-list/', views.view_appointments, name='appointments_list'),
    path('create-slot/', views.create_slot_view, name='create_slot'),
    path('delete-slot/<int:appointmentslot_id>/', views.delete_slots, name='delete_slot'),
    path('slots/', views.slots_view, name='slots_view'),
]