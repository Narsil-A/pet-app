from django.urls import path


from . import views

app_name = 'pets'

urlpatterns = [
    path('', views.pets_list, name='list'),
    path('add-pet/', views.add_pet, name='add_pet'),
    path('<int:pet_id>/', views.pet_detail, name='detail'),
    path('<int:pet_id>/delete/', views.pet_delete, name='delete'),
    path('<int:pet_id>/edit/', views.pet_edit, name='edit'),
    path('add-weight/<int:pet_id>/', views.add_weight_record, name='add_weight_record'),
    path('<int:pet_id>/edit_goal_weight/', views.edit_goal_weight, name='edit_goal_weight'),
    path('pets/<int:record_id>/delete-weight-record/', views.delete_weight_record, name='delete_weight_record'),
    path('petowner/list/', views.petowner_list, name='petowner_list'),
    path('petowner/<int:petowner_id>/', views.petowner_detail, name='petowner_detail'),
    path('search/', views.search_for_pets, name='search_for_pets'),
    path('weight-tracker/', views.weighttracker, name='weight_tracker'),
]