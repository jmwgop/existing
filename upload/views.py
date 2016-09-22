# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import FormView

import shutil
import os
import magic
from glob import iglob, glob

from .doc_pull import Runsheet
from . import doc_pull
from .models import Document
from .forms import DocumentForm

def list(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            mime = magic.from_buffer(request.FILES['docfile'].read(), mime=True)
            if mime == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                newdoc.save()
                # Redirect to the document list after POST
                return HttpResponseRedirect(reverse('upload.views.process'))
            else:
                return render_to_response('upload/error.html')
    else:
        form = DocumentForm() # A empty, unbound form
    # Load documents for the list page
    documents = Document.objects.all()
    # Render list page with the documents and the form
    return render_to_response(
        'upload/list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request))

def process(self):
    path = '/home/jmwgop/midland/midland/media/documents/**/*.xlsx'
    for filename in iglob(path, recursive=True):
        runsheet = Runsheet(filename)
        runsheet.create_request()
        for x in runsheet.instrument:
            did = x["did"]
            saveas = x["saveas"]
            runsheet.grab_img(did, saveas)
            # This part needs to be fixed. currently creating the file but throwing an error
            #
            # out = "/home/jmwgop/midland/midland/media/runsheets/"+str(runsheet.runsheet_id)
            # shutil.make_archive(out, 'zip', runsheet.temp)
        runsheet.create_runsheet()
        os.remove(filename)
    shutil.rmtree("/home/jmwgop/midland/midland/media/documents")
    return render_to_response(
        'upload/processed.html')
