from django.urls import path


from . import views

app_name = 'services'

urlpatterns = [
    path('', views.service_list, name='list'),
    path('<int:pk>/', views.service_detail, name='detail'),
    path('<int:pk>/delete/', views.service_delete, name='delete'),
    path('<int:pk>/edit/', views.service_edit, name='edit'),
    path('add-service/', views.add_service, name='add_service'),
    path('create-category/', views.create_pet_service_category, name='create_category'),
    path('request-service/', views.request_service, name='request_service'),
    path('cancel/<int:request_id>/', views.cancel_service_request, name='cancel_service_request'),
    path('request-service-list/', views.request_service_list, name='request_list'),
    path('<int:request_id>/request-detail/', views.request_detail, name='request_detail'),
    path('make-payment/', views.make_payment, name='payment'),
    path('payment-successful/', views.payment_successful, name='payment_successful'),
    path('payment-cancelled/', views.payment_cancelled, name='payment_cancelled'),
    path('stripe-webhook/', views.stripe_webhook, name='stripe_webhook'),
]