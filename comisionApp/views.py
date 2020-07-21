from datetime import date
from django.db import transaction
from io import BytesIO
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, DeleteView, ListView, TemplateView
from django.http import HttpResponse, JsonResponse, request
from django.core.exceptions import ObjectDoesNotExist
from .forms import TransporteForm
from .models import *
from usuarios.models import User
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import cm, inch
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.rl_config import defaultPageSize
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer
from comisionManager.utils import render_pdf
from django.core import serializers


# Create your views here.
class ReportePdfSolicitud(View):
    """Regresa Pdf"""

    def post(self, request, *args, **kwargs):
        pk = request.POST.getlist('afiliado[]')
        num_afiliados = request.POST.getlist('num_afiliado[]')
        motivo = request.POST['motivo']
        fech_inicio = request.POST['fech_inicio']
        duracion_prevista = request.POST['duracion_prevista']
        ciudad = request.POST['ciudad']
        transporte = request.POST['transporte']
        patente = request.POST['patente']
        gastos_previstos = request.POST['gastos_previstos']

        # este for recupera los usuarios cuyos id estan contenidos en la lista pk
        nombre = []
        for i in range(len(pk)):
            pk1 = str(pk[i])
            nombre.append(User.objects.get(pk=pk1))

        num_legajo_transporte = Transporte.objects.get(
            id_transporte=transporte)

        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)

        PAGE_WIDTH = defaultPageSize[0]
        PAGE_HEIGHT = defaultPageSize[1]

        text = 'Solicitud de comisión'

        width = stringWidth(text, 'Helvetica', 16)
        x = (PAGE_WIDTH/2)-(width/2)

        # Header
        c.setLineWidth(.3)
        c.setFont('Helvetica', 18)
        c.drawString(x, 800, text)
        c.setFont('Helvetica', 12)

        fecha = date.today().strftime("%d/%m/%Y")

        c.drawString(400, 770, 'Fecha de pedido: ' + str(fecha))
        c.drawString(30, 745, 'Apellido y Nombre'+'       ' +
                     request.user.last_name + '  '+request.user.first_name)
        c.drawString(360, 745, 'N° Afiliado a SEMPRE' +
                     '         ' + str(request.user.num_afiliado))

        alto = 720
        for i in range(len(pk)):
            c.drawString(30, alto, 'Apellido y Nombre'+'       ' +
                         nombre[i].last_name + '  '+nombre[i].first_name)
            c.drawString(360, alto, 'N° Afiliado a SEMPRE' +
                         '         ' + num_afiliados[i])
            alto = alto - 25

        c.drawString(30, 570, 'Motivo de la comisión: ')
        # Funcion que agrega saltos de linea a 'motivo' para que se pinte en el pdf
        j = 0
        n = 87
        story = ''
        for i in range(len(motivo)):
            if i == n:
                story = story + motivo[j:n] + '\n'
                j = n
                n = n + 86
        story = story + motivo[j:len(motivo)]

        # Texto que va contenido dentro de los detalles de trabajo
        textobject = c.beginText()
        textobject.setTextOrigin(35, 555)
        textobject.setFont("Courier", 10)
        textobject.textLines(story)
        c.drawText(textobject)

        c.setFont('Helvetica', 12)
        c.drawString(30, 410, 'Fecha de iniciación: '+fech_inicio)
        c.drawString(320, 410, 'Duracón prevista: '+duracion_prevista)
        c.drawString(
            30, 380, 'Lugar de residencia durante la comisión: '+ciudad)
        c.drawString(30, 350, 'Medio de transporte')
        c.drawString(200, 350, 'Unidad de legajo: ' +
                     num_legajo_transporte.num_legajo)
        c.drawString(400, 350, 'Patente: '+patente)
        c.drawString(30, 320, 'Gastos a solicitar: $'+gastos_previstos)
        c.drawString(30, 290, 'Comisión ordenada por: ' +
                     request.user.last_name+'  '+request.user.first_name)

        c.drawString(500, 20, 'Firma')
        c.line(465, 32, 570, 32)

        c.save()
        pdf = buffer.getvalue()
        buffer.close()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'filename=Solicitud.pdf'
        return response


