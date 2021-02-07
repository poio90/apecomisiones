import os
import time
import datetime
from datetime import date, datetime
from io import BytesIO, StringIO
from django.db import transaction
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import View, CreateView, DeleteView, ListView, TemplateView, UpdateView
from django.http import HttpResponse, JsonResponse, request
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import cm, inch
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.rl_config import defaultPageSize
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer
from .models import *
from .forms import FormLicencia
from comisionManager.settings import STATICFILES_DIRS

# Create your views here.


class LicenciaSolicitud(CreateView):
    model = Licencia
    form_class = FormLicencia
    context_object_name = 'licencia'
    template_name = 'licencias/licencia.html'

    def get_context_data(self, **kwargs):
        context = super(LicenciaSolicitud, self).get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('licencias:licencias_solicitud')
        context['url'] = reverse_lazy('licencias:licencias_historico')
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            if form.is_valid():
                with transaction.atomic():
                    object = form.save(commit=False)
                    object.user = self.request.user
                    object.save()
                    data['pdf_url'] = reverse_lazy(
                        'licencias:licencias_pdf', kwargs={'pk': object.pk})
                data['success_message'] = 'Solicitud de licencia creada exitosamente'
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


class LicenciaUpdate(UpdateView):
    model = Licencia
    form_class = FormLicencia
    context_object_name = 'licencia'
    template_name = 'licencias/licencia.html'

    """Con esto evito que se cree un nuevo registro en la base de datos"""

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LicenciaUpdate, self).get_context_data(**kwargs)
        context['list_url'] = reverse_lazy(
            'licencias:licencias_editar', kwargs={'pk': self.object.pk})
        context['url'] = reverse_lazy('licencias:licencias_historico')
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            if form.is_valid():
                with transaction.atomic():
                    object = form.save()
                    data['pdf_url'] = reverse_lazy(
                        'licencias:licencias_pdf', kwargs={'pk': object.pk})
                    data['success_message'] = 'Cambios realizados con éxito'
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


class HistoricoLicencias(ListView):
    model = Licencia
    context_object_name = 'licencias'
    template_name = 'licencias/historico_licencias.html'

    def get_queryset(self):
        return Licencia.objects.filter(user=self.request.user)


class EliminarLicencia(DeleteView):
    model = Licencia
    context_object_name = 'licencia'
    template_name = 'licencias/eliminar_licencia.html'
    success_url = reverse_lazy('licencias:licencias_historico')
    success_message = "La solicitud de licencia ha sido eliminada exitosamente"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(EliminarLicencia, self).delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'Licencia'
        context['list_url'] = reverse_lazy('licencias:licencias_historico')
        return context


