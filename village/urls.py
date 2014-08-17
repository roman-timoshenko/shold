from django.conf.urls import patterns, url
from village.views import list, add, view


urlpatterns = patterns('',
    url(r'^list/', list),
    url(r'^add/', add),
    url(r'^view/(?P<id>\d+)', view),
)
