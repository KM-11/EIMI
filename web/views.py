from django.shortcuts import render
from .models import Muestra, Familia
from django.db.models import Count
from django.http import HttpResponse

# Create your views here.


def index(request):
    cuenta_familia = Muestra.objects.all().values('familia').annotate(total=Count('familia')).order_by('total')

    latest_muestra_list = Muestra.objects.order_by('-date')[:5]
    context = {'latest_muestra_list': latest_muestra_list,
               'cuenta_familia': cuenta_familia}
    return render(request, 'web/tables.html',context)


def samples_detail(request):
    cuenta_familia = Muestra.objects.all().values('familia').annotate(total=Count('familia')).order_by('total')

    latest_muestra_list =Muestra.objects.order_by('-date')[:5]
    context = {'latest_muestra_list': latest_muestra_list,
               'cuenta_familia': cuenta_familia}
    return render(request, 'web/global_samples.html', context)


def sample_detail(request, muestra_hash):
    muestra=Muestra.objects.get(hash=muestra_hash)
    context = {'muestra': muestra}
    return render(request, 'web/sample_detail.html', context)

def family_detail(request, familia_id):
    #print(str(muestra_familia_id))
    #return HttpResponse(str(muestra_familia_id))
    #family= Muestra.familyid.all()
    family = Familia.objects.get(id=familia_id)
    muestras = Muestra.objects.filter(familia_id=familia_id)

    context = {'family': family,
               'muestras': muestras}
    return render(request, 'web/family_detail.html')