class ReportePdfAnticipo(View):

    def get(self, request, *args, **kwargs):
        anticipo = Anticipo.objects.get(pk=kwargs['pk'])
        itineraio = Itineraio.objects.filter(anticipo_id=kwargs['pk'])
        det_trabajo = DetalleTrabajo.objects.get(anticipo_id=kwargs['pk'])
        integrantes = Integrantes_x_Anticipo.objects.filter(
            anticipo_id=kwargs['pk'])

        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)

        PAGE_WIDTH = defaultPageSize[0]
        PAGE_HEIGHT = defaultPageSize[1]

        text = 'Rendicion de comisión'

        width = stringWidth(text, 'Helvetica', 16)
        x = (PAGE_WIDTH/2)-(width/2)

        # Header
        c.setLineWidth(.3)
        c.setFont('Helvetica', 18)
        c.drawString(x, 800, text)

        alto = 770

        c.setFont('Helvetica', 12)
        for i in range(len(integrantes)):
            c.drawString(30, alto, 'Apellido y Nombre'+'       ' +
                         integrantes[i].user.last_name + '  '+integrantes[i].user.first_name)
            c.drawString(360, alto, 'N° Afiliado a SEMPRE' +
                         '         ' + integrantes[i].user.num_afiliado)
            alto = alto - 25

        c.drawString(30, 620, 'Fecha de inicio: ' + str(anticipo.fech_inicio))
        c.drawString(320, 620, 'Fecha de finalización: ' +
                     str(anticipo.fech_fin))
        c.drawString(
            30, 595, 'Lugar de residencia durante la comisión: ' + anticipo.ciudad.ciudad)
        c.drawString(30, 570, 'Medio de transporte')
        c.drawString(200, 570, 'Unidad de legajo: ' +
                     anticipo.transporte.num_legajo)
        c.drawString(400, 570, 'Patente: ' + anticipo.transporte.patente)
        c.drawString(30, 545, 'Gastos: ' + str(anticipo.gastos))

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
        c.drawString(30, 245, 'Informe de la comision: ')

        c.setFont('Helvetica', 12)
        c.drawString(32, 220, 'km Salida: '+str(det_trabajo.km_salida))
        c.drawString(180, 220, 'km Llegada: '+str(det_trabajo.km_llegada))
        c.drawString(350, 220, 'Total km recorrido: ' +
                     str(det_trabajo.km_llegada-det_trabajo.km_salida))

        # Lineas Verticales
        c.line(30, 237, 30, 50)
        c.line(565, 50, 565, 237)

        # Lineas Horizontales
        c.line(30, 237, 565, 237)
        c.line(30, 210, 565, 210)
        c.line(30, 50, 565, 50)

        c.setFont('Helvetica', 12)
        c.drawString(35, 195, 'Detalle de los trabajos realizados: ')

        # Funcion que agrega saltos de linea
        j = 0
        n = 87
        story = ''
        for i in range(len(det_trabajo.detalle_trabajo)):
            if i == n:
                story = story + det_trabajo.detalle_trabajo[j:n] + '\n'
                j = n
                n = n + 87
        story = story + \
            det_trabajo.detalle_trabajo[j:len(det_trabajo.detalle_trabajo)]

        # Texto que va contenido dentro de los detalles de trabajo
        textobject = c.beginText()
        textobject.setTextOrigin(35, 180)
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
        response['Content-Dispotition'] = 'filename=Reporte-Anticipo.pdf'
        return response

    def post(self, request, *args, **kwargs):
        pk = request.POST.getlist('afiliado[]')
        num_afiliados = request.POST.getlist('num_afiliado[]')
        # ciudad
        pk_ciudad = request.POST['ciudad']
        # comision
        fech_inicio = request.POST['fecha_inicio']
        fech_fin = request.POST['fecha_fin']
        transporte = request.POST['transporte']
        patente = request.POST.get('patente')
        gastos = request.POST.get('gastos')

        # Itinerario
        nombres = request.POST.getlist('name[]')
        dias = request.POST.getlist('dia[]')
        meses = request.POST.getlist('mes[]')
        salidas = request.POST.getlist('salida[]')
        llegadas = request.POST.getlist('llegada[]')
        horas_salida = request.POST.getlist('hora_salida[]')
        horas_llegada = request.POST.getlist('hora_llegada[]')

        # Detalle de trabajo
        km_salida = request.POST['km_salida']
        km_llegada = request.POST['km_llegada']
        km_total = request.POST['km_total']
        detalle_trabajo = request.POST['detalle_trabajo']

        # este for recupera los usuarios cuyos id estan contenidos en la lista pk
        nombre = []
        for i in range(len(pk)):
            pk1 = str(pk[i])
            nombre.append(User.objects.get(pk=pk1))

        num_legajo_transporte = Transporte.objects.get(
            id_transporte=transporte)
        ciudad = Ciudad.objects.get(id_ciudad=pk_ciudad)

        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)

        PAGE_WIDTH = defaultPageSize[0]
        PAGE_HEIGHT = defaultPageSize[1]

        text = 'Rendicion de comisión N° ___________'

        width = stringWidth(text, 'Helvetica', 16)
        x = (PAGE_WIDTH/2)-(width/2)

        # Header
        c.setLineWidth(.3)
        c.setFont('Helvetica', 18)
        c.drawString(x, 800, text)

        c.setFont('Helvetica', 12)
        c.drawString(30, 770, 'Apellido y Nombre'+'       ' +
                     request.user.last_name + '  '+request.user.first_name)
        c.drawString(360, 770, 'N° Afiliado a SEMPRE' +
                     '         ' + str(request.user.num_afiliado))

        alto = 745

        for i in range(len(pk)):
            c.drawString(30, alto, 'Apellido y Nombre'+'       ' +
                         nombre[i].last_name + '  '+nombre[i].first_name)
            c.drawString(360, alto, 'N° Afiliado a SEMPRE' +
                         '         ' + num_afiliados[i])
            alto = alto - 25

        c.drawString(30, 620, 'Fecha de inicio: ' + fech_inicio)
        c.drawString(320, 620, 'Fecha de finalización: ' + fech_fin)
        c.drawString(
            30, 595, 'Lugar de residencia durante la comisión: ' + ciudad.ciudad)
        c.drawString(30, 570, 'Medio de transporte')
        c.drawString(200, 570, 'Unidad de legajo: ' +
                     num_legajo_transporte.num_legajo)
        c.drawString(400, 570, 'Patente: ' + patente)
        c.drawString(30, 545, 'Gastos: ' + gastos)

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
        for i in range(len(nombres)):
            comisiones.append({'name': nombres[i], 'b1': dias[i], 'b2': meses[i], 'b3': salidas[i],
                               'b4': horas_salida[i], 'b5': llegadas[i], 'b6': horas_llegada[i], })

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
        c.drawString(30, 245, 'Informe de la comision: ')

        c.setFont('Helvetica', 12)
        c.drawString(32, 220, 'km Salida: '+km_salida)
        c.drawString(180, 220, 'km Llegada: '+km_llegada)
        c.drawString(350, 220, 'Total km recorrido: '+km_total)

        # Lineas Verticales
        c.line(30, 237, 30, 50)
        c.line(565, 50, 565, 237)

        # Lineas Horizontales
        c.line(30, 237, 565, 237)
        c.line(30, 210, 565, 210)
        c.line(30, 50, 565, 50)

        c.setFont('Helvetica', 12)
        c.drawString(35, 195, 'Detalle de los trabajos realizados: ')

        # Funcion que agrega saltos de linea
        j = 0
        n = 87
        story = ''
        for i in range(len(detalle_trabajo)):
            if i == n:
                story = story + detalle_trabajo[j:n] + '\n'
                j = n
                n = n + 87
        story = story + detalle_trabajo[j:len(detalle_trabajo)]

        # Texto que va contenido dentro de los detalles de trabajo
        textobject = c.beginText()
        textobject.setTextOrigin(35, 180)
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
        response['Content-Dispotition'] = 'filename=Reporte-Anticipo.pdf'
        return response


