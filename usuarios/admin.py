from django.contrib import admin
from .models import Agente
# Register your models here.

class AgenteAdmin(admin.ModelAdmin):
    search_fields = ['num_afiliado']
    list_display = ('num_afiliado')

admin.site.register(Agente)