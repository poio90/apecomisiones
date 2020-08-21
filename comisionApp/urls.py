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
         view=login_required(views.confeccionSolicitudComision),
         name='confeccion_solicitud_comisión'),

    path(route='comisiones/solicitudes/archivar',
         view=login_required(views.archivarSolicitud),
         name='archivar_solicitud'),

    path(route='comisiones/historico',
         view=login_required(views.historicos),
         name='historico_comisiones'),

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
         view=login_required(views.confeccionAnticipo),
         name='confeccion_comisión'),

    path(route='anticipos/archivar',
         view=login_required(views.archivar),
         name='archivar'),

    path(route='get_patente',
         view=login_required(views.get_patente),
         name='get_patente'),

    path(route='usuario/get_num_afiliado',
         view=login_required(views.get_num_afiliado),
         name='get_num_afiliado'),
]

"""path(route='usuarios/anticipos/historico/solicitudes',
         view=login_required(views.HistoricoSolicitudes.as_view()),
         name='historico_solicitud'),
         
     path(route='usuarios/anticipos/historico',
         view=login_required(views.HistoricoAnticipos.as_view()),
         name='historico_anticipo'),"""
