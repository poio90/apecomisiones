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
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.rl_config import defaultPageSize
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer
from .models import *
from .forms import *


class ComprasServiciosCreate(CreateView):
    model = ComprasServicios
    form_class = ComprasServiciosForm
    template_name = 'compras_servicios/compras_servicios.html'

    def get_context_data(self, **kwargs):
        context = super(ComprasServiciosCreate,
                        self).get_context_data(**kwargs)
        if self.request.POST:
            context['requerido'] = DetalleRequeridoFormSet(self.request.POST)
        else:
            context['list_url'] = reverse_lazy(
                'compras_servicios:compras_servicios_solicitud')
            context['url'] = reverse_lazy(
                'compras_servicios:compras_servicios_historico')
            context['requerido'] = DetalleRequeridoFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        data = {}
        try:
            requerido = context['requerido']
            if requerido.is_valid():
                with transaction.atomic():
                    self.object = form.save(commit=False)
                    self.object.user = self.request.user
                    self.object.save()
                    requerido.instance = self.object
                    requerido.save()
                    data['pdf_url'] = reverse_lazy(
                        'compras_servicios:cs_pdf', kwargs={'pk': self.object.pk})
                data['success_message'] = 'Solicitud de compras y servicios creada exitosamente'
            else:
                data['error'] = 'Revise los campos de detalles'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def form_invalid(self, form):
        return JsonResponse(form.errors)

    def get_success_url(self):
        return reverse_lazy('compras_servicios:compras_servicios_historico')


class ComprasServiciosUpdate(UpdateView):
    model = ComprasServicios
    form_class = ComprasServiciosForm
    template_name = 'compras_servicios/compras_servicios.html'

    def get_context_data(self, **kwargs):
        context = super(ComprasServiciosUpdate,
                        self).get_context_data(**kwargs)
        if self.request.POST:
            context['requerido'] = DetalleRequeridoFormSet(
                self.request.POST, instance=self.object)
        else:
            context['list_url'] = reverse_lazy(
                'compras_servicios:compras_servicios_editar', kwargs={'pk': self.object.pk})
            context['url'] = reverse_lazy(
                'compras_servicios:compras_servicios_historico')
            context['requerido'] = DetalleRequeridoFormSet(
                instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        data = {}
        try:
            requerido = context['requerido']
            if requerido.is_valid():
                with transaction.atomic():
                    self.object = form.save()
                    requerido.instance = self.object
                    requerido.save()
                    data['pdf_url'] = reverse_lazy(
                        'compras_servicios:cs_pdf', kwargs={'pk': self.object.pk})
                data['success_message'] = 'Cambios realizados con éxito'
            else:
                data['error'] = 'Revise los campos de detalles'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def form_invalid(self, form):
        return JsonResponse(form.errors)

    def get_success_url(self):
        return reverse_lazy('compras_servicios:compras_servicios_historico')


class ComprasServiciosDelete(DeleteView):
    model = ComprasServicios
    template_name = 'compras_servicios/eliminar_compras_servicios.html'
    success_url = reverse_lazy('compras_servicios:compras_servicios_historico')
    success_message = "Solicitud de compras y servicios eliminada exitosamente"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ComprasServiciosDelete, self).delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'ComprasServicios'
        context['list_url'] = reverse_lazy(
            'compras_servicios:compras_servicios_historico')
        return context


class HistoricoLicencias(ListView):
    model = ComprasServicios
    context_object_name = 'compras_servicios'
    template_name = 'compras_servicios/historial_compras_servicios.html'

    def get_queryset(self):
        return ComprasServicios.objects.filter(user=self.request.user)


