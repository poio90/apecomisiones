from django.contrib import admin
from .models import Agente, Ciudad, Transporte

# Register your models here.

class AgenteAdmin(admin.ModelAdmin):
    search_fields = ['apellido','nombre']
    list_display = ('num_afiliado','apellido','nombre','dni','email','num_tel')

admin.site.register(Agente,AgenteAdmin)
admin.site.register(Ciudad)
admin.site.register(Transporte)
