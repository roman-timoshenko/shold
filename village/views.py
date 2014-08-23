# Create your views here.
import json

from django.http import HttpResponse
from django.views.generic import FormView

from village.forms import InitVillagesForm, CreateVillageForm
from village.models import Village


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

    return HttpResponse(json.dumps({'a': a, 'b': b}), content_type='application/json')