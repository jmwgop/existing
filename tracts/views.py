from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from .models import Tract
from .forms import TractForm

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
                owner=self.request.user
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

@login_required()
def tract_cru(request):
    owner = request.user
    if request.POST:
        form = TractForm(request.POST)
        if form.is_valid():
            tract = form.save(commit=False)
            tract.owner = owner
            print(tract.short_legal, tract.full_legal, tract.situs_address, tract.city, tract.state, tract.zip_code, tract.owner, tract.created_on)
            tract.save()
            redirect_url = reverse('tract_detail', kwargs={'uuid': tract.uuid})
            return HttpResponseRedirect(redirect_url)
    else:
        form = TractForm()

    variables = {
        'form': form,
    }

    template = 'tracts/tract_cru.html'

    return render(request, template, variables)
