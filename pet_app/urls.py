from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views
from core.views import index, about
from django.urls import path, include

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', include('userprofile.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('dashboard/services/', include('services.urls')),
    path('dashboard/medicalvisit/', include('medicalvisit.urls')),
    path('dashboard/appointments/', include('appointments.urls')),
    path('dashboard/chatbot/', include('chatbot.urls')),
    path('pets/', include('pets.urls')),
    path('about/', about, name='about'),
    path('log-in/', views.LoginView.as_view(template_name='userprofile/login.html'), name='login'),
    path('log-out/', views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


   