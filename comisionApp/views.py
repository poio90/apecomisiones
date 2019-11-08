from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .forms import TransporteForm
from .models import Ciudad,Transporte


# Create your views here.
def home(request):
    return render(request, 'index.html')


def listarCiudades(request):
    ciudades = Ciudad.objects.all()
    return render(request, 'ciudades.html', {'ciudades': ciudades})


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

