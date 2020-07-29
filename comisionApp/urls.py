from django.urls import path
from django.contrib.auth.decorators import login_required
from comisionApp import views

urlpatterns = [
    # Solicitudes
    path(route='usuarios/anticipos/solicitudes/reportes',
         view=views.ReportePdfSolicitud.as_view(),
         name='reportePdfSolicitud'),

    path(route='usuarios/anticipos/<pk>/solicitudes/reportes',
         view=views.ReportePdfSolicitud.as_view(),
         name='reportePdfSolicitud'),

    path(route='usuarios/solicitudes/<pk>/eliminar/',
         view=views.EliminarSolicitud.as_view(),
         name='solicitud_eliminar'),

    path(route='usuarios/anticipos/solicitudes',
         view=login_required(views.confeccionSolicitudComision),
         name='confeccion_solicitud_comisión'),

    path(route='usuarios/anticipos/solicitudes/archivar',
         view=login_required(views.archivarSolicitud),
         name='archivar_solicitud'),

    path(route='usuarios/anticipos/historico/solicitudes',
         view=login_required(views.HistoricoSolicitudes.as_view()),
         name='historico_solicitud'),

    # Anticipos
    path(route='usuarios/anticipos/reportes',
         view=views.ReportePdfAnticipo.as_view(),
         name='reportePdfAnticipo'),

    path(route='usuarios/anticipos/<pk>/reportes/',
         view=views.ReportePdfAnticipo.as_view(),
         name='reportePdfAnticipo'),

    path(route='usuarios/anticipos/<pk>/eliminar/',
         view=views.EliminarAnticipo.as_view(),
         name='eliminar_anticipo'),

    path(route='usuarios/anticipos/comisiones',
         view=login_required(views.confeccionAnticipo),
         name='confeccion_comisión'),



    path(route='usuarios/anticipos/historico',
         view=login_required(views.HistoricoAnticipos.as_view()),
         name='historico_anticipo'),

    path(route='usuarios/anticipos/archivar',
         view=login_required(views.archivar),
         name='archivar'),

    path(route='usuario/get_patente',
         view=login_required(views.get_patente),
         name='get_patente'),

    path(route='usuario/get_num_afiliado',
         view=login_required(views.get_num_afiliado),
         name='get_num_afiliado'),
]
