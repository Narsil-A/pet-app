from django.urls import path


from . import  views


app_name = 'userprofile'


urlpatterns = [
    path('myaccount/', views.myaccount, name='myaccount'),
    path('signup/<str:role>/', views.signup, name='signup'),
    path('get-notifications/', views.get_notifications, name='get_notifications'),
    path('mark-notification-as-read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
]