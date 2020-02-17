from io import BytesIO
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .forms import TransporteForm
from .models import Ciudad,Transporte, Comision
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.rl_config import defaultPageSize
from comisionManager.utils import render_pdf


# Create your views here.
class ReportePdf(View):
    """Regresa Pdf"""
    def get(self, request,*args,**kwargs):
        datos = {
            'nombre': 'Germán',
            'apellido': 'Vargas',
            'edad': 29
        }
        pdf = render_pdf('reporte_pdf.html', {'datos':datos})
        
        return HttpResponse(pdf, content_type='reporte_pdf.html')

class ReportePdf2(View):
    """response = HttpResponse(content_type='reporte_pdf.html')
    response['Content-Disposition'] = 'attachment; filename=Anticipo.pdf'
    def get(self, request,*args,**kwargs):
        pdf = render_pdf2(request)
        response.write(pdf) 
        return response"""
    def get(self, request,*args,**kwargs):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)

        PAGE_WIDTH  = defaultPageSize[0]
        PAGE_HEIGHT = defaultPageSize[1]

        text = 'Rendicion de comisión N° 547982'

        width = stringWidth(text, 'Helvetica',16)
        x = (PAGE_WIDTH/2)-(width/2)

        # Header
        c.setLineWidth(.3)
        c.setFont('Helvetica',16)
        c.drawString(x,800,'Rendicion de comisión N° 547982')

        c.setFont('Helvetica',12)
        c.drawString(60,770,'Apellido y Nombre')
        c.drawString(190,770,'Vargas Germán')
        c.drawString(320,770,'N° Afiliado a SEMPRE')
        c.drawString(490,770,'70305/1')

        c.drawString(60,745,'Apellido y Nombre')
        c.drawString(190,745,'Vargas Germán')
        c.drawString(320,745,'N° Afiliado a SEMPRE')
        c.drawString(490,745,'70305/1')

        c.drawString(60,720,'Apellido y Nombre')
        c.drawString(190,720,'Vargas Germán')
        c.drawString(320,720,'N° Afiliado a SEMPRE')
        c.drawString(490,720,'70305/1')

        c.drawString(60,695,'Apellido y Nombre')
        c.drawString(190,695,'Vargas Germán')
        c.drawString(320,695,'N° Afiliado a SEMPRE')
        c.drawString(490,695,'70305/1')
    
        c.save()
        pdf = buffer.getvalue()
        buffer.close()
        return HttpResponse(pdf,content_type='reporte_pdf.html')


def listarComisiones(request):
    comisiones = Comision.objects.all()
    return render(request,'comisiones.html',{'comisiones':comisiones})

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
    transporte_form= None
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
    return render(request,'alta_transporte.html', {'transporte_form': transporte_form, 'error':error})

def eliminarTransporte(request,id):
    transporte = Transporte.objects.get(id_transporte=id)
    if request.method == 'POST':
        transporte.delete()
        return redirect('comision:transportes')
    return render(request,'eliminar_transporte.html',{'transporte':transporte})