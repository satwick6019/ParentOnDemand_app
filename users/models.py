from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('parent', 'Parent'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15,default='')