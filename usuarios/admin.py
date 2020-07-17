from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from usuarios.models import User


class CustomUserAdmin(UserAdmin):
    search_fields = ['dni','last_name','first_name']
    list_display = ('dni','last_name','first_name','num_tel')
    list_filter = ()
    ordering = ['last_name','first_name']

    fieldsets = UserAdmin.fieldsets + (
        ('Info extra', {'fields': ('num_afiliado','dni','num_tel',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Info extra', {'fields': ('num_afiliado','dni','num_tel',)}),
    )

admin.site.register(User,CustomUserAdmin)
