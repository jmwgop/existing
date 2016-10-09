from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from django.shortcuts import render

from .models import Tract

class TractList(ListView):
    model = Tract
    paginate_by = 12
    template_name = 'tracts/tract_list.html'
    context_object_name = 'tracts'

    def get_queryset(self):
        try:
            a = self.request.GET.get('tract',)
        except KeyError:
            a = None
        if a:
            tract_list = Tract.objects.filter(
                name__icontains=a,
                owner=self.request.user.id
            )
        else:
            tract_list = Tract.objects.filter(owner=self.request.user)
        return tract_list

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TractList, self).dispatch(*args, **kwargs)


@login_required()
def tract_detail(request, uuid):

    tract = Tract.objects.get(uuid=uuid)
    variables = {
        'tract': tract,
    }

    return render(request, 'tracts/tract_detail.html', variables)
