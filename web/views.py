from django.shortcuts import render
from .models import Muestra
from django.db.models import Count
# Create your views here.


def index(request):
    return render(request, 'tables.html')


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