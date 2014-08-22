from django.http.response import HttpResponseRedirect

# Create your views here.
from django.template.response import TemplateResponse
from village.forms import InitVillagesForm, CreateVillageForm
from village.models import Village


def list(request):
    villages = Village.objects.all()
    return TemplateResponse(request, "village/list.html", {'villages': villages})


def view(request, village_id):
    village = Village.objects.get(pk=village_id)
    return TemplateResponse(request, "village/view.html", {'village': village})


def add(request):
    if request.method == 'POST':
        form = CreateVillageForm(request.POST)
        if form.is_valid():
            form.save()
            village = form.cleaned_data['village']
            return HttpResponseRedirect('/villages/view/%s/' % village.id)
    else:
        form = CreateVillageForm()
    return TemplateResponse(request, 'village/add.html', {'form': form})


def init(request):
    if request.method == 'POST':
        form = InitVillagesForm(request.POST)
        if form.is_valid():
            if Village.objects.count() > 0:
                Village.objects.all().delete()
            form.save()
            return HttpResponseRedirect('/villages/list/')
    else:
        form = InitVillagesForm()
    return TemplateResponse(request, 'village/init.html', {'form': form})