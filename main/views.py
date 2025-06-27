from django.shortcuts import render, redirect, get_object_or_404
from .models import AdminUser, Service, ServiceMedia, StudioContact

# Static Pages
def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')

def services(request):
    return render(request, 'main/services.html')

def contact(request):
    return render(request, 'main/contact.html')

# Admin Logout
def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')

# Forgot Password
def forgot_password(request):
    message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            admin = AdminUser.objects.get(username=username)
            message = f"Hi {admin.username}, please contact superadmin to reset your password."
        except AdminUser.DoesNotExist:
            message = "Username not found."
    return render(request, 'main/forgot_password.html', {'message': message})

# Admin Login
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

# Admin Dashboard with services and contact
def admin_dashboard(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    
    services = Service.objects.all()
    contact = StudioContact.objects.first()
    return render(request, 'admin_dashboard.html', {
        'services': services,
        'contact': contact,
    })

# Upload Media with service selection
def upload_media(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    if request.method == 'POST':
        service_id = request.POST.get("service_id")
        service = get_object_or_404(Service, id=service_id)
        for file in request.FILES.getlist("media_file"):
            ServiceMedia.objects.create(service=service, media_file=file)
        return redirect('admin_dashboard')
    
    return redirect('admin_dashboard')

# Update Studio Contact Info
def update_contact(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    contact = StudioContact.objects.first()
    if request.method == 'POST':
        if not contact:
            contact = StudioContact.objects.create(
                phone=request.POST.get('phone', ''),
                email=request.POST.get('email', ''),
                address=request.POST.get('address', '')
            )
        else:
            contact.phone = request.POST.get('phone', '')
            contact.email = request.POST.get('email', '')
            contact.address = request.POST.get('address', '')
            contact.save()
        return redirect('admin_dashboard')

    return redirect('admin_dashboard')

# Service Detail Page (for frontend)
def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    media = service.media.all()  # uses related_name='media'
    return render(request, 'main/service_detail.html', {
        'service': service,
        'media': media
    })


# Rename a Service
def rename_service(request, service_id):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        if new_name:
            service.name = new_name
            service.save()
    return redirect('admin_dashboard')


from django.shortcuts import redirect, get_object_or_404
from .models import ServiceMedia

def delete_media(request, media_id):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    media = get_object_or_404(ServiceMedia, id=media_id)
    media.delete()

    section = request.GET.get('section', 'category')
    return redirect(f'/admin-dashboard/?section={section}')


from .models import Service

def services_page(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})
