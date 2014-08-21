from django.conf.urls import patterns, url
from village.views import list, add, view, init


urlpatterns = patterns('',
    url(r'^list/', list),
    url(r'^add/', add),
    url(r'^init/', init),
    url(r'^view/(?P<village_id>\d+)', view),
)
