from django.urls import path
from django.contrib.auth.decorators import login_required
from comisionApp import views

urlpatterns = [
     path(route='accounts/reporte_pdf',
         view=views.ReportePdf.as_view(),
         name='reporte_pdf'),
         
     path(route='accounts/reporte_pdf2',
         view=views.ReportePdf2.as_view(),
         name='reporte_pdf2'),
     
     path('historico_anticipo', login_required(
        views.historicoAnticipos), name='historico_anticipo'),
]
