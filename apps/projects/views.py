from django.http import Http404
from django.views.generic import TemplateView


class ProjectListView(TemplateView):
    template_name = "pages/projects.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project_bands"] = [
            {
                "image": "img/projects/projects-band-1-recovered.png",
                "title": "SED UT\nPERSPICIATIS",
                "count": "13  /  20",
                "filter": True,
            },
            {
                "image": "img/projects/projects-band-2-recovered.png",
                "title": "SED UT\nPERSPICIATIS",
            },
            {
                "image": "img/projects/projects-band-3-recovered.png",
                "title": "SED UT\nPERSPICIATIS",
            },
            {
                "image": "img/projects/projects-band-4-recovered.png",
                "title": "SED UT\nPERSPICIATIS",
                "modifier": "project-band--tower",
            },
        ]
        return context


class ProjectDetailView(TemplateView):
    template_name = "pages/project_detail.html"
    reference_slug = "sed-ut-perspiciatis"

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get("slug") != self.reference_slug:
            raise Http404("Project not found")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = {
            "slug": self.reference_slug,
            "title": "SED UT\nPERSPICIATIS",
            "image": "img/projects/project-detail-tower-recovered.png",
            "description": [
                "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem.",
                "Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page",
                "editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will",
            ],
            "info": {
                "date": "12/1/2017",
                "client": "House creavite",
                "status": "completed",
                "location": "New york",
            },
        }
        return context
