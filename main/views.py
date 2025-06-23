from django.shortcuts import render, redirect, get_object_or_404
from .models import AdminUser, Service, ServiceMedia

# Static Pages
def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')

def services(request):
    return render(request, 'main/services.html')

def contact(request):
    return render(request, 'main/contact.html')

from django.shortcuts import redirect

def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')  # redirects to /admin-login/

def forgot_password(request):
    message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            admin = AdminUser.objects.get(username=username)
            # You can either:
            # (A) Set a temporary password here
            # (B) Redirect to another page to set new password

            # For now, just show message
            message = f"Hi {admin.username}, please contact superadmin to reset your password."
        except AdminUser.DoesNotExist:
            message = "Username not found."

    return render(request, 'main/forgot_password.html', {'message': message})





# Admin Login View
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            admin = AdminUser.objects.get(username=username, password=password)
            request.session['admin_logged_in'] = True
            return redirect('admin_dashboard')
        except AdminUser.DoesNotExist:
            return render(request, 'admin_login.html', {'error': 'Invalid credentials'})
    return render(request, 'admin_login.html')

# Admin Dashboard
def admin_dashboard(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    services = Service.objects.all()
    return render(request, 'admin_dashboard.html', {'services': services})

# Upload Media to Service
def upload_service_media(request, service_id):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    service = Service.objects.get(id=service_id)
    if request.method == 'POST' and request.FILES:
        for f in request.FILES.getlist('media'):
            ServiceMedia.objects.create(service=service, media_file=f)
        return redirect('admin_dashboard')
    return render(request, 'upload_media.html', {'service': service})

# Service Detail View
def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    media = service.servicemedia_set.all()
    return render(request, 'main/service_detail.html', {
        'service': service,
        'media': media
    })

# Rename Service
def rename_service(request, service_id):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    service = Service.objects.get(id=service_id)
    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        if new_name:
            service.name = new_name
            service.save()
    return redirect('admin_dashboard')
