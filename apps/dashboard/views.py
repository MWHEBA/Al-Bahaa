import csv
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)

from apps.core.models import (
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
    PageHero,
    ServiceItem,
    SiteSettings,
    SpecializationItem,
    TeamMember,
    Testimonial,
)
from apps.news.models import NewsCategory, Post
from apps.projects.models import Project, ProjectCategory, ProjectImage
from .forms import (
    ClientLogoForm,
    ContactMessageReviewForm,
    ExecutiveProfileForm,
    JobApplicationReviewForm,
    JobDepartmentForm,
    JobOpeningForm,
    NewsCategoryForm,
    PageHeroForm,
    PostForm,
    ProjectCategoryForm,
    ProjectForm,
    SiteSettingsForm,
    TeamMemberForm,
    TestimonialForm,
)


class StaffRequiredMixin(UserPassesTestMixin):
    """Ensure user is authenticated and is a staff member."""

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(f"{reverse('dashboard:login')}?next={self.request.path}")
        return HttpResponseForbidden("Access restricted to authorized executive staff.")


# ==========================================
# 1. AUTHENTICATION & PROFILE VIEWS
# ==========================================
class DashboardLoginView(FormView):
    template_name = "dashboard/login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("dashboard:overview")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return redirect("dashboard:overview")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_staff:
            messages.error(self.request, "Your account does not have executive staff access permissions.")
            return self.form_invalid(form)
        login(self.request, user)
        messages.success(self.request, f"Welcome back, {user.get_full_name() or user.username}!")
        next_url = self.request.GET.get("next") or self.success_url
        return redirect(next_url)


class DashboardLogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have been securely signed out.")
        return redirect("dashboard:login")

    def post(self, request):
        logout(request)
        messages.info(request, "You have been securely signed out.")
        return redirect("dashboard:login")


class DashboardProfileView(StaffRequiredMixin, View):
    template_name = "dashboard/profile.html"

    def get(self, request):
        user_form = ExecutiveProfileForm(instance=request.user)
        pw_form = PasswordChangeForm(user=request.user)
        return render(request, self.template_name, {"user_form": user_form, "pw_form": pw_form})

    def post(self, request):
        action = request.POST.get("action")
        user_form = ExecutiveProfileForm(instance=request.user)
        pw_form = PasswordChangeForm(user=request.user)

        if action == "update_profile":
            user_form = ExecutiveProfileForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, "Your executive profile details were successfully updated.")
                return redirect("dashboard:profile")

        elif action == "change_password":
            pw_form = PasswordChangeForm(user=request.user, data=request.POST)
            if pw_form.is_valid():
                user = pw_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Your account password was successfully updated.")
                return redirect("dashboard:profile")

        return render(request, self.template_name, {"user_form": user_form, "pw_form": pw_form})


# ==========================================
# 2. OVERVIEW & KPI DASHBOARD
# ==========================================
class DashboardOverviewView(StaffRequiredMixin, TemplateView):
    template_name = "dashboard/overview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["kpis"] = {
            "projects_count": Project.objects.count(),
            "active_jobs_count": JobOpening.objects.filter(is_active=True).count(),
            "new_applications_count": JobApplication.objects.filter(status="new").count(),
            "total_applications_count": JobApplication.objects.count(),
            "unread_inquiries_count": ContactMessage.objects.filter(status="unread").count(),
            "tender_inquiries_count": ContactMessage.objects.filter(inquiry_type="tenders", status="unread").count(),
            "published_articles_count": Post.objects.filter(is_published=True).count(),
            "partners_count": ClientLogo.objects.filter(is_active=True).count(),
        }
        context["recent_applications"] = JobApplication.objects.select_related("job").order_by("-submitted_at")[:5]
        context["recent_inquiries"] = ContactMessage.objects.order_by("-created_at")[:5]
        context["recent_projects"] = Project.objects.select_related("category").order_by("-date", "-id")[:4]
        return context


