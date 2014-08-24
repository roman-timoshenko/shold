from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.views.generic import RedirectView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^password_change/done/', RedirectView.as_view(
        url='/profile/'), name='password_change_done'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/', include('account.urls', namespace='account', app_name='account')),
    url(r'^villages/', include('village.urls', namespace='village', app_name='village')),
)
