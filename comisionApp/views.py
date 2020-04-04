from django.db import transaction
from io import BytesIO
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse,  JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .forms import TransporteForm
from .models import *
from usuarios.models import User
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.rl_config import defaultPageSize
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

        afiliados = [{'nombre': request.user.get_full_name,
                      'num_afiliado': request.user.num_afiliado}]

        #este for recupera los usuarios cuyos id estan contenidos en la lista pk
        nombre = []
        for i in range(len(pk)):
            pk1 = str(pk[i])
            nombre.append(User.objects.get(pk=pk1))

        for i in range(len(pk)):
            pk1 = str(pk[i])
            afiliados.append({
                'nombre': nombre[i].last_name+' '+nombre[i].first_name,
                'num_afiliado': num_afiliados[i]
            })

        pdf = render_pdf('reporte_pdf.html',
                         {
                             'afiliados': afiliados,
                             'motivo': motivo,
                             'fech_inicio': fech_inicio,
                             'duracion_prevista': duracion_prevista,
                             'ciudad': ciudad,
                             'transporte': transporte,
                             'patente': patente,
                             'gastos_previstos': gastos_previstos,
                         }
                         )
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'filename=Solicitud.pdf'
        return response


class ReportePdfAnticipo(View):

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='reporte_pdf.html')
        response['Content-Disposition'] = 'attachment; filename=Anticipo.pdf'
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)

        PAGE_WIDTH = defaultPageSize[0]
        PAGE_HEIGHT = defaultPageSize[1]

        text = 'Rendicion de comisión N° 547982'

        width = stringWidth(text, 'Helvetica', 16)
        x = (PAGE_WIDTH/2)-(width/2)

        # Header
        c.setLineWidth(.3)
        c.setFont('Helvetica', 16)
        c.drawString(x, 800, 'Rendicion de comisión N° 547982')

        c.setFont('Helvetica', 12)  # machea tipo de fuente y tamaño
        c.drawString(60, 770, 'Apellido y Nombre')
        c.drawString(190, 770, 'Vargas Germán')
        c.drawString(320, 770, 'N° Afiliado a SEMPRE')
        c.drawString(490, 770, '70305/1')

        c.drawString(60, 745, 'Apellido y Nombre')
        c.drawString(190, 745, 'Vargas Germán')
        c.drawString(320, 745, 'N° Afiliado a SEMPRE')
        c.drawString(490, 745, '70305/1')

        c.drawString(60, 720, 'Apellido y Nombre')
        c.drawString(190, 720, 'Vargas Germán')
        c.drawString(320, 720, 'N° Afiliado a SEMPRE')
        c.drawString(490, 720, '70305/1')

        c.drawString(60, 695, 'Apellido y Nombre')
        c.drawString(190, 695, 'Vargas Germán')
        c.drawString(320, 695, 'N° Afiliado a SEMPRE')
        c.drawString(490, 695, '70305/1')

        c.save()
        pdf = buffer.getvalue()
        buffer.close()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Dispotition'] = 'filename=Reporte-Anticipo.pdf'
        return response


@login_required
@transaction.atomic
def confeccionSolicitudComision(request):
    users = User.objects.all()
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
    users = User.objects.all()
    ciudades = Ciudad.objects.all()
    transportes = Transporte.objects.all()
    return render(request, 'confeccion_comision.html', {
        'users': users,
        'ciudades': ciudades,
        'transportes': transportes,
    })


@login_required
def historicoAnticipos(request):
    anticipos = Anticipo.objects.filter(
        integrantes_x_anticipo__user=request.user.id)
    return render(request, 'public/historico.html', {'anticipos': anticipos})


def archivar(request):
    print(request.POST)
    return render(request, 'index.html')


@login_required
def get_patente(request):
    transporte = request.GET.get('transporte', None)
    data = list(Transporte.objects.filter(
        num_legajo=transporte).values('patente'))
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
