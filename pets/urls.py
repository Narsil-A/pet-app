from django.urls import path


from . import views

app_name = 'pets'

urlpatterns = [
    path('', views.pets_list, name='list'),
    path('add-pet/', views.add_pet, name='add_pet'),
    path('<int:pet_id>/', views.pet_detail, name='detail'),
    path('<int:pet_id>/delete/', views.pet_delete, name='delete'),
    path('<int:pet_id>/edit/', views.pet_edit, name='edit'),
    path('add-weight/', views.add_weight_record, name='add_weight_record'),
    path('pets/<int:record_id>/delete-weight-record/', views.delete_weight_record, name='delete_weight_record'),
    path('weight-records/<int:pet_id>/', views.view_weight_records, name='view_weight_records'),
]