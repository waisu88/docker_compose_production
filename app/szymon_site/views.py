from django.views import generic
from .models import PdfAttachment


class IndexTemplateView(generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        # Add your context data here
        context = super().get_context_data(**kwargs)
        obj_pdf = PdfAttachment.objects.last()
        if obj_pdf:
            context['pdf_file'] = obj_pdf.pdf_file.url
        return context