from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("New Fields", {'fields': ('phone_number', 'categoria')}),
    )
    # list_display = ['username', 'email', 'phone_number', 'categoria']

admin.site.register(User, CustomUserAdmin)

admin.site.register(Local)
admin.site.register(Foto)

