from django.urls import path
from django.contrib.auth.decorators import login_required
from comisionApp import views

urlpatterns = [
    path(route='usuario/anticipo/solicitud/reporte',
         view=views.ReportePdfSolicitud.as_view(),
         name='reportePdfSolicitud'),

    path(route='usuario/anticipo/reporte',
         view=views.ReportePdfAnticipo.as_view(),
         name='reportePdfAnticipo'),
        
    path(route='usuario/anticipo/reporte/<pk>/',
         view=views.ReportePdfAnticipo.as_view(),
         name='reportePdfAnticipo'),

    path('usuario/anticipo/comisión', login_required(
        views.confeccionAnticipo), name='confeccion_comisión'),

    path('usuario/anticipo/solicitud', login_required(
        views.confeccionSolicitudComision), name='confeccion_solicitud_comisión'),

    path('usuario/anticipo/historico', login_required(
        views.historicoAnticipos), name='historico_anticipo'),
    
    path('usuario/archivar', login_required(
        views.archivar), name='archivar'),

    path('usuario/get_patente', login_required(
        views.get_patente), name='get_patente'),
    
    path('usuario/get_num_afiliado', login_required(
        views.get_num_afiliado), name='get_num_afiliado'),
        
    path('usuario/get_num_comisión', login_required(
        views.get_num_comision), name='get_num_comision'),
]
