from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from .models import Project, ProjectCategory


class ProjectListView(ListView):
    model = Project
    template_name = "pages/projects.html"
    context_object_name = "projects"
    paginate_by = 6

    def get_queryset(self):
        queryset = Project.objects.select_related("category").all()

        # Category Filter
        category_slug = self.request.GET.get("category")
        if category_slug and category_slug != "all":
            queryset = queryset.filter(category__slug=category_slug)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Categories with actual project count
        context["categories"] = ProjectCategory.objects.annotate(
            projects_count=Count("project")
        )
        context["total_all_projects_count"] = Project.objects.count()
        context["selected_category"] = self.request.GET.get("category", "all")

        # Build query string for pagination without 'page' param
        params = self.request.GET.copy()
        if "page" in params:
            params.pop("page")
        context["querystring_without_page"] = params.urlencode()

        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = "pages/project_detail.html"
    context_object_name = "project"
    slug_url_kwarg = "slug"

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        # Legacy fallback if demo slug requested
        if slug == "sed-ut-perspiciatis" and not Project.objects.filter(slug=slug).exists():
            first_project = Project.objects.first()
            if first_project:
                return first_project
        return get_object_or_404(
            Project.objects.prefetch_related("images").select_related("category"),
            slug=slug
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object

        # Previous and Next project navigation
        context["prev_project"] = (
            Project.objects.filter(order__lt=project.order).order_by("-order", "-id").first()
            or Project.objects.filter(id__lt=project.id).order_by("-id").first()
        )
        context["next_project"] = (
            Project.objects.filter(order__gt=project.order).order_by("order", "id").first()
            or Project.objects.filter(id__gt=project.id).order_by("id").first()
        )

        # Related projects (same category first, topped up with latest projects up to 4)
        related_qs = Project.objects.exclude(id=project.id).select_related("category")
        if project.category:
            same_cat = list(related_qs.filter(category=project.category)[:4])
            if len(same_cat) < 4:
                other_projects = list(related_qs.exclude(id__in=[p.id for p in same_cat])[: 4 - len(same_cat)])
                context["related_projects"] = same_cat + other_projects
            else:
                context["related_projects"] = same_cat
        else:
            context["related_projects"] = list(related_qs[:4])

        return context
