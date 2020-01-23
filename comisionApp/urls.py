from django.urls import path
from comisionApp import views

urlpatterns = [
  path(route='accounts/reporte_pdf',
         view=views.ReportePdf.as_view(),
         name='reporte_pdf'),
]