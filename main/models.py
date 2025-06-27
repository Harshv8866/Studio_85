
# studio/models.py
from django.db import models


# main/models.py

from django.db import models

class AdminUser(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)  # For demo use only. You should hash this later.

    def __str__(self):
        return self.username


class Service(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_first_image(self):
        return self.media.filter(media_file__iendswith=('.jpg', '.jpeg', '.png')).first()


class ServiceMedia(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='media')
    media_file = models.FileField(upload_to='service_media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service.name} - {self.media_file.name}"


class StudioContact(models.Model):
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return "Studio Contact Info"
