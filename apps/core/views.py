from django.core.mail import send_mail
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import TemplateView

from apps.news.models import Post
from apps.projects.models import Project
from .forms import ContactForm, JobApplicationForm
from .models import (
    AboutContent,
    AboutStatistic,
    CareerPillar,
    CareerSettings,
    ClientLogo,
    CompanyPillar,
    ContactMessage,
    HomeContent,
    JobApplication,
    JobDepartment,
    JobOpening,
    ServiceItem,
    SiteSettings,
    SpecializationItem,
    TeamMember,
    Testimonial,
)


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        featured_projects = list(Project.objects.select_related("category").all()[:6])

        specializations = list(SpecializationItem.objects.filter(is_active=True))
        # Format for JS consumption
        specializations_json = [
            {
                "discipline": s.discipline,
                "title": s.title,
                "description": s.description,
            }
            for s in specializations
        ]

        context["home_content"] = HomeContent.load()
        context["specializations"] = specializations
        context["specializations_json"] = specializations_json
        context["featured_projects"] = featured_projects
        context["featured_project"] = featured_projects[0] if featured_projects else None
        context["testimonials"] = Testimonial.objects.filter(show_on_home=True)[:3]
        context["clients"] = ClientLogo.objects.filter(show_on_home=True, is_active=True)[:12]
        context["latest_posts"] = list(Post.objects.select_related("category").filter(is_published=True)[:3])
        return context


class AboutView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["about_content"] = AboutContent.load()
        context["statistics"] = AboutStatistic.objects.filter(is_active=True)
        context["pillars"] = CompanyPillar.objects.filter(is_active=True)
        context["services"] = ServiceItem.objects.filter(is_active=True)

        founder = TeamMember.objects.filter(member_type="founder", is_active=True).first()
        board_members = TeamMember.objects.filter(member_type="executive", is_active=True)
        general_members = TeamMember.objects.filter(member_type="general", is_active=True)

        context["founder"] = founder
        context["board_members"] = board_members
        context["team_members"] = general_members
        context["testimonials"] = Testimonial.objects.filter(show_on_about=True)[:3]
        context["clients"] = ClientLogo.objects.filter(show_on_about=True, is_active=True)[:12]
        return context


class CareersView(TemplateView):
    template_name = "pages/careers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        departments_qs = JobDepartment.objects.annotate(
            active_jobs_count=Count("jobs", filter=Q(jobs__is_active=True))
        )

        all_active_jobs = JobOpening.objects.filter(is_active=True).select_related("department")

        selected_dept_slug = self.request.GET.get("department", "all")
        if selected_dept_slug and selected_dept_slug != "all":
            jobs = all_active_jobs.filter(department__slug=selected_dept_slug)
        else:
            selected_dept_slug = "all"
            jobs = all_active_jobs

        departments_with_counts = [
            {
                "name": dept.name,
                "slug": dept.slug,
                "count": dept.active_jobs_count,
            }
            for dept in departments_qs
        ]

        context["career_settings"] = CareerSettings.load()
        context["pillars"] = CareerPillar.objects.filter(is_active=True)
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
        prev_job = (
            JobOpening.objects.filter(is_active=True, order__lt=job.order).order_by("-order", "-id").first()
            or JobOpening.objects.filter(is_active=True, id__lt=job.id).order_by("-id").first()
        )
        next_job = (
            JobOpening.objects.filter(is_active=True, order__gt=job.order).order_by("order", "id").first()
            or JobOpening.objects.filter(is_active=True, id__gt=job.id).order_by("id").first()
        )

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

            # Optional Notification Email
            settings_obj = SiteSettings.load()
            dest_email = settings_obj.email_careers or "careers@albahaacontracting.com"
            try:
                send_mail(
                    subject=f"[New Application] {app_instance.full_name} - {job.title}",
                    message=f"New candidate applied for {job.title}.\nName: {app_instance.full_name}\nEmail: {app_instance.email}\nPhone: {app_instance.phone}\nCover Note: {app_instance.cover_note}",
                    from_email=None,
                    recipient_list=[dest_email],
                    fail_silently=True,
                )
            except Exception:
                pass

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
        is_ajax = (
            request.headers.get("x-requested-with") == "XMLHttpRequest"
            or "application/json" in request.headers.get("accept", "")
        )

        if form.is_valid():
            msg_instance = form.save()

            # Optional Notification Email
            settings_obj = SiteSettings.load()
            dest_email = settings_obj.email_tenders if msg_instance.inquiry_type == "tenders" else settings_obj.email_general
            try:
                send_mail(
                    subject=f"[New Inquiry] {msg_instance.name} ({msg_instance.get_inquiry_type_display()})",
                    message=f"New contact inquiry received:\nFrom: {msg_instance.name}\nCompany: {msg_instance.company}\nEmail: {msg_instance.email}\nPhone: {msg_instance.phone}\nType: {msg_instance.get_inquiry_type_display()}\n\nMessage:\n{msg_instance.message}",
                    from_email=None,
                    recipient_list=[dest_email or "info@albahaacontracting.com"],
                    fail_silently=True,
                )
            except Exception:
                pass

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