# ==========================================
# 3. PROJECTS MANAGEMENT
# ==========================================
class ProjectListView(StaffRequiredMixin, ListView):
    model = Project
    template_name = "dashboard/projects/list.html"
    context_object_name = "projects"
    paginate_by = 15

    def get_queryset(self):
        qs = Project.objects.select_related("category").prefetch_related("images").all()
        q = self.request.GET.get("q", "").strip()
        category = self.request.GET.get("category", "").strip()
        status = self.request.GET.get("status", "").strip()

        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(location__icontains=q) | Q(client_name__icontains=q))
        if category:
            qs = qs.filter(category__slug=category)
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ProjectCategory.objects.all()
        context["selected_category"] = self.request.GET.get("category", "")
        context["selected_status"] = self.request.GET.get("status", "")
        context["search_query"] = self.request.GET.get("q", "")
        return context


class ProjectCreateView(StaffRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "dashboard/projects/form.html"
    success_url = reverse_lazy("dashboard:projects_list")

    def form_valid(self, form):
        project = form.save()
        # Process multi-image gallery upload
        gallery_files = self.request.FILES.getlist("gallery_images")
        for idx, g_file in enumerate(gallery_files):
            ProjectImage.objects.create(
                project=project,
                image=g_file,
                caption=f"{project.title} - Photo {idx + 1}",
                order=idx + 1,
            )
        messages.success(self.request, f"Project '{project.title}' successfully created with {len(gallery_files)} gallery photos.")
        return redirect("dashboard:projects_edit", pk=project.pk)


class ProjectUpdateView(StaffRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "dashboard/projects/form.html"

    def form_valid(self, form):
        project = form.save()
        # Process multi-image gallery upload
        gallery_files = self.request.FILES.getlist("gallery_images")
        if gallery_files:
            current_count = project.images.count()
            for idx, g_file in enumerate(gallery_files):
                ProjectImage.objects.create(
                    project=project,
                    image=g_file,
                    caption=f"{project.title} - Photo {current_count + idx + 1}",
                    order=current_count + idx + 1,
                )
            messages.success(self.request, f"Project updated and {len(gallery_files)} new photos added to gallery.")
        else:
            messages.success(self.request, f"Project '{project.title}' specifications updated successfully.")
        return redirect("dashboard:projects_edit", pk=project.pk)


class ProjectDeleteView(StaffRequiredMixin, DeleteView):
    model = Project
    template_name = "dashboard/projects/confirm_delete.html"
    success_url = reverse_lazy("dashboard:projects_list")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        title = obj.title
        messages.success(request, f"Project '{title}' and its associated gallery were permanently deleted.")
        return super().delete(request, *args, **kwargs)


class ProjectGalleryImageDeleteView(StaffRequiredMixin, View):
    def post(self, request, pk):
        image_obj = get_object_or_404(ProjectImage, pk=pk)
        project_pk = image_obj.project.pk
        image_obj.delete()
        messages.success(request, "Gallery photo removed successfully.")
        return redirect("dashboard:projects_edit", pk=project_pk)


class ProjectCategoryManageView(StaffRequiredMixin, View):
    template_name = "dashboard/projects/categories.html"

    def get(self, request):
        categories = ProjectCategory.objects.annotate(proj_count=Count("project")).order_by("order", "name")
        form = ProjectCategoryForm()
        return render(request, self.template_name, {"categories": categories, "form": form})

    def post(self, request):
        action = request.POST.get("action")
        if action == "create":
            form = ProjectCategoryForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "New project category added.")
        elif action == "delete":
            cat_id = request.POST.get("category_id")
            cat = get_object_or_404(ProjectCategory, pk=cat_id)
            cat.delete()
            messages.success(request, f"Category '{cat.name}' removed.")
        return redirect("dashboard:projects_categories")


# ==========================================
# 4. NEWS & ARTICLES MANAGEMENT
# ==========================================
class NewsListView(StaffRequiredMixin, ListView):
    model = Post
    template_name = "dashboard/news/list.html"
    context_object_name = "posts"
    paginate_by = 15

    def get_queryset(self):
        qs = Post.objects.select_related("category").all()
        q = self.request.GET.get("q", "").strip()
        category = self.request.GET.get("category", "").strip()
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(author__icontains=q) | Q(content__icontains=q))
        if category:
            qs = qs.filter(category__slug=category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = NewsCategory.objects.all()
        context["selected_category"] = self.request.GET.get("category", "")
        context["search_query"] = self.request.GET.get("q", "")
        return context


class NewsCreateView(StaffRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "dashboard/news/form.html"
    success_url = reverse_lazy("dashboard:news_list")

    def form_valid(self, form):
        post = form.save()
        messages.success(self.request, f"Article '{post.title}' published successfully.")
        return redirect("dashboard:news_edit", pk=post.pk)


class NewsUpdateView(StaffRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "dashboard/news/form.html"

    def form_valid(self, form):
        post = form.save()
        messages.success(self.request, f"Article '{post.title}' updated successfully.")
        return redirect("dashboard:news_edit", pk=post.pk)


class NewsDeleteView(StaffRequiredMixin, DeleteView):
    model = Post
    template_name = "dashboard/news/confirm_delete.html"
    success_url = reverse_lazy("dashboard:news_list")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        title = obj.title
        messages.success(request, f"Article '{title}' deleted successfully.")
        return super().delete(request, *args, **kwargs)


# ==========================================
# 5. CAREERS & RECRUITMENT MANAGEMENT
# ==========================================
class JobOpeningListView(StaffRequiredMixin, ListView):
    model = JobOpening
    template_name = "dashboard/careers/jobs_list.html"
    context_object_name = "jobs"
    paginate_by = 15

    def get_queryset(self):
        return JobOpening.objects.select_related("department").annotate(applicants_count=Count("applications")).order_by("order", "-created_at")


class JobOpeningCreateView(StaffRequiredMixin, CreateView):
    model = JobOpening
    form_class = JobOpeningForm
    template_name = "dashboard/careers/job_form.html"
    success_url = reverse_lazy("dashboard:careers_jobs")

    def form_valid(self, form):
        job = form.save()
        messages.success(self.request, f"Job opening '{job.title}' created successfully.")
        return redirect("dashboard:careers_jobs")


class JobOpeningUpdateView(StaffRequiredMixin, UpdateView):
    model = JobOpening
    form_class = JobOpeningForm
    template_name = "dashboard/careers/job_form.html"
    success_url = reverse_lazy("dashboard:careers_jobs")

    def form_valid(self, form):
        job = form.save()
        messages.success(self.request, f"Job opening '{job.title}' specifications updated.")
        return redirect("dashboard:careers_jobs")


class JobOpeningDeleteView(StaffRequiredMixin, DeleteView):
    model = JobOpening
    template_name = "dashboard/careers/confirm_delete.html"
    success_url = reverse_lazy("dashboard:careers_jobs")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        title = obj.title
        messages.success(request, f"Job opening '{title}' deleted successfully.")
        return super().delete(request, *args, **kwargs)


class JobApplicationListView(StaffRequiredMixin, ListView):
    model = JobApplication
    template_name = "dashboard/careers/applications_list.html"
    context_object_name = "applications"
    paginate_by = 15

    def get_queryset(self):
        qs = JobApplication.objects.select_related("job", "job__department").all()
        q = self.request.GET.get("q", "").strip()
        status = self.request.GET.get("status", "").strip()
        job_id = self.request.GET.get("job", "").strip()

        if q:
            qs = qs.filter(Q(full_name__icontains=q) | Q(email__icontains=q) | Q(phone__icontains=q))
        if status:
            qs = qs.filter(status=status)
        if job_id:
            qs = qs.filter(job_id=job_id)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["jobs"] = JobOpening.objects.all()
        context["selected_status"] = self.request.GET.get("status", "")
        context["selected_job"] = self.request.GET.get("job", "")
        context["search_query"] = self.request.GET.get("q", "")
        return context


class JobApplicationDetailView(StaffRequiredMixin, View):
    template_name = "dashboard/careers/application_detail.html"

    def get(self, request, pk):
        app = get_object_or_404(JobApplication.objects.select_related("job"), pk=pk)
        form = JobApplicationReviewForm(instance=app)
        return render(request, self.template_name, {"application": app, "form": form})

    def post(self, request, pk):
        app = get_object_or_404(JobApplication.objects.select_related("job"), pk=pk)
        form = JobApplicationReviewForm(request.POST, instance=app)
        if form.is_valid():
            form.save()
            messages.success(request, f"Candidate evaluation for '{app.full_name}' updated.")
            return redirect("dashboard:careers_application_detail", pk=app.pk)
        return render(request, self.template_name, {"application": app, "form": form})


class JobApplicationQuickStatusView(StaffRequiredMixin, View):
    def post(self, request, pk):
        app = get_object_or_404(JobApplication, pk=pk)
        new_status = request.POST.get("status")
        valid_statuses = dict(JobApplication.STATUS_CHOICES).keys()
        if new_status in valid_statuses:
            app.status = new_status
            app.save()
            return JsonResponse({"success": True, "status": app.status, "status_display": app.get_status_display()})
        return JsonResponse({"success": False, "error": "Invalid status value"}, status=400)


class ExportApplicationsCsvView(StaffRequiredMixin, View):
    def get(self, request):
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="AlBahaa_Job_Applications.csv"'
        writer = csv.writer(response)
        writer.writerow(["Full Name", "Applied Role", "Email", "Phone", "Status", "Date Submitted", "CV File URL", "Cover Note"])

        apps = JobApplication.objects.select_related("job").order_by("-submitted_at")
        for a in apps:
            cv_url = request.build_absolute_uri(a.resume.url) if a.resume else "N/A"
            writer.writerow([
                a.full_name,
                a.job.title,
                a.email,
                a.phone,
                a.get_status_display(),
                a.submitted_at.strftime("%Y-%m-%d %H:%M"),
                cv_url,
                a.cover_note,
            ])
        return response


# ==========================================
# 6. INQUIRIES MANAGEMENT
# ==========================================
class InquiriesListView(StaffRequiredMixin, ListView):
    model = ContactMessage
    template_name = "dashboard/inquiries/list.html"
    context_object_name = "inquiries"
    paginate_by = 15

    def get_queryset(self):
        qs = ContactMessage.objects.all()
        q = self.request.GET.get("q", "").strip()
        inquiry_type = self.request.GET.get("type", "").strip()
        status = self.request.GET.get("status", "").strip()

        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(company__icontains=q) | Q(email__icontains=q) | Q(phone__icontains=q))
        if inquiry_type:
            qs = qs.filter(inquiry_type=inquiry_type)
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_type"] = self.request.GET.get("type", "")
        context["selected_status"] = self.request.GET.get("status", "")
        context["search_query"] = self.request.GET.get("q", "")
        return context


class InquiryDetailView(StaffRequiredMixin, View):
    template_name = "dashboard/inquiries/detail.html"

    def get(self, request, pk):
        inquiry = get_object_or_404(ContactMessage, pk=pk)
        if inquiry.status == "unread":
            inquiry.status = "read"
            inquiry.is_read = True
            inquiry.save()
        form = ContactMessageReviewForm(instance=inquiry)
        default_subject = f"Re: {inquiry.get_inquiry_type_display()} - Al Bahaa Contracting"
        default_reply_body = (
            f"Dear {inquiry.name},\n\n"
            f"Thank you for reaching out to Al Bahaa Contracting regarding '{inquiry.get_inquiry_type_display()}'.\n\n"
            f"We have thoroughly reviewed your inquiry and would like to inform you that ...\n\n"
            f"Should you have any further questions or require immediate engineering assistance, please feel free to reply to this email or call our headquarters.\n\n"
            f"Best regards,\n"
            f"Al Bahaa Contracting & General Supplies\n"
            f"https://albahaacontracting.com"
        )
        return render(request, self.template_name, {
            "inquiry": inquiry,
            "form": form,
            "default_subject": default_subject,
            "default_reply_body": default_reply_body,
        })

    def post(self, request, pk):
        inquiry = get_object_or_404(ContactMessage, pk=pk)
        action = request.POST.get("action")

        if action == "send_reply":
            reply_subject = request.POST.get("reply_subject", "").strip()
            reply_body = request.POST.get("reply_body", "").strip()

            if not reply_subject or not reply_body:
                messages.error(request, "Subject and reply message body cannot be empty.")
            else:
                from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "info@albahaacontracting.com")
                try:
                    send_mail(
                        subject=reply_subject,
                        message=reply_body,
                        from_email=from_email,
                        recipient_list=[inquiry.email],
                        fail_silently=False,
                    )
                    timestamp = timezone.now().strftime("%Y-%m-%d %H:%M")
                    log_entry = f"--- [Official Email Reply Sent on {timestamp}] ---\nSubject: {reply_subject}\n\n{reply_body}\n\n"
                    inquiry.internal_notes = log_entry + (inquiry.internal_notes or "")
                    inquiry.status = "resolved"
                    inquiry.is_read = True
                    inquiry.save()
                    messages.success(request, f"Official reply email successfully dispatched to '{inquiry.email}'.")
                    return redirect("dashboard:inquiry_detail", pk=inquiry.pk)
                except Exception as e:
                    messages.error(request, f"Could not send email: {str(e)}")
            return redirect("dashboard:inquiry_detail", pk=inquiry.pk)
        else:
            form = ContactMessageReviewForm(request.POST, instance=inquiry)
            if form.is_valid():
                form.save()
                messages.success(request, "Inquiry status & internal notes saved.")
                return redirect("dashboard:inquiry_detail", pk=inquiry.pk)
            return render(request, self.template_name, {"inquiry": inquiry, "form": form})


class InquiryQuickStatusView(StaffRequiredMixin, View):
    def post(self, request, pk):
        inquiry = get_object_or_404(ContactMessage, pk=pk)
        new_status = request.POST.get("status")
        valid_statuses = dict(ContactMessage.STATUS_CHOICES).keys()
        if new_status in valid_statuses:
            inquiry.status = new_status
            if new_status in ["read", "resolved"]:
                inquiry.is_read = True
            inquiry.save()
            return JsonResponse({"success": True, "status": inquiry.status, "status_display": inquiry.get_status_display()})
        return JsonResponse({"success": False, "error": "Invalid status value"}, status=400)


class ExportInquiriesCsvView(StaffRequiredMixin, View):
    def get(self, request):
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="AlBahaa_Contact_Inquiries.csv"'
        writer = csv.writer(response)
        writer.writerow(["Client Name", "Company", "Inquiry Type", "Email", "Phone", "Status", "Date Submitted", "Message Body", "Internal Notes"])

        inquiries = ContactMessage.objects.order_by("-created_at")
        for i in inquiries:
            writer.writerow([
                i.name,
                i.company,
                i.get_inquiry_type_display(),
                i.email,
                i.phone,
                i.get_status_display(),
                i.created_at.strftime("%Y-%m-%d %H:%M"),
                i.message,
                i.internal_notes,
            ])
        return response


# ==========================================
# 7. SETTINGS, HEROES, CLIENTS & TEAM
# ==========================================
class SiteSettingsEditView(StaffRequiredMixin, View):
    template_name = "dashboard/settings/general.html"

    def get(self, request):
        settings_obj = SiteSettings.load()
        form = SiteSettingsForm(instance=settings_obj)
        return render(request, self.template_name, {"form": form, "settings": settings_obj})

    def post(self, request):
        settings_obj = SiteSettings.load()
        if request.POST.get("header_logo-clear") and settings_obj.header_logo:
            settings_obj.header_logo.delete(save=False)
            settings_obj.header_logo = ""
        if request.POST.get("footer_logo-clear") and settings_obj.footer_logo:
            settings_obj.footer_logo.delete(save=False)
            settings_obj.footer_logo = ""
        if request.POST.get("favicon-clear") and settings_obj.favicon:
            settings_obj.favicon.delete(save=False)
            settings_obj.favicon = ""
        form = SiteSettingsForm(request.POST, request.FILES, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Corporate site settings and contact parameters updated.")
            return redirect("dashboard:settings_general")
        return render(request, self.template_name, {"form": form, "settings": settings_obj})


class PageHeroesManageView(StaffRequiredMixin, View):
    template_name = "dashboard/settings/heroes.html"

    def get(self, request):
        heroes = PageHero.objects.all()
        return render(request, self.template_name, {"heroes": heroes})


class PageHeroEditView(StaffRequiredMixin, UpdateView):
    model = PageHero
    form_class = PageHeroForm
    template_name = "dashboard/settings/hero_form.html"
    success_url = reverse_lazy("dashboard:settings_heroes")

    def form_valid(self, form):
        hero = form.save()
        messages.success(self.request, f"{hero.get_page_display()} banner updated.")
        return redirect("dashboard:settings_heroes")


class ClientLogosManageView(StaffRequiredMixin, View):
    template_name = "dashboard/clients/list.html"

    def get(self, request):
        logos = ClientLogo.objects.all().order_by("order", "name")
        edit_id = request.GET.get("edit")
        editing_logo = None
        if edit_id:
            try:
                editing_logo = ClientLogo.objects.get(pk=edit_id)
                form = ClientLogoForm(instance=editing_logo)
            except ClientLogo.DoesNotExist:
                form = ClientLogoForm()
        else:
            form = ClientLogoForm()
        return render(request, self.template_name, {
            "logos": logos,
            "form": form,
            "editing_logo": editing_logo,
        })

    def post(self, request):
        action = request.POST.get("action")
        if action == "create":
            form = ClientLogoForm(request.POST, request.FILES)
            if form.is_valid():
                logo = form.save()
                messages.success(request, f"Partner logo '{logo.name}' added successfully.")
            else:
                messages.error(request, "Please correct the form errors.")
                logos = ClientLogo.objects.all().order_by("order", "name")
                return render(request, self.template_name, {"logos": logos, "form": form})
        elif action == "update":
            logo_id = request.POST.get("logo_id")
            logo = get_object_or_404(ClientLogo, pk=logo_id)
            if request.POST.get("logo-clear") and logo.logo_image:
                logo.logo_image.delete(save=False)
                logo.logo_image = ""
            form = ClientLogoForm(request.POST, request.FILES, instance=logo)
            if form.is_valid():
                form.save()
                messages.success(request, f"Partner logo '{logo.name}' updated successfully.")
            else:
                messages.error(request, "Failed to update partner logo. Please check the fields.")
                logos = ClientLogo.objects.all().order_by("order", "name")
                return render(request, self.template_name, {"logos": logos, "form": form, "editing_logo": logo})
        elif action == "delete":
            logo_id = request.POST.get("logo_id")
            logo = get_object_or_404(ClientLogo, pk=logo_id)
            name = logo.name
            logo.delete()
            messages.success(request, f"Partner logo '{name}' removed.")
        return redirect("dashboard:clients_manage")


class ClientLogoEditView(StaffRequiredMixin, View):
    def get(self, request, pk):
        return redirect(f"{reverse('dashboard:clients_manage')}?edit={pk}")


class TeamManageView(StaffRequiredMixin, View):
    template_name = "dashboard/team/list.html"

    def get(self, request):
        members = TeamMember.objects.all().order_by("order", "name")

        # Edit mode
        edit_id = request.GET.get("edit")
        editing_member = None
        if edit_id:
            try:
                editing_member = TeamMember.objects.get(pk=edit_id)
                form = TeamMemberForm(instance=editing_member)
            except TeamMember.DoesNotExist:
                form = TeamMemberForm()
        else:
            form = TeamMemberForm()

        context = {
            "members": members,
            "form": form,
            "editing_member": editing_member,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        action = request.POST.get("action")
        if action == "create":
            form = TeamMemberForm(request.POST, request.FILES)
            if form.is_valid():
                member = form.save()
                messages.success(request, f"Team member '{member.name}' added successfully.")
            else:
                messages.error(request, "Please correct the errors in the form.")
                members = TeamMember.objects.all().order_by("order", "name")
                return render(request, self.template_name, {"members": members, "form": form})
        elif action == "update":
            member_id = request.POST.get("member_id")
            member = get_object_or_404(TeamMember, pk=member_id)
            if request.POST.get("photo-clear") and member.photo:
                member.photo.delete(save=False)
                member.photo = ""
            form = TeamMemberForm(request.POST, request.FILES, instance=member)
            if form.is_valid():
                form.save()
                messages.success(request, f"Leadership profile '{member.name}' updated successfully.")
            else:
                messages.error(request, "Failed to update member. Please check the fields.")
                members = TeamMember.objects.all().order_by("order", "name")
                return render(request, self.template_name, {"members": members, "form": form, "editing_member": member})
        elif action == "delete":
            member_id = request.POST.get("member_id")
            member = get_object_or_404(TeamMember, pk=member_id)
            name = member.name
            member.delete()
            messages.success(request, f"Team member '{name}' removed.")
        return redirect("dashboard:team_manage")


class TeamMemberEditView(StaffRequiredMixin, View):
    def get(self, request, pk):
        return redirect(f"{reverse('dashboard:team_manage')}?edit={pk}")
