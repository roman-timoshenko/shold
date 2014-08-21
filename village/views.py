from django.http.response import HttpResponseRedirect

# Create your views here.
from django.template.response import TemplateResponse
from village.forms import InitVillagesForm, CreateVillageForm
from village.models import Village, calculate_villages
from village.utils import get_fourth_point


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
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            c = form.cleaned_data['c']
            #TODO: check and save village
            try:
                point = get_fourth_point((a.x, a.y), (b.x, b.y), (c.x, c.y),
                                 form.get_toa(), form.get_tob(), form.get_toc())
                village = Village(name=form.cleaned_data['name'], x=point[0], y=point[1])
                print(village)
                return HttpResponseRedirect('/villages/view/%s/' % village.id)
            except ValueError as e:
                form.errors['__all__'] = form.error_class([e.message])
    else:
        form = CreateVillageForm()
    return TemplateResponse(request, 'village/add.html', {'form': form})


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