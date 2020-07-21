from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from licencias import views

urlpatterns = [
    path('usuario/licencia/solicitar', login_required(
        views.LicenciaSolicitud.as_view()), name='licencia_solicitud'),
]