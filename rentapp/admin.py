from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("New Fields", {'fields': ('phone_number', 'categoria')}),
    )
    # list_display = ['username', 'email', 'phone_number', 'categoria']

admin.site.register(Amistad)
admin.site.register(Mensaje)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Renta)
admin.site.register(Foto)

