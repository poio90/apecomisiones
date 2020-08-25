import time
import datetime
from datetime import date, datetime
from io import BytesIO, StringIO
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import View, CreateView, DeleteView, ListView, TemplateView, UpdateView
from django.http import HttpResponse, JsonResponse, request
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

# Create your views here.


class LicenciaSolicitud(SuccessMessageMixin,CreateView):
    model = Licencia
    form_class = FormLicencia
    context_object_name = 'licencia'
    template_name = 'licencias/licencia.html'
    success_url = reverse_lazy('licencias:licencias_historico')
    success_message = "La solicitud de licencia ha sido creada exitosamente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('licencias:licencias_pdf')
        context['title'] = 'Imprimir'
        context['method'] = 'POST'
        context['target'] = '_blank'
        context['atr'] = 'btn-success'
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super(LicenciaSolicitud, self).form_valid(form)


class LicenciaEditar(UpdateView):
    model = Licencia
    form_class = FormLicencia
    context_object_name = 'licencia'
    template_name = 'licencias/licencia.html'
    success_url = reverse_lazy('licencias:licencias_historico')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('licencias:licencias_historico')
        context['title'] = 'Cancelar'
        context['method'] = 'GET'
        context['target'] = '_self'
        context['atr'] = 'btn-danger'
        return context


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

    def get(self, request, *args, **kwargs):

        licencia = Licencia.objects.get(pk=kwargs['pk'])

        buffer = BytesIO()

        response = HttpResponse(content_type='application/pdf')
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
        Story = []
        logotipo = "static/dist/img/escudo.jpeg"

        nombreRevista = "Programación Avanzada"
        numero = 4
        precio = "10.00"
        fechaLimite = "27/09/2017"
        obsequio = "Taller de Python"

        formatoFecha = time.ctime()
        nombreCompleto = self.request.user.last_name

        imagen = Image(logotipo, 1 * inch, 1 * inch)
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

        texto = 'Santa Rora, ' + str(fecha_solicitud)
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

    def post(self, request, *args, **kwargs):

        dias_habiles_acum = request.POST['dias_habiles_acum']
        dias_habiles_agregar = request.POST['dias_habiles_agregar']
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']
        fecha_reintegro = request.POST['fecha_reintegro']

        buffer = BytesIO()
        response = HttpResponse(content_type='application/pdf')

        doc = SimpleDocTemplate(buffer, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
        Story = []
        logotipo = "static/dist/img/escudo.jpeg"

        nombreRevista = "Programación Avanzada"
        numero = 4
        precio = "10.00"
        fechaLimite = "27/09/2017"
        obsequio = "Taller de Python"

        formatoFecha = time.ctime()
        nombreCompleto = self.request.user.last_name

        imagen = Image(logotipo, 1 * inch, 1 * inch)
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

        Story.append(Spacer(1, 12))

        texto = 'El que suscribe, agente ' + request.user.last_name + ' '+request.user.first_name + ' dependiente de Gerencia de \
                Explotación solicita ' + dias_habiles_acum + ' días hábiles, comenzando a hacer uso de la misma desde el '\
                + fecha_inicio + ' hasta el ' + fecha_fin + ', a la cual se le agregarán '\
                + dias_habiles_agregar + ' días hábiles en concepto de traslado reintegrándome a mis\
                funciones el día ' + fecha_reintegro + '.'
        Story.append(Paragraph(texto, estilos["Normal"]))
        Story.append(Spacer(1, 60))

        fecha = date.today().strftime("%d/%m/%Y")

        texto = 'Santa Rora, ' + str(fecha)
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
