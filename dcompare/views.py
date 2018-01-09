import logging
import os
import json
from tempfile import NamedTemporaryFile

from django.shortcuts import render
from django.http import Http404
from django.views.generic.edit import FormView
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from .forms import FileUploadForm
from .api.runword import run2


def display_table(request):
    logger = logging.getLogger(__name__)
    template = 'dcompare/table.html'

    if 'compare_obj' not in request.session:
        return Http404("Cannot find processed files.")
    else:
        obj = None
        with open(request.session['compare_obj']) as f:
            obj = json.loads(f.read())

        print(obj['structure'])
        return render(request, template, {'compare_table': obj})

# class DocUploadView(FormView):
#     form_class = FileUploadForm
#     template_name = "dcompare/doc_upload.html"
#     success_url = '/compare/success'
#
#     def post(self, request, *args, **kwargs):
#         request.upload_handlers = [TemporaryFileUploadHandler(request)]
#         return self._post(request, *args, **kwargs)
#
#     def _post(self, request, *args, **kwargs):
#         logger = logging.getLogger(__name__)
#
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#
#         files = request.FILES.getlist('documents')
#         # logger.debug('file is {}'.format(form.is_valid()))
#         if form.is_valid():
#             request.session['compare_files'] = [f.temporary_file_path() for f in files]
#             for f in request.session['compare_files']:
#                 logger.debug(os.path.exists(f))
#             request.session['filenames'] = [f.name for f in files]
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)

@method_decorator(csrf_exempt, 'dispatch')
class DocUploadView(FormView):
    form_class = FileUploadForm
    template_name = "dcompare/doc_upload.html"
    success_url = '/compare/success'


    def post(self, request, *args, **kwargs):
        request.upload_handlers = [TemporaryFileUploadHandler(request=request)]
        return self._post(request)

    @method_decorator(csrf_protect)
    def _post(self, request, *args, **kwargs):
        logger = logging.getLogger(__name__)

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        files = request.FILES.getlist('documents')
        # logger.debug('file is {}'.format(form.is_valid()))
        if form.is_valid():
            process_files  = [f.temporary_file_path() for f in files]
            filenames = [f.name for f in files]
            doc_struct = []
            gen = run2(process_files, doc_struct)
            sections =  [s for s in gen]
            save_obj = {'filenames': filenames, 'components': sections, 'structure': doc_struct}

            with NamedTemporaryFile(delete = False) as f:
                f.write(json.dumps(save_obj).encode('utf-8'))
                request.session['compare_obj'] = f.name
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
