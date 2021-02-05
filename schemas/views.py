import mimetypes
import os
from wsgiref.util import FileWrapper

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView, CreateView
from django.urls import reverse_lazy

from test_task import settings
from .models import Schema, Dataset
from .tasks import create_csv_2


class SchemaListView(LoginRequiredMixin, ListView):
    model = Schema
    template_name = 'schemas/schema_list.html'


class SchemaDetailView(LoginRequiredMixin, DetailView):
    model = Schema
    context_object_name = 'schema'
    template_name = 'schemas/schema_detail.html'

    def get(self, request, **kwargs):
        if 'path' in request.GET:
            file_path = settings.BASE_DIR + '/' + request.GET['path']
            file_path = file_path.replace('/', '\\')
            file_wrapper = FileWrapper(open(file_path, 'rb'))
            file_mimetype = mimetypes.guess_type(file_path)
            response = HttpResponse(file_wrapper, content_type=file_mimetype)
            response['X-Sendfile'] = file_path
            response['Content-Length'] = os.stat(file_path).st_size
            response['Content-Disposition'] = 'attachment; filename=%s/' % str(request.GET['path'])
            return response
        elif 'rows-amount' in request.GET:
            dataset = Dataset(schema=self.get_object(),
                              status='Processing')
            dataset.save()

            # Pull task to celery
            create_csv_2.delay(dataset_pk=dataset.pk,
                               rows_amount=request.GET['rows-amount'],
                               column_separator=self.get_object().column_separator,
                               columns=self.get_object().columns)
            return HttpResponse('Dataset is in a creation queue!')

        else:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)


class SchemaDeleteView(LoginRequiredMixin, DeleteView):
    model = Schema
    template_name = 'schemas/schema_delete.html'
    success_url = reverse_lazy('schema_list')


class SchemaCreateView(LoginRequiredMixin, CreateView):
    model = Schema
    template_name = 'schemas/schema_new.html'
    fields = ('title', 'column_separator')
    success_url = reverse_lazy('schema_list')

    def post(self, request, **kwargs):
        schema = Schema(title=request.POST['title'],
                        column_separator=request.POST['column_separator'],
                        columns=request.POST['columns'])
        schema.save()
        return HttpResponse('Schema added!')
