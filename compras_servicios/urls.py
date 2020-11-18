from django.urls import path
from django.contrib.auth.decorators import login_required
from compras_servicios import views

urlpatterns = [
    path(route='compras-servicios/solicitudes/',
         view=login_required(views.ComprasServiciosCreate.as_view()),
         name='compras_servicios_solicitud'),

    path('compras-servicios/<pk>/editar/', login_required(
        views.ComprasServiciosUpdate.as_view()), name='compras_servicios_editar'),

    path('compras-servicios/historico', login_required(
        views.HistoricoLicencias.as_view()), name='compras_servicios_historico'),

    path(route='compras-servicios/<pk>/eliminar/',
         view=login_required(views.ComprasServiciosDelete.as_view()),
         name='compras_servicios_eliminar'),

    path(route='compras-servicios/<pk>/reportes/',
         view=login_required(views.ReporteComprasServicios.as_view()),
         name='cs_pdf'),
]
