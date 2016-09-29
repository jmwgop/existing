from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage

import os, magic, shutil, xlrd, datetime

from .forms import SearchForm
from search.process_search import Query



@login_required(login_url='/accounts/login/')
def initial(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            subdivision = request.POST['subdivision'].upper()
            block = request.POST['block'].zfill(5)
            query = Query(block, subdivision)
            landman_1 = request.user.id
            runsheet_id = query.create_request(landman_1)
            for y in query.instrument:
                did = y['did']
                saveas = y['saveas']
                if saveas != '--None.tif':
                    try:
                        query.grab_img(did, saveas)
                    except:
                        pass
                else:
                    pass
            query.create_runsheet()
            query.archive()
            shutil.rmtree(default_storage.path('runsheets/'+str(runsheet_id)+"/"))
    else:
        form = SearchForm()
    return render(request, 'search/search.html', {'form': form})
