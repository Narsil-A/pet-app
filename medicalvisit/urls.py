from django.urls import path


from . import views

app_name = 'medicalvisit'

urlpatterns = [
    path('add-medical-visit/', views.add_medical_visit, name='medical_visit'),
    path('medical-visit-list/', views.medical_visit_list, name='medical_visit_list'),
    path('medical-visit/<int:medical_visit_id>/', views.medical_visit_detail, name='medical_visit_detail'),
    path('edit-medical-visit/<int:medical_visit_id>/', views.medical_visit_edit, name='edit_medical_visit'),
    path('<int:medical_visit_id>/delete/', views.medical_visit_delete, name='delete'),
]