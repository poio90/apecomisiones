from django.urls import path
from django.contrib.auth.decorators import login_required
from comisionApp import views

urlpatterns = [
    path(route='usuarios/anticipos/solicitudes/reportes',
         view=views.ReportePdfSolicitud.as_view(),
         name='reportePdfSolicitud'),

    path(route='usuarios/anticipos/reportes',
         view=views.ReportePdfAnticipo.as_view(),
         name='reportePdfAnticipo'),

    path(route='usuarios/anticipos/<pk>/reportes/',
         view=views.ReportePdfAnticipo.as_view(),
         name='reportePdfAnticipo'),

    path(route='usuarios/anticipos/<pk>/eliminar/',
         view=views.EliminarAnticipo.as_view(),
         name='eliminar_anticipo'),

    path('usuarios/anticipos/comisiones', login_required(
        views.confeccionAnticipo), name='confeccion_comisión'),

    path('usuarios/anticipos/solicitudes', login_required(
        views.confeccionSolicitudComision), name='confeccion_solicitud_comisión'),

    path('usuarios/anticipos/historico/solicitudes', login_required(
        views.HistoricoSolicitudes.as_view()), name='historico_solicitud'),

    path('usuarios/anticipos/historico', login_required(
        views.HistoricoAnticipos.as_view()), name='historico_anticipo'),

    path('usuarios/anticipos/archivar', login_required(
        views.archivar), name='archivar'),

    path('usuarios/anticipos/solicitudes/archivar', login_required(
        views.archivarSolicitud), name='archivar_solicitud'),

    path('usuario/get_patente', login_required(
        views.get_patente), name='get_patente'),

    path('usuario/get_num_afiliado', login_required(
        views.get_num_afiliado), name='get_num_afiliado'),

]
