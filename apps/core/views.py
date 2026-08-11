from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View

from .forms import ContactForm


class HomeView(TemplateView):
    template_name = "pages/home.html"


class AboutView(TemplateView):
    template_name = "pages/about.html"


class ContactView(View):
    template_name = "pages/contact.html"

    def get_context_data(self, form=None):
        return {
            "form": form or ContactForm(),
            "show_footer_quote": True,
            "footer_copyright": "© MOONLIGT 2017. ALL RIGHTS RESERVED",
            "footer_quote_text": (
                "It is a long established fact that a reader will be distracted by the "
                "readable content of a page when looking at its layout."
            ),
        }

    def get(self, request):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("core:contact")
        return render(request, self.template_name, self.get_context_data(form=form), status=400)
