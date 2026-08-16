from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import TemplateView

from apps.projects.models import Project
from .forms import ContactForm, JobApplicationForm
from .models import (
    ClientLogo,
    ContactMessage,
    JobApplication,
    JobDepartment,
    JobOpening,
    ServiceItem,
    SiteSettings,
    TeamMember,
    Testimonial,
)


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        featured_projects = list(Project.objects.select_related("category").all()[:6])
        context["settings"] = SiteSettings.load()
        context["featured_projects"] = featured_projects
        context["featured_project"] = featured_projects[0] if featured_projects else None
        context["testimonials"] = Testimonial.objects.filter(is_featured=True)[:3]
        context["clients"] = ClientLogo.objects.all()[:12]
        context["services"] = ServiceItem.objects.all()[:4]
        return context


class AboutView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team_members"] = TeamMember.objects.all()
        context["testimonials"] = Testimonial.objects.filter(is_featured=True)[:3]
        context["clients"] = ClientLogo.objects.all()[:12]
        context["settings"] = SiteSettings.load()
        return context


class CareersView(TemplateView):
    template_name = "pages/careers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        departments = list(JobDepartment.objects.all())
        all_active_jobs = JobOpening.objects.filter(is_active=True).select_related("department")

        # Calculate counts per department
        departments_with_counts = []
        for dept in departments:
            count = all_active_jobs.filter(department=dept).count()
            departments_with_counts.append({
                "name": dept.name,
                "slug": dept.slug,
                "count": count,
            })

        selected_dept_slug = self.request.GET.get("department", "all")
        if selected_dept_slug and selected_dept_slug != "all":
            jobs = all_active_jobs.filter(department__slug=selected_dept_slug)
        else:
            selected_dept_slug = "all"
            jobs = all_active_jobs

        context["total_all_jobs_count"] = all_active_jobs.count()
        context["selected_department"] = selected_dept_slug
        context["departments_with_counts"] = departments_with_counts
        context["jobs"] = jobs
        return context


class JobDetailView(View):
    template_name = "pages/job_detail.html"

    def get_job(self, slug):
        return get_object_or_404(
            JobOpening.objects.select_related("department"),
            slug=slug,
            is_active=True,
        )

    def get_context_data(self, job, form=None, application_success=False):
        # Previous and Next job navigation
        prev_job = (
            JobOpening.objects.filter(is_active=True, order__lt=job.order).order_by("-order", "-id").first()
            or JobOpening.objects.filter(is_active=True, id__lt=job.id).order_by("-id").first()
        )
        next_job = (
            JobOpening.objects.filter(is_active=True, order__gt=job.order).order_by("order", "id").first()
            or JobOpening.objects.filter(is_active=True, id__gt=job.id).order_by("id").first()
        )

        # Related jobs in the same department (or other departments)
        related_qs = JobOpening.objects.filter(is_active=True).exclude(id=job.id).select_related("department")
        if job.department:
            same_dept = list(related_qs.filter(department=job.department)[:3])
            if len(same_dept) < 3:
                other = list(related_qs.exclude(id__in=[j.id for j in same_dept])[: 3 - len(same_dept)])
                related_jobs = same_dept + other
            else:
                related_jobs = same_dept
        else:
            related_jobs = list(related_qs[:3])

        return {
            "job": job,
            "form": form or JobApplicationForm(),
            "prev_job": prev_job,
            "next_job": next_job,
            "related_jobs": related_jobs,
            "application_success": application_success,
        }

    def get(self, request, slug):
        job = self.get_job(slug)
        return render(request, self.template_name, self.get_context_data(job))

    def post(self, request, slug):
        job = self.get_job(slug)
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app_instance = form.save(commit=False)
            app_instance.job = job
            app_instance.save()
            return render(
                request,
                self.template_name,
                self.get_context_data(job, form=JobApplicationForm(), application_success=True),
            )
        return render(
            request,
            self.template_name,
            self.get_context_data(job, form=form, application_success=False),
            status=400,
        )


class ContactView(View):
    template_name = "pages/contact.html"

    def get_context_data(self, form=None, contact_success=False):
        return {
            "form": form or ContactForm(),
            "contact_success": contact_success,
        }

    def get(self, request):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request):
        form = ContactForm(request.POST)
        is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest" or "application/json" in request.headers.get("accept", "")

        if form.is_valid():
            form.save()
            if is_ajax:
                return JsonResponse({
                    "success": True,
                    "message": "Your inquiry has been successfully transmitted to our engineering and business development committee. We will review your project requirements and respond promptly.",
                })
            return render(
                request,
                self.template_name,
                self.get_context_data(form=ContactForm(), contact_success=True),
            )

        if is_ajax:
            errors = {}
            for field, field_errors in form.errors.items():
                errors[field] = [str(e) for e in field_errors]
            return JsonResponse({
                "success": False,
                "errors": errors,
                "message": "Please check the highlighted required fields.",
            }, status=400)

        return render(
            request,
            self.template_name,
            self.get_context_data(form=form, contact_success=False),
            status=400,
        )
