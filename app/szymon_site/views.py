from django.views import generic
from .models import PdfAttachment


class IndexTemplateView(generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        # Add your context data here
        context = super().get_context_data(**kwargs)
        obj_pdf = PdfAttachment.objects.last().pdf_file.url
        context['pdf_file'] = obj_pdf
        return context