class ReporteComprasServicios(View):

    def get(self, request, *args, **kwargs):

        compras_servicios = ComprasServicios.objects.get(pk=kwargs['pk'])
        detalle = DetalleRequerido.objects.filter(compras_servicios_id=kwargs['pk'])

        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)

        PAGE_WIDTH = defaultPageSize[0]
        PAGE_HEIGHT = defaultPageSize[1]

        # Header
        logo = ImageReader('static/dist/img/logoApe.png')
        c.drawImage(logo, 30, 757,  0.75 * inch, 0.75 * inch)

        text = 'Administracion Provincial de Energia'

        c.setFont('Helvetica', 8)
        c.drawString(90, 790, text)
        c.drawString(90, 780, 'Falucho n°585 - Santa Rosa - La Pampa')
        c.drawString(90, 770, 'Tel: (02954) 429590')

        # Esquina superior derecha
        # Lineas verticales
        c.line(400, 780, 400, 810)
        c.line(570, 810, 570, 780)
        # Lineas horizontales
        c.line(400, 810, 570, 810)
        c.line(570, 780, 400, 780)

        c.setFont('Helvetica', 10)
        c.drawString(
            410, 790, 'N° ....................... / .......................')

        # Transforma el formato de 99-99-9999 a 99/99/9999
        fecha_pedido = datetime.strptime(
            str(compras_servicios.fecha_pedido), "%Y-%m-%d").strftime("%d/%m/%Y")

        c.drawString(440, 760, 'Fecha: ' + str(fecha_pedido))

        # Cuadro.principal
        c.line(30, 750, 570, 750)
        c.line(570, 750, 570, 625)
        c.line(570, 625, 30, 625)
        c.line(30, 625, 30, 750)

        c.drawString(
            35, 737, 'REQUISICIÓN DE COMPRA DE BIENES Y/O SERVICIOS (COMPRA DIRECTA) / PRESUPUESTO')
        c.drawString(35, 723, 'MOTIVO DEL REQUERIMIENTO:')

        # Funcion que agrega saltos de linea a 'motivo' para que se pinte en el pdf
        j = 0
        n = 87
        story = ''
        for i in range(len(compras_servicios.motivo)):
            if compras_servicios.motivo[i] == '\n':
                n = i + 86
            if i == n:
                story = story + compras_servicios.motivo[j:n] + '\n'
                j = n
                n = n + 86
        story = story + \
            compras_servicios.motivo[j:len(compras_servicios.motivo)]

        # Texto que va contenido dentro de los detalles de trabajo
        textobject = c.beginText()
        textobject.setTextOrigin(35, 710)
        textobject.setFont("Courier", 10)
        textobject.textLines(story)
        c.drawText(textobject)

        # Cuandro.vehiculos
        c.setFont('Helvetica', 10)
        c.line(30, 667, 570, 666)
        c.drawString(35, 655, 'Sólo para reparación de vehículos:')

        # Funcion que agrega saltos de linea a 'motivo' para que se pinte en el pdf
        """j = 0
        n = 61
        story = ''
        for i in range(len(compras_servicios.motivo)):
            if compras_servicios.motivo[i] == '\n':
                n = i + 60
            if i == n:
                story = story + compras_servicios.motivo[j:n] + '\n'
                j = n
                n = n + 60
        story = story + compras_servicios.motivo[j:len(compras_servicios.motivo)]

        # Texto que va contenido dentro de los detalles de trabajo
        textobject = c.beginText()
        textobject.setTextOrigin(198, 655)
        textobject.setFont("Courier", 10)
        textobject.textLines(story)
        c.drawText(textobject)"""

        c.drawString(200, 632, 'N° de legajo:')
        c.drawString(380, 632, 'Dominio:')

        # tabla.encabezado
        styles = getSampleStyleSheet()
        styleBH = styles["Normal"]
        styleBH.fontSize = 10

        nombre = Paragraph('''DETALLE DE LO REQUERIDO''', styleBH)
        dia = Paragraph('''MONTO''', styleBH)

        data = []
        data.append([nombre, dia])

        styleN = styles["BodyText"]
        styleN.alignment = TA_CENTER
        styleN.fontSize = 7

        # tabla.contenico
        contenido = []
        # El rango determina la cantidad de cuadros que se pintan en el documento
        for i in range(11):
            contenido.append({'name': '', 'b1': '', })

        hight1 = 607 # comienzo de la tabla

        for part in contenido:
            this_part = [part['name'], part['b1'], ]
            data.append(this_part)
            hight1 = hight1 - 18

        width, height = A4
        table = Table(data, colWidths=[
                      15 * cm, 4.05 * cm, ])
        table.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ]))

        table.wrapOn(c, width, height)
        table.drawOn(c, 30, hight1)

        hight1 = 594
        delta = 18
        c.setFont('Helvetica', 9)
        monto_total = 0

        for i in range(len(detalle)):
            c.drawString(35, hight1, detalle[i].detalle_requerido)
            c.drawString(460, hight1, str(detalle[i].monto))
            hight1 = hight1 - delta
            monto_total = monto_total + detalle[i].monto
        
        c.setFont('Helvetica', 10)
        c.drawString(355, 415, 'TOTAL $ IVA incluido')
        c.drawString(460, 415, str("{:.2f}".format(monto_total + (monto_total * 0.21))))

        # Destino.localidad.requirente        
        c.drawString(147, 385, 'DESTINO: ')
        c.drawString(210, 385, compras_servicios.destino)
        c.line(200, 400, 570, 400)  # l.horizontal
        c.line(570, 400, 570, 380)  # l.vertical
        c.line(570, 380, 200, 380)  # l.horizontal
        c.line(200, 380, 200, 400)  # l.vertical

        c.drawString(135, 355, 'LOCALIDAD: ')
        c.drawString(210, 355, compras_servicios.localidad.ciudad)
        c.line(200, 370, 570, 370)  # l.horizontal
        c.line(570, 370, 570, 350)  # l.vertical
        c.line(570, 350, 200, 350)  # l.horizontal
        c.line(200, 350, 200, 370)  # l.vertical

        c.drawString(126, 325, 'REQUIRENTE:')
        c.drawString(210, 325, compras_servicios.user.get_full_name())
        c.line(200, 340, 570, 340)  # l.horizontal
        c.line(570, 340, 570, 320)  # l.vertical
        c.line(570, 320, 200, 320)  # l.horizontal
        c.line(200, 320, 200, 340)  # l.vertical

        # Firmas
        firm = 'Nombre y firma jefe departamento'
        width = stringWidth(firm, 'Helvetica', 10)
        c.setFont('Helvetica', 10)
        x = (PAGE_WIDTH/2)-(width/2)
        c.drawString(x, 225, firm)
        c.line(220, 240, 380, 240)
        c.drawString(240, 210, 'Legajo n° .........................')
        # c.showPage()

        c.line(30, 240, 190, 240)
        c.drawString(60, 225, 'Firma del requirente')
        c.drawString(50, 210, 'Legajo n° .........................')

        c.line(410, 240, 570, 240)
        c.drawString(440, 225, 'Gerente/Adm. Gral.')
        c.drawString(430, 210, 'Legajo n° .........................')

        # Cuadro.procedimiento
        c.drawString(35, 188, 'Procedimiento:')

        c.setFont('Helvetica', 8)
        c.drawString(
            35, 175, '1) SOLICITUD DEL BIEN O PRESTACIÓN DE SERVICIO. 2) PRESUPUESTO/S REQUERIDO/S. 3) AUTORIZACION JEFE DE DEPARTAMENTO')
        c.drawString(
            35, 165, 'Y GERENTE/ADMINISTRADOR GENERAL. 4) CONSTATACION DE LA EFECTIVA PRESTACION DE LOS SERVICIOS Y/O REMITO DE')
        c.drawString(
            35, 155, 'RECEPCIÓN DE LOS BIENES. CONFECCIÓN DE PLANILLA DE CARGO, CUANDO CORRESPONDA. 5) FACTURA DEL PROVEEDOR.')
        c.drawString(
            35, 145, '6) ORDEN DE PROVISION (CONTADURÍA) CON TODO LO ANTERIOR ANEXADO.')

        c.line(30, 200, 570, 200)  # L.hor
        c.line(570, 200, 570, 130)  # L.vert
        c.line(570, 130, 30, 130)  # L.hor
        c.line(30, 130, 30, 200)  # L.vert

        # Cuadro.ultima.firma
        c.setFont('Helvetica', 10)
        c.drawString(
            35, 118, 'RECIBI DE CONFORMIDAD LOS BIENES ADQUIRIDOS Y/O HE VERIFICADO LA PRESTACIÓN EFECTIVA DEL')
        c.drawString(35, 103, 'SERVICIO EL DÍA: ……/……/……')
        c.line(570, 130, 570, 20)  # L.vert
        c.line(570, 20, 30, 20)  # L.hor
        c.line(30, 20, 30, 130)  # L.vert

        c.line(400, 50, 560, 50)  # firma
        c.drawString(410, 40, 'Nombre y firma del Requirente/ ')
        c.drawString(415, 25, 'Jefe depto./Gte./Adm. Gral.')

        c.setFont('Helvetica', 12)

        # Funcion que agrega saltos de linea
        j = 0
        n = 87
        story = ''

        # Texto que va contenido dentro de los detalles de trabajo
        textobject = c.beginText()
        textobject.setTextOrigin(35, 208)
        textobject.setFont("Courier", 10)

        c.drawText(textobject)

        c.save()
        pdf = buffer.getvalue()
        buffer.close()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Dispotition'] = 'filename=Reporte-Anticipo.pdf'
        return response
