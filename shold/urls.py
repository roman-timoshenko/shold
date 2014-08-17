from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'shold.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^accounts/', include('account.urls')),
    url(r'^villages/', include('village.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
