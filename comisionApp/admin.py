from django.contrib import admin
from .models import Ciudad, Transporte, Solicitud_Comision,Comision, DetalleTrabajo, Itineraio, Comision_x_Afiliado

# Register your models here.

class ComisionAdmin(admin.ModelAdmin):
    search_fields = ['id_comision']
    list_display = ('num_comision','fech_inicio','fech_fin')

class TransporteAdmin(admin.ModelAdmin):
    search_fields = ['num_legajo','patente']
    list_display = ('num_legajo','patente')

class CiudadAdmin(admin.ModelAdmin):
    search_fields = ['ciudad']


admin.site.register(Comision,ComisionAdmin)
admin.site.register(Comision_x_Afiliado)
admin.site.register(Ciudad,CiudadAdmin)
admin.site.register(Transporte,TransporteAdmin)
admin.site.register(Solicitud_Comision)
admin.site.register(DetalleTrabajo)
##admin.site.register(Itineraio)

