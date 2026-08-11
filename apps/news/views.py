from django.views.generic import TemplateView


class NewsFoundationView(TemplateView):
    template_name = "pages/foundation.html"
