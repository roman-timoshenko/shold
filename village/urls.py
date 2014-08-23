from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from village.models import Village
from village.views import AddVillageView, InitVillagesView, calculate_distance


urlpatterns = patterns('',
    url(r'^$', login_required(ListView.as_view(model=Village, context_object_name='villages'))),
    url(r'^(?P<pk>\d+)/$', login_required(DetailView.as_view(model=Village, context_object_name='village'))),
    url(r'^add/$', login_required(AddVillageView.as_view())),
    url(r'^init/$', login_required(InitVillagesView.as_view())),
    url(r'^distance/(?P<a>\d+)/(?P<b>\d+)/$', calculate_distance),
)
