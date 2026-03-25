from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class ParentProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    city = models.CharField(max_length=100)

    PARENT_TYPE_CHOICES = (
        ('father', 'Father'),
        ('mother', 'Mother'),
    )
    parent_type = models.CharField(max_length=10, choices=PARENT_TYPE_CHOICES)

    SERVICE_TYPE_CHOICES = (
        ('call', 'On Call'),
        ('onsite', 'On Site'),
    )
    service_type = models.CharField(max_length=10, choices=SERVICE_TYPE_CHOICES)

    price = models.IntegerField()
    description = models.TextField()

    photo = models.ImageField(upload_to='parent_photos/')
    aadhar = models.FileField(upload_to='aadhar_docs/')

    is_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Request(models.Model):

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    parent = models.ForeignKey(ParentProfile, on_delete=models.CASCADE, related_name='received_requests')

    status = models.CharField(max_length=10, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} → {self.parent}"