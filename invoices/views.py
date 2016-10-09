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

from .process_invoice import Invoice
# from .models import Document
# from .forms import DocumentForm
from .forms import FileFieldForm

class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'invoices/process.html'  # Replace with your template.
    success_url = '/invoices/'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                pass
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


# def invoice(request):
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             file_obj = request.FILES.getlist['docfile']
#             print(file_obj)
#             # basename = "invoice"
#             # suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")\
#             #         +".xlsx"
#             # filename = "_".join([basename, suffix])
#             # with open(default_storage.path('invoices/'+filename), 'wb+') as destination:
#             #     for chunk in file_obj.chunks():
#             #         destination.write(chunk)
#             # invoice_data = Invoice(default_storage.path('invoices/'+filename))
#             # print(invoice_data.landman)
#     else:
#         form = DocumentForm() # A empty, unbound form
#     # Render list page with the form
#     return render(request, 'invoices/process.html', {'form': form})
