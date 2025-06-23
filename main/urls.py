from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('upload-media/<int:service_id>/', views.upload_service_media, name='upload_service_media'),
    path('rename-service/<int:service_id>/', views.rename_service, name='rename_service'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),




]
