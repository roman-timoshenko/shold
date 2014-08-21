from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.template import context
from django.template.response import TemplateResponse


# @login_required
def profile(request):
    return TemplateResponse(request, "registration/profile.html", {"user": request.user})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/accounts/profile/")
    else:
        form = UserCreationForm()
    return TemplateResponse(request, "registration/register.html", {'form': form})