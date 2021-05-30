from django.contrib import admin

# Register your models here.
from .models import Blog
from .models import CustomUser

admin.site.register(Blog)
admin.site.register(CustomUser)