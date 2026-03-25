from django.contrib import admin

# Register your models here.
from .models import ParentProfile, Request

admin.site.register(ParentProfile)
admin.site.register(Request)