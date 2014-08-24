from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from account.views import profile, register

urlpatterns = patterns('',
    url(r'^login/', auth_views.login, name='login'),
    url(r'^register/', register, name='register'),
    url(r'^profile/', profile, name='profile'),
    url(r'^password_change/done/', RedirectView.as_view(
        url='/profile/'), name='password_change_done'),
    url(r'^logout/', auth_views.logout, name='logout'),
    url(r'^password_change/', auth_views.password_change, name='password_change'),
)
