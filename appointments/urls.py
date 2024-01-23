from django.urls import path


from . import views

app_name = 'appointments'

urlpatterns = [
    path('add-schedule/<int:service_id>/', views.schedule_appointment_view, name='add_schedule'),
    path('available-slots/', views.available_slots, name='available_slots'),
    path('appointments-list/', views.view_appointments, name='appointments_list'),
    path('create-slot/', views.create_slot_view, name='create_slot'),
]