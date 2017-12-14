from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import FileUploadForm
import logging

class DocUploadView(FormView):
    form_class = FileUploadForm
    template_name = "dcompare/doc_upload.html"
    success_url = '/admin'

    # def get(self, request, *args, **kwargs):
    #     logger = logging.getLogger(__name__)
    #     logger.debug("hello world")
    #     return super(DocUploadView, self).get(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        logger = logging.getLogger(__name__)

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        files = request.FILES.getlist('documents')
        logger.debug('file is {}'.format(form.is_valid()))
        if form.is_valid():
            for f in files:
                logger.debug(type(f))
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
