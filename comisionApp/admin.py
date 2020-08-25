from django.contrib import admin
from .models import *


class TransporteAdmin(admin.ModelAdmin):
    search_fields = ['num_legajo', 'patente']
    list_display = ('num_legajo', 'patente')


class CiudadAdmin(admin.ModelAdmin):
    search_fields = ['ciudad']


admin.site.register(Ciudad, CiudadAdmin)
admin.site.register(Transporte, TransporteAdmin)

# admin.site.register(Itineraio)