class ReportePdfLicencia(View):

    template_name = 'licencias/licencia.html'

    def get(self, request, *args, **kwargs):

        licencia = Licencia.objects.get(pk=kwargs['pk'])
        buffer = BytesIO()
        response = HttpResponse(content_type='application/pdf')
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
        Story = []
        logotipo = STATICFILES_DIRS[0] + "/dist/img/escudo.jpeg"

        formatoFecha = time.ctime()
        nombreCompleto = self.request.user.last_name + ' ' + request.user.first_name

        imagen = Image(os.path.realpath(logotipo), 1 * inch, 1 * inch)
        Story.append(imagen)

        estilos = getSampleStyleSheet()
        estilos.add(ParagraphStyle(name='Justify', alignment=TA_CENTER))

        titulo = "PROVINCIA DE LA PAMPA"
        Story.append(Paragraph(titulo, estilos["Justify"]))
        titulo = "MINISTERIO DE OBRAS Y SERVICIOS PÚBLICOS "
        Story.append(Paragraph(titulo, estilos["Justify"]))
        titulo = "ADMINISTRACIÓN PROVINCIAL DE ENERGÍA"
        Story.append(Paragraph(titulo, estilos["Justify"]))
        Story.append(Spacer(1, 36))
        titulo = "SOLICITUD ANUAL DE LICENCIA ORDINARIA"
        Story.append(Paragraph(titulo, estilos["Justify"]))
        Story.append(Spacer(1, -12))
        texto = '______________________________________'
        Story.append(Paragraph(texto, estilos["Justify"]))

        estilos = getSampleStyleSheet()
        estilos.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        #texto = '%s' % formatoFecha

        #Story.append(Paragraph(texto, estilos["Normal"]))
        #Story.append(Spacer(1, 12))

        fecha_inicio = datetime.strptime(
            str(licencia.fecha_inicio), "%Y-%m-%d").strftime("%d/%m/%Y")
        fecha_fin = datetime.strptime(
            str(licencia.fecha_fin), "%Y-%m-%d").strftime("%d/%m/%Y")
        fecha_reintegro = datetime.strptime(
            str(licencia.fecha_reintegro), "%Y-%m-%d").strftime("%d/%m/%Y")
        fecha_solicitud = datetime.strptime(
            str(licencia.fecha_solicitud), "%Y-%m-%d").strftime("%d/%m/%Y")

        Story.append(Spacer(1, 12))

        texto = 'El que suscribe, agente ' + licencia.user.last_name + ' '+licencia.user.first_name + ' dependiente de Gerencia de \
                Explotación solicita ' + str(licencia.dias_habiles_acum) + ' días hábiles, comenzando a hacer uso de la misma desde el '\
                + str(fecha_inicio) + ' hasta el ' + str(fecha_fin) + ', a la cual se le agregarán '\
                + str(licencia.dias_habiles_agregar) + ' días hábiles en concepto de traslado reintegrándome a mis\
                funciones el día ' + str(fecha_reintegro) + '.'
        Story.append(Paragraph(texto, estilos["Normal"]))
        Story.append(Spacer(1, 60))

        texto = licencia.ciudad.ciudad + ', ' + str(fecha_solicitud)
        Story.append(Paragraph(texto, estilos["Normal"]))
        Story.append(Spacer(1, -8))

        texto = '........................................'
        Story.append(Paragraph(texto, estilos["Normal"]))
        Story.append(Spacer(1, 1))
        texto = 'LUGAR Y FECHA'
        Story.append(Paragraph(texto, estilos["Normal"]))

        Story.append(Spacer(1, -24))
        estilos = getSampleStyleSheet()
        estilos.add(ParagraphStyle(name='Justify', alignment=TA_RIGHT))
        texto = '....................................'
        Story.append(Paragraph(texto, estilos["Justify"]))
        Story.append(Spacer(1, 1))
        texto = 'FIRMA DEL AGENTE'
        Story.append(Paragraph(texto, estilos["Justify"]))

        estilos = getSampleStyleSheet()
        estilos.add(ParagraphStyle(name='Justify', alignment=TA_CENTER))
        Story.append(Spacer(1, 12))
        texto = '__________________________________________________________________________________'
        Story.append(Paragraph(texto, estilos["Justify"]))

        Story.append(Spacer(1, 12))
        texto = 'AUTORIZADO:'
        Story.append(Paragraph(texto, estilos["Normal"]))
        Story.append(Spacer(1, 12))
        texto = 'SANTA ROSA, ............... DE ...................................... DE ...............'
        Story.append(Paragraph(texto, estilos["Normal"]))

        Story.append(Spacer(1, 60))
        texto = '.....................................................................'
        Story.append(Paragraph(texto, estilos["Normal"]))
        Story.append(Spacer(1, 1))
        texto = 'FIRMA Y SELLO JEFE DEPARTAMENTO'
        Story.append(Paragraph(texto, estilos["Normal"]))

        Story.append(Spacer(1, -24))
        estilos = getSampleStyleSheet()
        estilos.add(ParagraphStyle(name='Justify', alignment=TA_RIGHT))
        texto = '...............................................'
        Story.append(Paragraph(texto, estilos["Justify"]))
        Story.append(Spacer(1, 0))
        texto = 'FIRMA Y SELLO GERENTE'
        Story.append(Paragraph(texto, estilos["Justify"]))

        estilos = getSampleStyleSheet()
        estilos.add(ParagraphStyle(name='Justify', alignment=TA_CENTER))
        Story.append(Spacer(1, 12))
        texto = '__________________________________________________________________________________'
        Story.append(Paragraph(texto, estilos["Justify"]))

        Story.append(Spacer(1, 12))
        texto = 'EN LA FECHA ........../........../.......... HE SIDO NOTIFICADO.'
        Story.append(Paragraph(texto, estilos["Normal"]))

        Story.append(Spacer(1, 60))
        texto = '..................................................................'
        Story.append(Paragraph(texto, estilos["Justify"]))
        Story.append(Spacer(1, 1))
        texto = 'FIRMA DEL GERENTE'
        Story.append(Paragraph(texto, estilos["Justify"]))

        Story.append(Spacer(1, 12))
        doc.build(Story)

        response.write(buffer.getvalue())
        buffer.close()

        response['Content-Dispotition'] = 'filename=Reporte-Anticipo.pdf'
        return response

