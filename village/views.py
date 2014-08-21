from django.http.response import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.template.response import TemplateResponse
from village.forms import InitVillagesForm
from village.models import Village, calculate_villages


def list(request):
    villages = Village.objects.all()
    return TemplateResponse(request, "village/list.html", {'villages': villages})


def view(request, village_id):
    village = Village.objects.get(pk=village_id)
    return TemplateResponse(request, "village/view.html", {'village': village})


def add(request):
    if request.method == 'POST':
        #TODO: check and save village
        village = Village(id=1)
        return HttpResponseRedirect('/villages/view/%s/' % village.id)
    return TemplateResponse(request, 'village/add.html', {'villages' : Village.objects.all()})


def init(request):
    if request.method == 'POST':
        form = InitVillagesForm(request.POST)
        if form.is_valid():
            a, b, c = calculate_villages(form.cleaned_data['a'], form.cleaned_data['b'], form.cleaned_data['c'],
                                         form.get_ab(), form.get_bc(), form.get_ca())
            if Village.objects.count() > 0:
                Village.objects.all().delete()
            a.save()
            b.save()
            c.save()
            return HttpResponseRedirect('/villages/list/')
    else:
        form = InitVillagesForm()
    return TemplateResponse(request, 'village/init.html', {'form': form})