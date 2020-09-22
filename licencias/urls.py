from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from licencias import views

urlpatterns = [
    path('licencias/solicitudes/', login_required(
        views.LicenciaSolicitud.as_view()), name='licencias_solicitud'),

    path('licencias/<pk>/editar/', login_required(
        views.LicenciaEditar.as_view()), name='licencias_editar'),

    path('licencias/historico', login_required(
        views.HistoricoLicencias.as_view()), name='licencias_historico'),

    path(route='licencias/<pk>/eliminar/',
         view=login_required(views.EliminarLicencia.as_view()),
         name='licencias_eliminar'),

    path(route='licencias/<pk>/reportes/',
         view=login_required(views.ReportePdfLicencia.as_view()),
         name='licencias_pdf'),

    path(route='licencias/reportes/',
         view=(views.ReportePdfLicencia.as_view()),
         name='licencias_pdf'),
]
