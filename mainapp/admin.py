from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Post

# Register your models here.
admin.site.register(User)
admin.site.register(Post)

class CustomUserAdmin(UserAdmin):
    model = User