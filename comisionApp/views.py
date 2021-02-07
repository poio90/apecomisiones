import datetime
from datetime import date, datetime
from django.db import transaction
from django.forms import formset_factory
from io import BytesIO
from django.db.utils import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import *
from django.http import HttpResponse, JsonResponse, request
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .forms import *
from comisionManager.settings import STATICFILES_DIRS
from usuarios.forms import UserForm
from usuarios.models import User
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import cm, inch
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.rl_config import defaultPageSize
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer
from django.core import serializers
import json


class ReportePdfSolicitud(View):
    """Regresa Pdf"""

    def get(self, request, *args, **kwargs):
        solicitud = Solicitud.objects.get(pk=kwargs['pk'])
        integrantes = Integrantes_x_Solicitud.objects.filter(
            solicitud_id=kwargs['pk'])

        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)

        # Header
        logo = ImageReader(STATICFILES_DIRS[0] + '/dist/img/logoApe.png')
        c.drawImage(logo, 30, 750,  1 * inch, 1 * inch)

        text = 'Administración Provincial de Energía de La Pampa'
        text2 = 'Departamento Telecontrol'
        c.setFont('Helvetica', 12)
        c.drawString(120, 790, text)
        c.drawString(120, 775, text2)

        PAGE_WIDTH = defaultPageSize[0]
        PAGE_HEIGHT = defaultPageSize[1]

        text = 'Solicitud de Anticipo'

        width = stringWidth(text, 'Helvetica', 16)
        x = (PAGE_WIDTH/2)-(width/2)

        c.setLineWidth(.3)
        c.setFont('Helvetica', 18)
        c.drawString(x, 730, text)
        c.setFont('Helvetica', 12)

        fecha = date.today().strftime("%d/%m/%Y")

        fecha_pedido = datetime.strptime(
            str(solicitud.fecha_pedido), "%Y-%m-%d").strftime("%d/%m/%Y")

        c.drawString(400, 700, 'Fecha de pedido: ' + str(fecha_pedido))

        alto = 675
        for i in range(len(integrantes)):
            c.drawString(30, alto, 'Apellido y Nombre'+'     ' +
                         integrantes[i].user.get_full_name())
            c.drawString(360, alto, 'N° Afiliado a SEMPRE' +
                         '         ' + integrantes[i].user.num_afiliado)
            alto = alto - 25

        c.drawString(30, 475, 'Motivo de la comisión: ')
        # Funcion que agrega saltos de linea a 'motivo' para que se pinte en el pdf
        j = 0
        n = 87
        story = ''
        for i in range(len(solicitud.motivo)):
            if solicitud.motivo[i] == '\n':
                n = i + 86
            if i == n:
                story = story + solicitud.motivo[j:n] + '\n'
                j = n
                n = n + 86
        story = story + solicitud.motivo[j:len(solicitud.motivo)]

        # Texto que va contenido dentro de los detalles de trabajo
        textobject = c.beginText()
        textobject.setTextOrigin(35, 455)
        textobject.setFont("Courier", 10)
        textobject.textLines(story)
        c.drawText(textobject)

        fecha_inicio = datetime.strptime(
            str(solicitud.fecha_inicio), "%Y-%m-%d").strftime("%d/%m/%Y")

        c.setFont('Helvetica', 12)
        c.drawString(30, 295, 'Fecha de iniciación: ' +
                     str(fecha_inicio))
        c.drawString(320, 295, 'Duracón prevista: ' +
                     solicitud.duracion_prevista)
        c.drawString(
            30, 265, 'Lugar de residencia durante la comisión: '+solicitud.ciudad.ciudad)
        c.drawString(30, 235, 'Medio de transporte')
        c.drawString(200, 235, 'Unidad de legajo: ' +
                     solicitud.transporte.num_legajo)
        c.drawString(400, 235, 'Patente: '+solicitud.transporte.patente)
        c.drawString(30, 205, 'Gastos a solicitar: $' +
                     str(solicitud.gastos_previstos))
        solicitante = solicitud.creado_por.get_full_name()
        c.drawString(30, 175, 'Anticipo ordenado por: ' + solicitante)

        c.drawString(500, 20, 'Firma')
        c.line(465, 32, 570, 32)

        c.save()
        titulo = 'filename=' + str(fecha)+'.pdf'
        pdf = buffer.getvalue()
        buffer.close()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = titulo
        return response


