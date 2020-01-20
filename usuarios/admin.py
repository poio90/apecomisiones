from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Afiliado
# Register your models here.


class AfiliadoAdmin(admin.ModelAdmin):
    list_display = ('user', 'num_afiliado', 'dni', 'num_tel')
    #list_editable = ('dni','num_tel')
    search_fields = ['user__first_name', 'user__last_name', 'num_tel']
    #list_filter = ('user__is_active', 'user__is_staff')

    fieldsets = (
        ('Afiliado', {
            'fields': (
                'user', 'num_afiliado'),
        }),
        ('Datos extra', {
            'fields': (
                'dni', 'num_tel'
            )
        })
    )


class AfiliadoInline(admin.StackedInline):
    model = Afiliado
    can_delete = False
    verbose_name_plural = 'afiliados'


class UsuarioAdmin(BaseUserAdmin):
    inlines = (AfiliadoInline,)


admin.site.unregister(User)
admin.site.register(User, UsuarioAdmin)