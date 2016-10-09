from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Tracts

class TractList(ListView):
    model = Tracts
    template_name = 'tracts/tract_list.html'
    context_object_name = 'tracts'

    def get_queryset(self):
        tract_list = Tracts.objects.filter(owner=self.request.user)
        return tract_list

    @login_required(login_url='/accounts/login/')
    def dispatch(self, *args, **kwargs):
        return super(TractList, self).dispatch(*args, **kwargs)
