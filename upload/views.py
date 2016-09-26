# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required

from sendfile import sendfile
import os, magic, shutil
from glob import iglob, glob

from .doc_pull import Runsheet
from .models import Document
from .forms import DocumentForm

@login_required(login_url='/accounts/login/')
def list(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            mime = magic.from_buffer(request.FILES['docfile'].read(), mime=True)
            if mime == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                newdoc.save()
            else:
                return render(request, 'upload/error.html')
            path = request.FILES['docfile']
            print(path)
    else:
        form = DocumentForm() # A empty, unbound form
    # Render list page with the form
    return render(request, 'upload/list.html', {'form': form})


def process():
    pass
    # path = '/home/jmwgop/midland/midland/media/documents/**/*.xlsx'
    # for filename in iglob(path, recursive=True):
    #     runsheet = Runsheet(filename)
    #     runsheet.create_request()
    #     for x in runsheet.instrument:
    #         did = x["did"]
    #         saveas = x["saveas"]
    #         runsheet.grab_img(did, saveas)
    #     runsheet.create_runsheet()
    #     out = "/home/jmwgop/midland/midland/media/runsheets/"+str(runsheet.runsheet_id)
    #     filename_1 = shutil.make_archive(out, 'zip', runsheet.temp)
    #     os.remove(filename)
    #     shutil.rmtree(out)
    #     return sendfile(request, filename_1)
    # return render_to_response(
    #     'upload/processed.html')
