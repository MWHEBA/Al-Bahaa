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
        return {"form": form or ContactForm()}

    def get(self, request):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("core:contact")
        return render(request, self.template_name, self.get_context_data(form=form), status=400)
