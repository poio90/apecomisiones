from django.contrib import admin
from .models import Ciudad, Transporte,Comision, DetalleTrabajo, Itineraio

# Register your models here.

class ComisionAdmin(admin.ModelAdmin):
    search_fields = ['id_comision']
    list_display = ('num_comision','fech_inicio','fech_fin')

class TransporteAdmin(admin.ModelAdmin):
    search_fields = ['num_legajo','patente']
    list_display = ('num_legajo','patente')


admin.site.register(Comision,ComisionAdmin)
admin.site.register(Ciudad)
admin.site.register(Transporte,TransporteAdmin)
admin.site.register(DetalleTrabajo)
##admin.site.register(Itineraio)

