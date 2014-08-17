from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views
from account.views import profile, register

urlpatterns = patterns('',
    url(r'^login/', auth_views.login),
    url(r'^register/', register),
    url(r'^profile/', profile),
    url(r'^logout/', auth_views.logout),
)
