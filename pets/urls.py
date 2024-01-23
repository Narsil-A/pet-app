from django.urls import path


from . import views

app_name = 'pets'

urlpatterns = [
    path('', views.pets_list, name='list'),
    path('add-pet/', views.add_pet, name='add_pet'),
    path('<int:pet_id>/', views.pet_detail, name='detail'),
    path('<int:pet_id>/delete/', views.pet_delete, name='delete'),
    path('<int:pet_id>/edit/', views.pet_edit, name='edit'),
]