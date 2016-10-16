# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

import os, magic, shutil, xlrd, psycopg2, datetime
import io
from glob import iglob, glob

from .doc_pull import Runsheet
from .models import Document
from .forms import DocumentForm

@login_required(login_url='/accounts/login/')
def list(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            mime = magic.from_buffer(request.FILES['docfile'].read(), mime=True)
            if mime == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                basename = "process"
                suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")\
                        +".xlsx"
                filename = "_".join([basename, suffix])
                file_obj = request.FILES['docfile']
                with open(default_storage.path('tmp/'+filename), 'wb+') as destination:
                    for chunk in file_obj.chunks():
                        destination.write(chunk)
                runsheet = Runsheet(default_storage.path('tmp/'+filename))
                landman_1 = request.user.id
                runsheet_id = runsheet.create_request(landman_1)
                for x in runsheet.instrument:
                    did = x['did']
                    saveas_1 = x['saveas']
                    print(did, saveas_1)
                    if did != '':
                        try:
                            runsheet.grab_img(did, saveas_1)
                        except:
                            pass
                    else:
                        pass
                runsheet.create_runsheet()
                runsheet.archive()
                shutil.rmtree(default_storage.path('runsheets/'+str(runsheet_id)+"/"))
                os.remove(default_storage.path('tmp/'+filename))
            else:
                return render(request, 'upload/error.html')
    else:
        form = DocumentForm() # A empty, unbound form
    # Render list page with the form
    return render(request, 'upload/list.html', {'form': form})

def process():
    pass
