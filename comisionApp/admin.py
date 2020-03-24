from django.contrib import admin
from .models import *


class IAxInline(admin.TabularInline):
    model = Integrantes_x_Anticipo
    extra = 1
    show_change_link = True


class AnticipoAdmin(admin.ModelAdmin):
    search_fields = ['num_comision']
    list_display = ('num_comision', 'fech_inicio', 'fech_fin')
    inlines = (IAxInline,)


class TransporteAdmin(admin.ModelAdmin):
    search_fields = ['num_legajo', 'patente']
    list_display = ('num_legajo', 'patente')


class CiudadAdmin(admin.ModelAdmin):
    search_fields = ['ciudad']


admin.site.register(Anticipo, AnticipoAdmin)
admin.site.register(Ciudad, CiudadAdmin)
admin.site.register(Transporte, TransporteAdmin)
admin.site.register(Solicitud)
admin.site.register(DetalleTrabajo)
# admin.site.register(Itineraio)
