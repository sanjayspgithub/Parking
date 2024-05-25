from django.contrib import admin
from .models import Userlogin, Visitor, park_vehicle

# Register your models here.
admin.site.register(Userlogin)
admin.site.register(Visitor)
admin.site.register(park_vehicle)
