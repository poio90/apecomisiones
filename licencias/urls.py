from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from licencias import views

urlpatterns = [
    path('usuarios/licencias/solicitudes', login_required(
        views.LicenciaSolicitud.as_view()), name='licencias_solicitud'),

    path('usuarios/licencias/historico', login_required(
        views.HistoricoLicencias.as_view()), name='licencias_historico'),

    path(route='usuarios/licencias/<pk>/eliminar/',
         view=views.EliminarLicencia.as_view(),
         name='licencias_eliminar'),

    path(route='usuarios/licencias/<pk>/reportes/',
         view=views.ReportePdfLicencia.as_view(),
         name='licencias_pdf'),
]