class ReportePdfAnticipo(View):

    def get(self, request, *args, **kwargs):
        anticipo = Anticipo.objects.get(pk=kwargs['pk'])
        itineraio = Itinerario.objects.filter(anticipo_id=kwargs['pk'])
        det_trabajo = DetalleTrabajo.objects.get(anticipo_id=kwargs['pk'])
        int_x_ant = Integrantes_x_Anticipo.objects.filter(
            anticipo_id=kwargs['pk'])

        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)

        logo = ImageReader(STATICFILES_DIRS[0] + '/dist/img/logoApe.png')
        c.drawImage(logo, 30, 788,  0.45 * inch, 0.45 * inch)

        c.setFont('Helvetica', 8)
        c.drawString(65, 805, 'Departamento')
        c.drawString(65, 795, 'de Telecontrol')

        PAGE_WIDTH = defaultPageSize[0]
        PAGE_HEIGHT = defaultPageSize[1]

        text = 'Rendicion de comisión N° ___________'

        width = stringWidth(text, 'Helvetica', 16)
        x = (PAGE_WIDTH/2)-(width/2)

        # Header
        c.setLineWidth(.3)
        c.setFont('Helvetica', 18)
        c.drawString(x, 800, text)

        alto = 770

        c.setFont('Helvetica', 12)
        for i in range(len(int_x_ant)):
            c.drawString(30, alto, 'Apellido y Nombre'+'     ' +
                         int_x_ant[i].user.get_full_name())
            c.drawString(360, alto, 'N° Afiliado a SEMPRE' +
                         '         ' + int_x_ant[i].user.num_afiliado)
            alto = alto - 25

        fecha_inicio = datetime.strptime(
            str(anticipo.fecha_inicio), "%Y-%m-%d").strftime("%d/%m/%Y")
        fecha_fin = datetime.strptime(
            str(anticipo.fecha_fin), "%Y-%m-%d").strftime("%d/%m/%Y")

        c.drawString(30, 620, 'Fecha de inicio: ' + fecha_inicio)
        c.drawString(320, 620, 'Fecha de finalización: ' + fecha_fin)
        c.drawString(
            30, 595, 'Lugar de residencia durante la comisión: ' + int_x_ant[0].anticipo.ciudad.ciudad)
        c.drawString(30, 570, 'Medio de transporte')
        c.drawString(200, 570, 'Unidad de legajo: ' +
                     int_x_ant[0].anticipo.transporte.num_legajo)
        c.drawString(400, 570, 'Patente: ' +
                     int_x_ant[0].anticipo.transporte.patente)
        c.drawString(30, 545, 'Gastos: $' + str(int_x_ant[0].anticipo.gastos))

        # tabla.encabezado
        styles = getSampleStyleSheet()
        styleBH = styles["Normal"]
        styleBH.fontSize = 10

        nombre = Paragraph('''Apellido y Nombre''', styleBH)
        dia = Paragraph('''Día''', styleBH)
        mes = Paragraph('''Mes''', styleBH)
        sal = Paragraph('''Salida de''', styleBH)
        h1 = Paragraph('''Horario''', styleBH)
        llegada = Paragraph('''Llegada de''', styleBH)
        h2 = Paragraph('''Horario''', styleBH)

        data = []
        data.append([nombre, dia, mes, sal, h1, llegada, h2])

        styleN = styles["BodyText"]
        styleN.alignment = TA_CENTER
        styleN.fontSize = 7

        # tabla.contenico
        comisiones = []
        for i in range(len(itineraio)):
            comisiones.append({'name': itineraio[i].nombre_afiliado, 'b1': itineraio[i].dia, 'b2': itineraio[i].mes, 'b3': itineraio[i].salida,
                               'b4': itineraio[i].hora_salida, 'b5': itineraio[i].llegada, 'b6': itineraio[i].hora_llegada, })

        hight1 = 505

        for part in comisiones:
            this_part = [part['name'], part['b1'], part['b2'],
                         part['b3'], part['b4'], part['b5'], part['b6']]
            data.append(this_part)
            hight1 = hight1 - 18

        width, height = A4
        table = Table(data, colWidths=[
                      5 * cm, 1.5 * cm, 1.5 * cm, 3.8 * cm, 1.7 * cm, 3.8 * cm, 1.7 * cm])
        table.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ]))

        table.wrapOn(c, width, height)
        table.drawOn(c, 30, hight1)

        # informe de comision
        c.setFont('Helvetica', 16)
        c.drawString(30, 245, 'Informe de Anticipo ')

        #c.setFont('Helvetica', 12)
        #c.drawString(32, 220, 'km Salida: '+str(det_trabajo.km_salida))
        #c.drawString(180, 220, 'km Llegada: '+str(det_trabajo.km_llegada))
        # c.drawString(350, 220, 'Total km recorrido: ' +
        #            str(det_trabajo.km_llegada-det_trabajo.km_salida))

        # Lineas Verticales
        c.line(30, 237, 30, 50)
        c.line(565, 50, 565, 237)

        # Lineas Horizontales
        c.line(30, 237, 565, 237)
        #c.line(30, 210, 565, 210)
        c.line(30, 50, 565, 50)

        c.setFont('Helvetica', 12)
        c.drawString(35, 220, 'NOTA: ')

        # Funcion que agrega saltos de linea
        j = 0
        n = 87
        story = ''
        for i in range(len(det_trabajo.detalle_trabajo)):
            if det_trabajo.detalle_trabajo[i] == '\n':
                n = i + 87
            if i == n:
                story = story + det_trabajo.detalle_trabajo[j:n] + '\n'
                j = n
                n = n + 87
        story = story + \
            det_trabajo.detalle_trabajo[j:len(det_trabajo.detalle_trabajo)]

        # Texto que va contenido dentro de los detalles de trabajo
        textobject = c.beginText()
        textobject.setTextOrigin(35, 208)
        textobject.setFont("Courier", 10)
        textobject.textLines(story)
        c.drawText(textobject)

        firm = 'Firma:'
        width = stringWidth(firm, 'Helvetica', 12)
        c.setFont('Helvetica', 12)
        x = (PAGE_WIDTH/2)-(width/2)
        c.drawString(x, 15, firm)
        c.line(200, 27, 400, 27)
        c.showPage()

        c.save()
        pdf = buffer.getvalue()
        buffer.close()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'filename=Anticipo.pdf'
        return response


