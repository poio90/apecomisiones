from django.urls import path
from django.contrib.auth.decorators import login_required
from comisionApp import views

urlpatterns = [
    # Solicitudes
    path(route='comisiones/solicitudes/reportes',
         view=views.ReportePdfSolicitud.as_view(),
         name='reportePdfSolicitud'),

    path(route='comisiones/<pk>/solicitudes/reportes',
         view=views.ReportePdfSolicitud.as_view(),
         name='reportePdfSolicitud'),

    path(route='solicitudes/<pk>/eliminar/',
         view=views.EliminarSolicitud.as_view(),
         name='solicitud_eliminar'),

    path(route='comisiones/solicitudes',
         view=views.SolicitudAnticipo.as_view(),
         name='solicitud_anticipo'),

    path(route='comisiones/historico',
         view=views.Historicos.as_view(),
         name='historico_comisiones'),
#####################################################
     path(route='comisiones/solicitudes/prueba',
         view=views.RendicionAnticipo.as_view(),
         name='solicitud_prueba'),
         #####################################

    # Anticipos
    path(route='comisiones/anticipos/reportes',
         view=views.ReportePdfAnticipo.as_view(),
         name='reportePdfAnticipo'),

    path(route='comisiones/anticipos/<pk>/reportes/',
         view=views.ReportePdfAnticipo.as_view(),
         name='reportePdfAnticipo'),

    path(route='comisiones/anticipos/<pk>/eliminar/',
         view=views.EliminarAnticipo.as_view(),
         name='eliminar_anticipo'),

    path(route='comisiones/anticipos',
         view=views.RendicionAnticipo.as_view(),
         name='rendicion_anticipo'),

    path(route='get_patente',
         view=login_required(views.get_patente),
         name='get_patente'),

    path(route='usuario/get_num_afiliado',
         view=login_required(views.get_num_afiliado),
         name='get_num_afiliado'),
]