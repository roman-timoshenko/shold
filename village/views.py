from django.http.response import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.template.response import TemplateResponse
from village.models import Village


def list(request):
    villages = Village.objects.all()
    return TemplateResponse(request, "village/list.html", {'villages': villages})


def view(request, village_id):
    village = Village.objects.get(pk=village_id)
    return TemplateResponse(request, "village/view.html", {'village': village})


def add(request):
    if request.method == 'POST':
        village = Village(name='', x=0, y=0)
        village.save()
        return HttpResponseRedirect('/villages/view/%s/' % village.id)
    return TemplateResponse(request, 'village/add.html', {'villages' : Village.objects.all()})