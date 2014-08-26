import json
import datetime

from django.http import HttpResponse
from django.views.generic import FormView

from village.forms import InitVillagesForm, CreateVillageForm, format_distance, CalculateTimeForm
from django.template.response import TemplateResponse
from village.models import Village
from village.utils import get_distance


class AddVillageView(FormView):
    form_class = CreateVillageForm
    success_url = '/villages/'
    template_name = 'village/add.html'

    def form_valid(self, form):
        form.save()
        return super(AddVillageView, self).form_valid(form)


class InitVillagesView(FormView):
    form_class = InitVillagesForm
    success_url = '/villages/'
    template_name = 'village/init.html'

    def form_valid(self, form):
        form.save()
        return super(InitVillagesView, self).form_valid(form)

def calculate_time(request):
    distance = None
    distance_x2 = None
    distance_x3 = None
    distance_x4 = None
    distance_x5 = None
    distance_x6 = None
    if request.method == 'POST':
        form = CalculateTimeForm(request.POST)
#        distance=(request.POST['distance'])
        if form.is_valid():
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
#            form.save()
#            village = form.cleaned_data['village']
#            distance = distance.cleaned_data['distance']
            distance = get_distance((a.x, a.y), (b.x, b.y))
            distance_x2 = distance//2
            distance_x3 = distance//3
            distance_x4 = distance//4
            distance_x5 = distance//5
            distance_x6 = distance//6
            distance = datetime.datetime.utcfromtimestamp(distance).strftime('%H:%M:%S')
            distance_x2 = ',  X2 = '+str(datetime.datetime.utcfromtimestamp(distance_x2).strftime('%H:%M:%S'))
            distance_x3 = ',  X3 = '+str(datetime.datetime.utcfromtimestamp(distance_x3).strftime('%H:%M:%S'))
            distance_x4 = ',  X4 = '+str(datetime.datetime.utcfromtimestamp(distance_x4).strftime('%H:%M:%S'))
            distance_x5 = ',  X5 = '+str(datetime.datetime.utcfromtimestamp(distance_x5).strftime('%H:%M:%S'))
            distance_x6 = ',  X6 = '+str(datetime.datetime.utcfromtimestamp(distance_x6).strftime('%H:%M:%S'))
            return TemplateResponse(request, 'village/calculate_time.html', {'form':form,
                                        'distance':distance, 'distance_x2':distance_x2, 'distance_x3':distance_x3,
                                        'distance_x4':distance_x4, 'distance_x5':distance_x5, 'distance_x6':distance_x6})
    else:
        form = CalculateTimeForm()

    return TemplateResponse(request, 'village/calculate_time.html', {'form': form, 'distance':distance})

def calculated(request, distance):
#    village = Village.objects.get(pk=village_id)
#    distance = (request.POST['distance'])
    return TemplateResponse(request, "village/calculated.html", {'distance': distance})

def calculate_distance(request, a, b):
    a = Village.objects.get(pk=a)
    b = Village.objects.get(pk=b)

    data = {
        'a': {
            'id': a.id,
            'name': a.name
        },
        'b': {
            'id': b.id,
            'name': b.name
        },
        'distance': format_distance(get_distance((a.x, a.y), (b.x, b.y)))
    }
    response = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    return HttpResponse(response, content_type='application/json')
