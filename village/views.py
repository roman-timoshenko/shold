# Create your views here.
import json

from django.http import HttpResponse
from django.views.generic import FormView

from village.forms import InitVillagesForm, CreateVillageForm, format_distance
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