# Esta vista podria escribirla como la de update pero asi anda bien
class SolicitudAnticipoCreate(CreateView):
    model = Solicitud
    template_name = 'comisiones/solicitud.html'
    form_class = SolicitudForm

    def get_context_data(self, **kwargs):
        data = super(SolicitudAnticipoCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['users'] = SolicitudFormSet(self.request.POST)
        else:
            data['users'] = SolicitudFormSet()
            data['single_user'] = CollectionUserForm()
            data['list_url'] = reverse_lazy('comisiones:solicitud_anticipo')
            data['url'] = reverse_lazy('comisiones:historico_comisiones')
        return data

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            users = SolicitudFormSet(request.POST)
            if form.is_valid():
                if users.is_valid():
                    self.object = form.save()
                    with transaction.atomic():
                        form.instance.creado_por = self.request.user
                        self.object = form.save()
                        users.instance = self.object
                        users.save()
                        data['pdf_url'] = reverse_lazy(
                            'comisiones:reportePdfSolicitud', kwargs={'pk': self.object.pk})
                        data['success_message'] = 'Solicitud de anticipo creada exitosamente'
                else:
                    data['error'] = 'Está intentando cargar un usuario más de una vez.'
            else:
                data = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_success_url(self):
        return reverse_lazy('comisiones:historico_comisiones')


class SolicitudAnticipoUpdate(UpdateView):
    model = Solicitud
    template_name = 'comisiones/solicitud.html'
    form_class = SolicitudForm

    def get_context_data(self, **kwargs):
        data = super(SolicitudAnticipoUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['users'] = SolicitudFormSet(
                self.request.POST, instance=self.object)
        else:
            data['users'] = SolicitudFormSet(instance=self.object)
            data['single_user'] = CollectionUserForm()
            data['list_url'] = reverse_lazy(
                'comisiones:solicitud_editar', kwargs={'pk': self.object.pk})
            data['url'] = reverse_lazy('comisiones:historico_comisiones')
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        data = {}
        try:
            users = context['users']
            if users.is_valid():
                with transaction.atomic():
                    self.object = form.save()
                    users.instance = self.object
                    users.save()
                    data['pdf_url'] = reverse_lazy(
                        'comisiones:reportePdfSolicitud', kwargs={'pk': self.object.pk})
                    data['success_message'] = 'Cambios realizados con éxito'
            else:
                data['error'] = 'Está intentando cargar usuario más de una vez.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def form_invalid(self, form):
        data = {}
        data['error'] = form.errors
        return JsonResponse(data)

    def get_success_url(self):
        return reverse_lazy('comisiones:historico_comisiones')


class RendicionAnticipoCreate(CreateView):
    model = Anticipo
    template_name = 'comisiones/rendicion.html'
    form_class = RendicionForm

    def get_context_data(self, **kwargs):
        data = super(RendicionAnticipoCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['users'] = RendicionFormSet(self.request.POST)
            data['detalle'] = DetalleTrabajoForm(self.request.POST)
            data['itinerario'] = ItinerarioFormSet(self.request.POST)
        else:
            data['users'] = RendicionFormSet()
            data['single_user'] = CollectionUserForm()
            data['single_user'].fields['user'].queryset = User.objects.all().order_by(
                'last_name').filter(is_active=1).exclude(pk=self.request.user.pk)
            data['detalle'] = DetalleTrabajoForm()
            data['itinerario'] = ItinerarioFormSet()
            data['list_url'] = reverse_lazy('comisiones:rendicion_anticipo')
            data['url'] = reverse_lazy('comisiones:historico_comisiones')
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        data = {}
        try:
            users = context['users']
            itinerario = context['itinerario']
            detalle = context['detalle']
            if users.is_valid():
                if itinerario.is_valid():
                    if detalle.is_valid():
                        with transaction.atomic():
                            self.object = form.save()
                            users.instance = self.object
                            detalle.instance.anticipo = self.object
                            itinerario.instance = self.object
                            users.save()
                            itinerario.save()
                            detalle.save()
                            data['pdf_url'] = reverse_lazy(
                                'comisiones:reportePdfAnticipo', kwargs={'pk': self.object.pk})
                            data['success_message'] = 'Rendición de anticipo creada exitosamente'
                    else:
                        data['error'] = 'Revise los campos del informe de anticipo.'
                else:
                    data['error'] = 'Revise los campos del itinerario de viaje.'
            else:
                data['error'] = 'Está intentando cargar un usuario más de una vez.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def form_invalid(self, form):
        return JsonResponse(form.errors)

    def get_success_url(self):
        return reverse_lazy('comisiones:historico_comisiones')


class RendicionAnticipoUpdate(UpdateView):
    model = Anticipo
    template_name = 'comisiones/rendicion.html'
    form_class = RendicionForm

    def get_context_data(self, **kwargs):
        data = super(RendicionAnticipoUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['users'] = RendicionFormSet(
                self.request.POST, instance=self.object)
            data['detalle'] = DetalleTrabajoForm(
                self.request.POST, instance=self.object.detalletrabajo)
            data['itinerario'] = ItinerarioFormSet(
                self.request.POST, instance=self.object)
        else:
            data['users'] = RendicionFormSet(instance=self.object)
            data['single_user'] = CollectionUserForm()
            data['detalle'] = DetalleTrabajoForm(
                instance=self.object.detalletrabajo)
            data['itinerario'] = ItinerarioFormSet(instance=self.object)
            data['list_url'] = reverse_lazy(
                'comisiones:anticipo_editar', kwargs={'pk': self.object.pk})
            data['url'] = reverse_lazy('comisiones:historico_comisiones')
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        data = {}
        try:
            users = context['users']
            itinerario = context['itinerario']
            detalle = context['detalle']
            if users.is_valid():
                if itinerario.is_valid():
                    if detalle.is_valid():
                        with transaction.atomic():
                            self.object = form.save()
                            users.instance = self.object
                            detalle.instance.anticipo = self.object
                            itinerario.instance = self.object
                            users.save()
                            itinerario.save()
                            detalle.save()
                            data['pdf_url'] = reverse_lazy(
                                'comisiones:reportePdfAnticipo', kwargs={'pk': self.object.pk})
                            data['success_message'] = 'Cambios realizados con éxito'
                    else:
                        data['error'] = itinerario.errors
                else:
                    data['error'] = 'Revise los campos del itinerario de viaje.'
            else:
                data['error'] = 'Está intentando cargar un usuario más de una vez.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def form_invalid(self, form):
        data = {}
        data['error'] = form.errors
        return JsonResponse(data)

    def get_success_url(self):
        return reverse_lazy('comisiones:historico_comisiones')


class Historicos(ListView):
    model = Anticipo
    context_object_name = 'anticipos'
    template_name = 'comisiones/historico.html'

    def get_queryset(self):
        return Anticipo.objects.filter(integrantes_x_anticipo__user=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['solicitudes'] = Solicitud.objects.filter(
            integrantes_x_solicitud__user=self.request.user.pk)
        context['solicitudes_pedidas'] = Solicitud.objects.filter(
            creado_por_id=self.request.user.pk)
        return context


class EliminarAnticipo(DeleteView):
    model = Anticipo
    context_object_name = 'anticipo'
    template_name = 'comisiones/eliminar_anticipo.html'
    success_url = reverse_lazy('comisiones:historico_comisiones')
    success_message = "Anticipo de comisión eliminado exitosamente"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        integrantes_x_anticipo = Integrantes_x_Anticipo.objects.filter(
            anticipo_id=self.kwargs['pk'])
        integrantes_x_anticipo.delete()
        return super(EliminarAnticipo, self).delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'Anticipo'
        context['list_url'] = reverse_lazy('comisiones:historico_comisiones')
        return context


class EliminarSolicitud(DeleteView):
    model = Solicitud
    context_object_name = 'solicitud'
    template_name = 'comisiones/eliminar_solicitud.html'
    success_url = reverse_lazy('comisiones:historico_comisiones')
    success_message = "Solicitud de comisión eliminada exitosamente"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(EliminarSolicitud, self).delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'Solicitud'
        context['list_url'] = reverse_lazy('comisiones:historico_comisiones')
        return context


class Error404View(TemplateView):
    template_name = 'error_404.html'


class Error500View(TemplateView):
    template_name = 'error_500.html'

    @classmethod
    def as_error_view(cls):
        v = cls.as_view()

        def view(request):
            r = v(request)
            r.render()
            return r
        return view


@login_required
def get_patente(request):
    pk_transporte = request.GET.get('transporte', None)
    data = list(Transporte.objects.filter(pk=pk_transporte).values('patente'))
    return JsonResponse({'data': data})


@login_required
def get_num_afiliado(request):
    data = {}
    try:
        pk = request.GET.get('pk')
        data['num_afiliado'] = list(
            User.objects.filter(pk=pk).values('num_afiliado'))
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data)