@login_required
@transaction.atomic
def confeccionSolicitudComision(request):
    users = User.objects.all().exclude(pk=request.user.pk)
    ciudades = Ciudad.objects.all()
    transportes = Transporte.objects.all()
    return render(request, 'confeccion_sol_comision.html', {
        'users': users,
        'ciudades': ciudades,
        'transportes': transportes,
    })


@login_required
@transaction.atomic
def confeccionAnticipo(request):
    users = User.objects.all().exclude(pk=request.user.pk)
    ciudades = Ciudad.objects.all()
    transportes = Transporte.objects.all()
    return render(request, 'confeccion_comision.html', {
        'users': users,
        'ciudades': ciudades,
        'transportes': transportes,
    })


class HistoricoAnticipos(ListView):
    model = Anticipo
    context_object_name = 'anticipos'
    template_name = 'public/historico.html'

    def get_queryset(self):
        return Anticipo.objects.filter(integrantes_x_anticipo__user=self.request.user.id)


class EliminarAnticipo(DeleteView):
    model = Anticipo
    context_object_name = 'anticipo'
    template_name = 'eliminar_anticipo.html'
    success_url = reverse_lazy('comisiones:historico_anticipo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'Anticipo'
        context['list_url'] = reverse_lazy('comisiones:historico_anticipo')
        return context


@login_required
def archivar(request):
    if request.method == 'POST':
        # usuarios
        pk_users = request.POST.getlist('afiliado[]')
        num_afiliados = request.POST.getlist('num_afiliado[]')
        # ciudad
        pk_ciudad = request.POST['ciudad']
        # comision
        fech_inicio = request.POST['fecha_inicio']
        fech_fin = request.POST['fecha_fin']
        pk_transporte = request.POST['transporte']
        patente = request.POST.get('patente')
        gastos = request.POST.get('gastos')
        # Itinerario
        nombres = request.POST.getlist('name[]')
        dias = request.POST.getlist('dia[]')
        meses = request.POST.getlist('mes[]')
        salidas = request.POST.getlist('salida[]')
        llegadas = request.POST.getlist('llegada[]')
        horas_salida = request.POST.getlist('hora_salida[]')
        horas_llegada = request.POST.getlist('hora_llegada[]')

        # Cetalle de trabajo
        km_salida = request.POST['km_salida']
        km_llegada = request.POST['km_llegada']
        detalle_trabajo = request.POST['detalle_trabajo']

        # Crear anticpo en la BD
        nuevo_anticipo = Anticipo(ciudad_id=pk_ciudad,
                                  transporte_id=pk_transporte, fech_inicio=fech_inicio, fech_fin=fech_fin, gastos=gastos)
        nuevo_anticipo.save()

        for i in range(len(nombres)):
            Itineraio.objects.create(
                anticipo=nuevo_anticipo, nombre_afiliado=nombres[i], dia=dias[i], mes=meses[i],
                hora_salida=horas_salida[i], hora_llegada=horas_llegada[i], salida=salidas[i], llegada=llegadas[i])

        DetalleTrabajo.objects.create(
            anticipo=nuevo_anticipo, km_salida=km_salida, km_llegada=km_llegada, detalle_trabajo=detalle_trabajo)
        Integrantes_x_Anticipo.objects.create(
            anticipo=nuevo_anticipo, user=request.user)
        for i in range(len(pk_users)):
            Integrantes_x_Anticipo.objects.create(
                anticipo=nuevo_anticipo, user_id=pk_users[i])
        return redirect('comisiones:historico_anticipo')
    return render(request, 'confeccion_comision.html')


@login_required
def get_patente(request):
    pk_transporte = request.GET.get('transporte', None)
    data = list(Transporte.objects.filter(pk=pk_transporte).values('patente'))
    return JsonResponse({'data': data})


@login_required
def get_num_afiliado(request):
    num_afiliado = request.GET.getlist('afiliado[]')
    pk = str(num_afiliado[0])
    data = list(User.objects.filter(pk=pk).values('num_afiliado'))
    return JsonResponse({'data': data})


def listarTransportes(request):
    transportes = Transporte.objects.all()
    return render(request, 'transportes.html', {'transportes': transportes})


def altaTrasnporte(request):
    if request.method == 'POST':
        transporte_form = TransporteForm(request.POST)
        if transporte_form.is_valid():
            transporte_form.save()
            return redirect('comision:transportes')
    else:
        transporte_form = TransporteForm()
    return render(request, 'alta_transporte.html', {'transporte_form': transporte_form})


def editarTransporte(request, id):
    transporte_form = None
    error = None
    try:
        transporte = Transporte.objects.get(id_transporte=id)
        if request.method == 'GET':
            transporte_form = TransporteForm(instance=transporte)
        else:
            transporte_form = TransporteForm(request.POST, instance=transporte)
            if transporte_form.is_valid():
                transporte_form.save()
            return redirect('index')
    except ObjectDoesNotExist as e:
        error = e
    return render(request, 'alta_transporte.html', {'transporte_form': transporte_form, 'error': error})


def eliminarTransporte(request, id):
    transporte = Transporte.objects.get(id_transporte=id)
    if request.method == 'POST':
        transporte.delete()
        return redirect('comision:transportes')
    return render(request, 'eliminar_transporte.html', {'transporte': transporte})
