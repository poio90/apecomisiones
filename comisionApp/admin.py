from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *

class TransporteResources(resources.ModelResource):
    class Meta:
        model = Transporte

class TransporteAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['num_legajo', 'patente']
    list_display = ('num_legajo', 'patente')
    resources_class = TransporteResources


class CiudadAdmin(admin.ModelAdmin):
    search_fields = ['ciudad']


admin.site.register(Itinerario)

admin.site.register(Ciudad, CiudadAdmin)
admin.site.register(Provincia)
admin.site.register(Transporte, TransporteAdmin)

# admin.site.register(Itineraio)
