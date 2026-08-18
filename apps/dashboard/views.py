import csv
import os
import re
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.cache import cache
from django.core.mail import BadHeaderError, send_mail
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count, Q
from django.http import FileResponse, Http404, HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
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
    AboutContentForm,
    AboutStatisticForm,
    CareerPillarForm,
    CareerSettingsForm,
    ClientLogoForm,
    CompanyPillarForm,
    ContactMessageReviewForm,
    ExecutiveProfileForm,
    HomeContentForm,
    JobApplicationReviewForm,
    JobDepartmentForm,
    JobOpeningForm,
    NewsCategoryForm,
    PageHeroForm,
    PostForm,
    ProjectCategoryForm,
    ProjectForm,
    ServiceItemForm,
    SiteSettingsForm,
    SpecializationItemForm,
    StaffUserCreateForm,
    StaffUserUpdateForm,
    TeamMemberForm,
    TestimonialForm,
)

User = get_user_model()


# ==========================================
# HELPER FUNCTIONS
# ==========================================
def invalidate_site_cache():
    """Immediately evicts cached site settings, page heroes, and footer links."""
    cache.delete("site_settings_cached")
    cache.delete("page_heroes_cached")
    cache.delete("footer_categories_cached")


def safe_delete_file(file_field):
    """Deletes physical file from filesystem to avoid orphaned media leaks."""
    if file_field and hasattr(file_field, "path"):
        try:
            if os.path.isfile(file_field.path):
                os.remove(file_field.path)
        except Exception:
            pass


def sanitize_csv_cell(val):
    """Neutralizes CSV Formula Injection (CWE-1236) by prepending a single quote to formula symbols."""
    if val is None:
        return ""
    text = str(val).strip()
    if text and text[0] in ("=", "+", "-", "@", "\t", "\r"):
        return f"'{text}"
    return text


def clean_email_header(text):
    """Strips newline and carriage return characters from subject to prevent header injection."""
    if not text:
        return ""
    return re.sub(r"[\r\n]+", " ", str(text)).strip()


# ==========================================
# ACCESS CONTROL MIXINS
# ==========================================
class StaffRequiredMixin(UserPassesTestMixin):
    """Ensure user is authenticated and is a staff member."""

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(f"{reverse('dashboard:login')}?next={self.request.path}")
        return HttpResponseForbidden("Access restricted to authorized executive staff.")


class SuperuserRequiredMixin(UserPassesTestMixin):
    """Ensure user is authenticated and is a superuser (Root Administrator)."""

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(f"{reverse('dashboard:login')}?next={self.request.path}")
        messages.error(self.request, "Access restricted: Superuser root administrative privileges required.")
        return redirect("dashboard:overview")


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

        # Open Redirect Defense (CWE-601)
        next_url = self.request.GET.get("next") or self.request.POST.get("next")
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={self.request.get_host()}):
            return redirect(next_url)
        return redirect(self.success_url)


class DashboardLogoutView(View):
    def post(self, request):
        logout(request)
        messages.info(request, "You have been securely signed out.")
        return redirect("dashboard:login")

    def get(self, request):
        # Fallback with safe sign-out
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
        if action == "update_profile":
            user_form = ExecutiveProfileForm(request.POST, instance=request.user)
            pw_form = PasswordChangeForm(user=request.user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, "Your executive profile details were updated successfully.")
                return redirect("dashboard:profile")
            messages.error(request, "Please correct the errors in your profile form.")
        elif action == "change_password":
            user_form = ExecutiveProfileForm(instance=request.user)
            pw_form = PasswordChangeForm(user=request.user, data=request.POST)
            if pw_form.is_valid():
                user = pw_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Your security password has been changed successfully.")
                return redirect("dashboard:profile")
            messages.error(request, "Please correct the password validation errors.")
        else:
            user_form = ExecutiveProfileForm(instance=request.user)
            pw_form = PasswordChangeForm(user=request.user)
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
            "testimonials_count": Testimonial.objects.count(),
        }
        context["recent_applications"] = JobApplication.objects.select_related("job").order_by("-submitted_at")[:5]
        context["recent_inquiries"] = ContactMessage.objects.order_by("-created_at")[:5]
        context["recent_projects"] = Project.objects.select_related("category").order_by("-date", "-id")[:4]
        return context


# ==========================================
# 3. PROJECTS & GALLERY MANAGEMENT
# ==========================================
class ProjectListView(StaffRequiredMixin, ListView):
    model = Project
    template_name = "dashboard/projects/list.html"
    context_object_name = "projects"
    paginate_by = 15

    def get_queryset(self):
        qs = Project.objects.select_related("category").all()
        q = self.request.GET.get("q", "").strip()[:80]
        category = self.request.GET.get("category", "").strip()
        status_val = self.request.GET.get("status", "").strip()
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(client_name__icontains=q) | Q(location__icontains=q))
        if category:
            qs = qs.filter(category__slug=category)
        if status_val in (Project.STATUS_ONGOING, Project.STATUS_COMPLETED):
            qs = qs.filter(status=status_val)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ProjectCategory.objects.all()
        context["selected_category"] = self.request.GET.get("category", "")
        context["selected_status"] = self.request.GET.get("status", "")
        context["q"] = self.request.GET.get("q", "").strip()[:80]
        context["hero"], _ = PageHero.objects.get_or_create(page="projects")

        params = self.request.GET.copy()
        if "page" in params:
            params.pop("page")
        context["querystring_without_page"] = params.urlencode()
        return context


class ProjectCreateView(StaffRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "dashboard/projects/form.html"

    @transaction.atomic
    def form_valid(self, form):
        project = form.save()
        gallery_files = self.request.FILES.getlist("gallery_images")
        if gallery_files:
            for idx, g_file in enumerate(gallery_files[:15]):
                ProjectImage.objects.create(
                    project=project,
                    image=g_file,
                    caption=f"{project.title} - Site Photo {idx + 1}",
                    order=idx + 1,
                )
        invalidate_site_cache()
        messages.success(self.request, f"Project '{project.title}' successfully created with {len(gallery_files)} gallery photos.")
        return redirect("dashboard:projects_edit", pk=project.pk)


class ProjectUpdateView(StaffRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "dashboard/projects/form.html"

    @transaction.atomic
    def form_valid(self, form):
        if self.request.POST.get("cover_image-clear") and self.object.cover_image:
            safe_delete_file(self.object.cover_image)
            self.object.cover_image = ""
        project = form.save()
        gallery_files = self.request.FILES.getlist("gallery_images")
        if gallery_files:
            current_count = project.images.count()
            for idx, g_file in enumerate(gallery_files[:15]):
                ProjectImage.objects.create(
                    project=project,
                    image=g_file,
                    caption=f"{project.title} - Site Photo {current_count + idx + 1}",
                    order=current_count + idx + 1,
                )
            messages.success(self.request, f"Project updated and {len(gallery_files)} new photos added to gallery.")
        else:
            messages.success(self.request, f"Project '{project.title}' specifications updated successfully.")
        invalidate_site_cache()
        return redirect("dashboard:projects_edit", pk=project.pk)


class ProjectDeleteView(StaffRequiredMixin, DeleteView):
    model = Project
    template_name = "dashboard/projects/confirm_delete.html"
    success_url = reverse_lazy("dashboard:projects_list")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        title = obj.title
        if obj.cover_image:
            safe_delete_file(obj.cover_image)
        for img in obj.images.all():
            safe_delete_file(img.image)
        invalidate_site_cache()
        messages.success(request, f"Project '{title}' and its associated gallery were permanently deleted.")
        return super().delete(request, *args, **kwargs)


class ProjectGalleryImageDeleteView(StaffRequiredMixin, View):
    def post(self, request, pk):
        image_obj = get_object_or_404(ProjectImage, pk=pk)
        project_pk = image_obj.project.pk
        safe_delete_file(image_obj.image)
        image_obj.delete()
        messages.success(request, "Gallery photo removed successfully.")
        return redirect("dashboard:projects_edit", pk=project_pk)


class ProjectCategoryManageView(StaffRequiredMixin, View):
    template_name = "dashboard/projects/categories.html"

    def get(self, request):
        categories = ProjectCategory.objects.annotate(proj_count=Count("project")).order_by("order", "name")
        edit_id = request.GET.get("edit")
        editing_category = None
        if edit_id:
            try:
                editing_category = ProjectCategory.objects.get(pk=int(edit_id))
                form = ProjectCategoryForm(instance=editing_category)
            except (ProjectCategory.DoesNotExist, ValueError):
                form = ProjectCategoryForm()
        else:
            form = ProjectCategoryForm()
        return render(request, self.template_name, {
            "categories": categories,
            "form": form,
            "editing_category": editing_category,
        })

    def post(self, request):
        action = request.POST.get("action")
        if action == "create":
            form = ProjectCategoryForm(request.POST)
            if form.is_valid():
                cat = form.save()
                invalidate_site_cache()
                messages.success(request, f"New project category '{cat.name}' added successfully.")
            else:
                messages.error(request, "Failed to create category. Please check required fields.")
                categories = ProjectCategory.objects.annotate(proj_count=Count("project")).order_by("order", "name")
                return render(request, self.template_name, {"categories": categories, "form": form})
        elif action == "update":
            cat_id = request.POST.get("category_id")
            try:
                cat = get_object_or_404(ProjectCategory, pk=int(cat_id))
                form = ProjectCategoryForm(request.POST, instance=cat)
                if form.is_valid():
                    form.save()
                    invalidate_site_cache()
                    messages.success(request, f"Project category '{cat.name}' updated.")
                else:
                    messages.error(request, "Failed to update category.")
            except (ValueError, TypeError):
                messages.error(request, "Invalid category identifier.")
        elif action == "delete":
            cat_id = request.POST.get("category_id")
            try:
                cat = get_object_or_404(ProjectCategory, pk=int(cat_id))
                name = cat.name
                count = cat.project_set.count()
                cat.delete()
                invalidate_site_cache()
                if count > 0:
                    messages.warning(request, f"Category '{name}' removed. {count} projects are now uncategorized.")
                else:
                    messages.success(request, f"Category '{name}' removed.")
            except (ValueError, TypeError):
                messages.error(request, "Invalid category identifier.")
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
        q = self.request.GET.get("q", "").strip()[:80]
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
        context["q"] = self.request.GET.get("q", "").strip()[:80]
        context["hero"], _ = PageHero.objects.get_or_create(page="news")

        params = self.request.GET.copy()
        if "page" in params:
            params.pop("page")
        context["querystring_without_page"] = params.urlencode()
        return context


class NewsCreateView(StaffRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "dashboard/news/form.html"

    def form_valid(self, form):
        post = form.save()
        messages.success(self.request, f"Article '{post.title}' created successfully.")
        return redirect("dashboard:news_edit", pk=post.pk)


class NewsUpdateView(StaffRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "dashboard/news/form.html"

    def form_valid(self, form):
        if self.request.POST.get("cover_image-clear") and self.object.cover_image:
            safe_delete_file(self.object.cover_image)
            self.object.cover_image = ""
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
        if obj.cover_image:
            safe_delete_file(obj.cover_image)
        messages.success(request, f"Article '{title}' deleted permanently.")
        return super().delete(request, *args, **kwargs)


class NewsCategoryManageView(StaffRequiredMixin, View):
    template_name = "dashboard/news/categories.html"

    def get(self, request):
        categories = NewsCategory.objects.annotate(posts_count=Count("post")).order_by("order", "name")
        edit_id = request.GET.get("edit")
        editing_category = None
        if edit_id:
            try:
                editing_category = NewsCategory.objects.get(pk=int(edit_id))
                form = NewsCategoryForm(instance=editing_category)
            except (NewsCategory.DoesNotExist, ValueError):
                form = NewsCategoryForm()
        else:
            form = NewsCategoryForm()
        return render(request, self.template_name, {
            "categories": categories,
            "form": form,
            "editing_category": editing_category,
        })

    def post(self, request):
        action = request.POST.get("action")
        if action == "create":
            form = NewsCategoryForm(request.POST)
            if form.is_valid():
                cat = form.save()
                messages.success(request, f"News category '{cat.name}' added successfully.")
            else:
                messages.error(request, "Failed to create category. Please check required fields.")
                categories = NewsCategory.objects.annotate(posts_count=Count("post")).order_by("order", "name")
                return render(request, self.template_name, {"categories": categories, "form": form})
        elif action == "update":
            cat_id = request.POST.get("category_id")
            try:
                cat = get_object_or_404(NewsCategory, pk=int(cat_id))
                form = NewsCategoryForm(request.POST, instance=cat)
                if form.is_valid():
                    form.save()
                    messages.success(request, f"News category '{cat.name}' updated.")
                else:
                    messages.error(request, "Failed to update category.")
            except (ValueError, TypeError):
                messages.error(request, "Invalid category identifier.")
        elif action == "delete":
            cat_id = request.POST.get("category_id")
            try:
                cat = get_object_or_404(NewsCategory, pk=int(cat_id))
                name = cat.name
                count = cat.post_set.count()
                cat.delete()
                if count > 0:
                    messages.warning(request, f"Category '{name}' removed. {count} articles are now uncategorized.")
                else:
                    messages.success(request, f"News category '{name}' removed.")
            except (ValueError, TypeError):
                messages.error(request, "Invalid category identifier.")
        return redirect("dashboard:news_categories")


# ==========================================
# 5. CAREERS & RECRUITMENT MANAGEMENT
# ==========================================
class JobOpeningListView(StaffRequiredMixin, ListView):
    model = JobOpening
    template_name = "dashboard/careers/jobs_list.html"
    context_object_name = "jobs"
    paginate_by = 15

    def get_queryset(self):
        qs = JobOpening.objects.select_related("department").annotate(app_count=Count("applications"))
        dept = self.request.GET.get("department", "").strip()
        status_val = self.request.GET.get("status", "").strip()
        if dept:
            qs = qs.filter(department__slug=dept)
        if status_val == "active":
            qs = qs.filter(is_active=True)
        elif status_val == "inactive":
            qs = qs.filter(is_active=False)
        return qs.order_by("order", "-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["departments"] = JobDepartment.objects.all()
        context["selected_department"] = self.request.GET.get("department", "")
        context["selected_status"] = self.request.GET.get("status", "")
        return context


class JobOpeningCreateView(StaffRequiredMixin, CreateView):
    model = JobOpening
    form_class = JobOpeningForm
    template_name = "dashboard/careers/job_form.html"
    success_url = reverse_lazy("dashboard:careers_jobs")

    def form_valid(self, form):
        job = form.save()
        messages.success(self.request, f"Job vacancy '{job.title}' published successfully.")
        return redirect("dashboard:careers_jobs")


class JobOpeningUpdateView(StaffRequiredMixin, UpdateView):
    model = JobOpening
    form_class = JobOpeningForm
    template_name = "dashboard/careers/job_form.html"
    success_url = reverse_lazy("dashboard:careers_jobs")

    def form_valid(self, form):
        job = form.save()
        messages.success(self.request, f"Job vacancy '{job.title}' specifications updated.")
        return redirect("dashboard:careers_jobs")


class JobOpeningDeleteView(StaffRequiredMixin, DeleteView):
    model = JobOpening
    template_name = "dashboard/careers/confirm_delete.html"
    success_url = reverse_lazy("dashboard:careers_jobs")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["applications_count"] = self.object.applications.count()
        return context

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        title = obj.title
        app_count = obj.applications.count()
        for app in obj.applications.all():
            if app.resume:
                safe_delete_file(app.resume)
        messages.success(request, f"Job opening '{title}' and its {app_count} candidate applications were removed.")
        return super().delete(request, *args, **kwargs)


class JobOpeningQuickStatusView(StaffRequiredMixin, View):
    def post(self, request, pk):
        job = get_object_or_404(JobOpening, pk=pk)
        job.is_active = not job.is_active
        job.save()
        state = "Active & Open" if job.is_active else "Closed / Inactive"
        messages.success(request, f"Job opening '{job.title}' is now {state}.")
        return redirect("dashboard:careers_jobs")


class JobDepartmentManageView(StaffRequiredMixin, View):
    template_name = "dashboard/careers/departments.html"

    def get(self, request):
        departments = JobDepartment.objects.annotate(jobs_count=Count("jobs")).order_by("order", "name")
        edit_id = request.GET.get("edit")
        editing_department = None
        if edit_id:
            try:
                editing_department = JobDepartment.objects.get(pk=int(edit_id))
                form = JobDepartmentForm(instance=editing_department)
            except (JobDepartment.DoesNotExist, ValueError):
                form = JobDepartmentForm()
        else:
            form = JobDepartmentForm()
        return render(request, self.template_name, {
            "departments": departments,
            "form": form,
            "editing_department": editing_department,
        })

    def post(self, request):
        action = request.POST.get("action")
        if action == "create":
            form = JobDepartmentForm(request.POST)
            if form.is_valid():
                dept = form.save()
                messages.success(request, f"Job department '{dept.name}' created.")
            else:
                messages.error(request, "Failed to create department. Please check fields.")
                departments = JobDepartment.objects.annotate(jobs_count=Count("jobs")).order_by("order", "name")
                return render(request, self.template_name, {"departments": departments, "form": form})
        elif action == "update":
            dept_id = request.POST.get("department_id")
            try:
                dept = get_object_or_404(JobDepartment, pk=int(dept_id))
                form = JobDepartmentForm(request.POST, instance=dept)
                if form.is_valid():
                    form.save()
                    messages.success(request, f"Department '{dept.name}' updated.")
                else:
                    messages.error(request, "Failed to update department.")
            except (ValueError, TypeError):
                messages.error(request, "Invalid department identifier.")
        elif action == "delete":
            dept_id = request.POST.get("department_id")
            try:
                dept = get_object_or_404(JobDepartment, pk=int(dept_id))
                name = dept.name
                count = dept.jobs.count()
                dept.delete()
                if count > 0:
                    messages.warning(request, f"Department '{name}' removed. {count} job openings have no department assigned.")
                else:
                    messages.success(request, f"Department '{name}' removed.")
            except (ValueError, TypeError):
                messages.error(request, "Invalid department identifier.")
        return redirect("dashboard:careers_departments")


class JobApplicationListView(StaffRequiredMixin, ListView):
    model = JobApplication
    template_name = "dashboard/careers/applications_list.html"
    context_object_name = "applications"
    paginate_by = 20

    def get_queryset(self):
        qs = JobApplication.objects.select_related("job", "job__department").all()
        q = self.request.GET.get("q", "").strip()[:80]
        status_val = self.request.GET.get("status", "").strip()
        job_id = self.request.GET.get("job", "").strip()
        if q:
            qs = qs.filter(Q(full_name__icontains=q) | Q(email__icontains=q) | Q(phone__icontains=q))
        if status_val:
            qs = qs.filter(status=status_val)
        if job_id:
            try:
                qs = qs.filter(job__id=int(job_id))
            except ValueError:
                pass
        return qs.order_by("-submitted_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["jobs"] = JobOpening.objects.all()
        context["selected_status"] = self.request.GET.get("status", "")
        context["selected_job"] = self.request.GET.get("job", "")
        context["q"] = self.request.GET.get("q", "").strip()[:80]

        params = self.request.GET.copy()
        if "page" in params:
            params.pop("page")
        context["querystring_without_page"] = params.urlencode()
        return context


class JobApplicationDetailView(StaffRequiredMixin, View):
    template_name = "dashboard/careers/application_detail.html"

    def get(self, request, pk):
        app = get_object_or_404(JobApplication.objects.select_related("job"), pk=pk)
        form = JobApplicationReviewForm(instance=app)
        default_subject = f"Al Bahaa Recruitment: Application for {app.job.title}"
        default_email_body = (
            f"Dear {app.full_name},\n\n"
            f"Thank you for applying for the position of '{app.job.title}' at Al Bahaa Contracting (S.A.E).\n\n"
            f"Our technical engineering recruitment committee has reviewed your CV and qualifications ...\n\n"
            f"Best regards,\n"
            f"Talent Acquisition & QA/QC Department\n"
            f"Al Bahaa Contracting (S.A.E)\n"
            f"https://albahaacontracting.com"
        )
        return render(request, self.template_name, {
            "application": app,
            "form": form,
            "default_subject": default_subject,
            "default_email_body": default_email_body,
        })

    def post(self, request, pk):
        app = get_object_or_404(JobApplication.objects.select_related("job"), pk=pk)
        action = request.POST.get("action")
        if action == "send_candidate_email":
            raw_subject = request.POST.get("subject", "").strip()
            body = request.POST.get("body", "").strip()
            subject = clean_email_header(raw_subject)
            if not subject or not body:
                messages.error(request, "Subject and email body cannot be blank.")
            else:
                from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "careers@albahaacontracting.com")
                try:
                    send_mail(
                        subject=subject,
                        message=body,
                        from_email=from_email,
                        recipient_list=[app.email],
                        fail_silently=False,
                    )
                    timestamp = timezone.now().strftime("%Y-%m-%d %H:%M")
                    log_entry = f"--- [Candidate Email Sent on {timestamp}] ---\nSubject: {subject}\n\n{body}\n\n"
                    app.internal_notes = log_entry + (app.internal_notes or "")
                    if app.status == "new":
                        app.status = "reviewed"
                    app.save()
                    messages.success(request, f"Official email dispatched to candidate '{app.email}' and logged in review history.")
                except BadHeaderError:
                    messages.error(request, "Invalid characters detected in email header.")
                except Exception as e:
                    messages.error(request, f"Could not send email: {str(e)}")
            return redirect("dashboard:careers_application_detail", pk=app.pk)
        else:
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
            messages.success(request, f"Application for '{app.full_name}' marked as {app.get_status_display()}.")
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": True, "status": app.status, "status_display": app.get_status_display()})
            return redirect("dashboard:careers_applications")
        return JsonResponse({"success": False, "error": "Invalid status value"}, status=400)


class JobApplicationDeleteView(StaffRequiredMixin, View):
    def post(self, request, pk):
        app = get_object_or_404(JobApplication, pk=pk)
        name = app.full_name
        if app.resume:
            safe_delete_file(app.resume)
        app.delete()
        messages.success(request, f"Application from '{name}' and attached resume were permanently deleted.")
        return redirect("dashboard:careers_applications")


class ProtectedResumeDownloadView(StaffRequiredMixin, View):
    """Securely streams applicant resume files to authenticated staff, preventing public unauthorized access."""

    def get(self, request, pk):
        app = get_object_or_404(JobApplication, pk=pk)
        if not app.resume:
            raise Http404("No resume file attached to this application.")
        try:
            return FileResponse(app.resume.open(), as_attachment=False, filename=os.path.basename(app.resume.name))
        except FileNotFoundError:
            raise Http404("Resume file not found on disk storage.")


class ExportApplicationsCsvView(StaffRequiredMixin, View):
    def get(self, request):
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="AlBahaa_Job_Applications.csv"'
        # Write UTF-8 BOM for Microsoft Excel compatibility with Arabic text
        response.write("\ufeff")
        writer = csv.writer(response)
        writer.writerow(["Candidate Name", "Email", "Phone", "Applied Role", "Status", "Date Submitted", "Notes"])
        qs = JobApplication.objects.select_related("job").all().order_by("-submitted_at")
        for app in qs:
            phone_literal = f"'{app.phone}" if app.phone else ""
            writer.writerow([
                sanitize_csv_cell(app.full_name),
                sanitize_csv_cell(app.email),
                phone_literal,
                sanitize_csv_cell(app.job.title if app.job else "N/A"),
                sanitize_csv_cell(app.get_status_display()),
                app.submitted_at.strftime("%Y-%m-%d %H:%M"),
                sanitize_csv_cell(app.internal_notes),
            ])
        return response


# ==========================================
# 6. INQUIRIES & TENDERS MANAGEMENT
# ==========================================
class InquiriesListView(StaffRequiredMixin, ListView):
    model = ContactMessage
    template_name = "dashboard/inquiries/list.html"
    context_object_name = "inquiries"
    paginate_by = 20

    def get_queryset(self):
        qs = ContactMessage.objects.all()
        q = self.request.GET.get("q", "").strip()[:80]
        status_val = self.request.GET.get("status", "").strip()
        inquiry_type = self.request.GET.get("inquiry_type", "").strip()
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(company__icontains=q) | Q(email__icontains=q) | Q(phone__icontains=q) | Q(message__icontains=q))
        if status_val:
            qs = qs.filter(status=status_val)
        if inquiry_type:
            qs = qs.filter(inquiry_type=inquiry_type)
        return qs.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_status"] = self.request.GET.get("status", "")
        context["selected_type"] = self.request.GET.get("inquiry_type", "")
        context["inquiry_types"] = ContactMessage.INQUIRY_CHOICES
        context["q"] = self.request.GET.get("q", "").strip()[:80]
        context["hero"], _ = PageHero.objects.get_or_create(page="contact")

        params = self.request.GET.copy()
        if "page" in params:
            params.pop("page")
        context["querystring_without_page"] = params.urlencode()
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
            f"Should you have any further questions or require immediate engineering assistance, please feel free to reply to this email.\n\n"
            f"Best regards,\n"
            f"Al Bahaa Contracting (S.A.E)\n"
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
            raw_subject = request.POST.get("reply_subject", "").strip()
            reply_body = request.POST.get("reply_body", "").strip()
            reply_subject = clean_email_header(raw_subject)

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
                except BadHeaderError:
                    messages.error(request, "Invalid characters detected in email header.")
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
            if new_status in ("read", "resolved"):
                inquiry.is_read = True
            inquiry.save()
            messages.success(request, f"Inquiry from '{inquiry.name}' updated to {inquiry.get_status_display()}.")
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": True, "status": inquiry.status, "status_display": inquiry.get_status_display()})
            return redirect("dashboard:inquiries_list")
        return JsonResponse({"success": False, "error": "Invalid status"}, status=400)


class InquiryDeleteView(StaffRequiredMixin, View):
    def post(self, request, pk):
        inquiry = get_object_or_404(ContactMessage, pk=pk)
        name = inquiry.name
        inquiry.delete()
        messages.success(request, f"Inquiry from '{name}' deleted permanently.")
        return redirect("dashboard:inquiries_list")


class ExportInquiriesCsvView(StaffRequiredMixin, View):
    def get(self, request):
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="AlBahaa_Contact_Inquiries.csv"'
        response.write("\ufeff")
        writer = csv.writer(response)
        writer.writerow(["Client Name", "Company", "Inquiry Type", "Email", "Phone", "Status", "Date Submitted", "Message Body", "Internal Notes"])
        for msg in ContactMessage.objects.all().order_by("-created_at"):
            phone_literal = f"'{msg.phone}" if msg.phone else ""
            writer.writerow([
                sanitize_csv_cell(msg.name),
                sanitize_csv_cell(msg.company),
                sanitize_csv_cell(msg.get_inquiry_type_display()),
                sanitize_csv_cell(msg.email),
                phone_literal,
                sanitize_csv_cell(msg.get_status_display()),
                msg.created_at.strftime("%Y-%m-%d %H:%M"),
                sanitize_csv_cell(msg.message),
                sanitize_csv_cell(msg.internal_notes),
            ])
        return response


# ==========================================
# 7. PAGE CMS EDITORS (Home, About, Careers)
# ==========================================
class HomeContentManageView(StaffRequiredMixin, View):
    template_name = "dashboard/content/home.html"

    def get(self, request):
        hero_obj, _ = PageHero.objects.get_or_create(page="home")
        home_content = HomeContent.load()
        hero_form = PageHeroForm(instance=hero_obj, prefix="hero")
        content_form = HomeContentForm(instance=home_content, prefix="content")
        slides = SpecializationItem.objects.all().order_by("order", "id")

        edit_slide_id = request.GET.get("edit_slide")
        editing_slide = None
        if edit_slide_id:
            try:
                editing_slide = SpecializationItem.objects.get(pk=int(edit_slide_id))
                slide_form = SpecializationItemForm(instance=editing_slide, prefix="slide")
            except (SpecializationItem.DoesNotExist, ValueError):
                slide_form = SpecializationItemForm(prefix="slide")
        else:
            slide_form = SpecializationItemForm(prefix="slide")

        return render(request, self.template_name, {
            "hero_form": hero_form,
            "content_form": content_form,
            "slide_form": slide_form,
            "slides": slides,
            "hero_obj": hero_obj,
            "home_content": home_content,
            "editing_slide": editing_slide,
        })

    def post(self, request):
        action = request.POST.get("action")
        hero_obj, _ = PageHero.objects.get_or_create(page="home")
        home_content = HomeContent.load()

        if action == "save_hero":
            if request.POST.get("hero-hero_image-clear") and hero_obj.hero_image:
                safe_delete_file(hero_obj.hero_image)
                hero_obj.hero_image = ""
            hero_form = PageHeroForm(request.POST, request.FILES, instance=hero_obj, prefix="hero")
            if hero_form.is_valid():
                hero_form.save()
                invalidate_site_cache()
                messages.success(request, "Home Page Hero Banner updated successfully.")
            else:
                messages.error(request, "Failed to save Hero Banner. Please check the fields.")
        elif action == "save_content":
            if request.POST.get("content-blueprints_image-clear") and home_content.blueprints_image:
                safe_delete_file(home_content.blueprints_image)
                home_content.blueprints_image = ""
            content_form = HomeContentForm(request.POST, request.FILES, instance=home_content, prefix="content")
            if content_form.is_valid():
                content_form.save()
                invalidate_site_cache()
                messages.success(request, "Blueprints & Specialization section narrative updated.")
            else:
                messages.error(request, "Failed to save Blueprints section.")
        elif action == "create_slide":
            slide_form = SpecializationItemForm(request.POST, prefix="slide")
            if slide_form.is_valid():
                slide = slide_form.save()
                invalidate_site_cache()
                messages.success(request, f"Specialization slide '{slide.discipline}' added successfully.")
            else:
                messages.error(request, "Failed to create slide. Please check required fields.")
        elif action == "update_slide":
            slide_id = request.POST.get("slide_id")
            try:
                slide = get_object_or_404(SpecializationItem, pk=int(slide_id))
                slide_form = SpecializationItemForm(request.POST, instance=slide, prefix="slide")
                if slide_form.is_valid():
                    slide_form.save()
                    invalidate_site_cache()
                    messages.success(request, f"Specialization slide '{slide.discipline}' updated.")
                else:
                    messages.error(request, "Failed to update slide.")
            except (ValueError, TypeError):
                messages.error(request, "Invalid slide identifier.")
        elif action == "delete_slide":
            slide_id = request.POST.get("slide_id")
            try:
                slide = get_object_or_404(SpecializationItem, pk=int(slide_id))
                name = slide.discipline
                slide.delete()
                invalidate_site_cache()
                messages.success(request, f"Slide '{name}' removed.")
            except (ValueError, TypeError):
                messages.error(request, "Invalid slide identifier.")

        return redirect("dashboard:content_home")


class AboutPageManageView(StaffRequiredMixin, View):
    template_name = "dashboard/content/about.html"

    def get(self, request):
        active_tab = request.GET.get("tab", "narrative")
        hero_obj, _ = PageHero.objects.get_or_create(page="about")
        about_content = AboutContent.load()

        hero_form = PageHeroForm(instance=hero_obj, prefix="hero")
        about_form = AboutContentForm(instance=about_content, prefix="about")

        stats = AboutStatistic.objects.all().order_by("order", "id")
        pillars = CompanyPillar.objects.all().order_by("order", "id")
        services = ServiceItem.objects.all().order_by("order", "title")

        # Edit modes for sub-items
        edit_stat_id = request.GET.get("edit_stat")
        editing_stat = None
        if edit_stat_id:
            try:
                editing_stat = AboutStatistic.objects.get(pk=int(edit_stat_id))
                stat_form = AboutStatisticForm(instance=editing_stat, prefix="stat")
            except (AboutStatistic.DoesNotExist, ValueError):
                stat_form = AboutStatisticForm(prefix="stat")
        else:
            stat_form = AboutStatisticForm(prefix="stat")

        edit_pillar_id = request.GET.get("edit_pillar")
        editing_pillar = None
        if edit_pillar_id:
            try:
                editing_pillar = CompanyPillar.objects.get(pk=int(edit_pillar_id))
                pillar_form = CompanyPillarForm(instance=editing_pillar, prefix="pillar")
            except (CompanyPillar.DoesNotExist, ValueError):
                pillar_form = CompanyPillarForm(prefix="pillar")
        else:
            pillar_form = CompanyPillarForm(prefix="pillar")

        edit_service_id = request.GET.get("edit_service")
        editing_service = None
        if edit_service_id:
            try:
                editing_service = ServiceItem.objects.get(pk=int(edit_service_id))
                service_form = ServiceItemForm(instance=editing_service, prefix="service")
            except (ServiceItem.DoesNotExist, ValueError):
                service_form = ServiceItemForm(prefix="service")
        else:
            service_form = ServiceItemForm(prefix="service")

        return render(request, self.template_name, {
            "active_tab": active_tab,
            "hero_obj": hero_obj,
            "about_content": about_content,
            "hero_form": hero_form,
            "about_form": about_form,
            "stats": stats,
            "pillars": pillars,
            "services": services,
            "stat_form": stat_form,
            "pillar_form": pillar_form,
            "service_form": service_form,
            "editing_stat": editing_stat,
            "editing_pillar": editing_pillar,
            "editing_service": editing_service,
        })

    def post(self, request):
        action = request.POST.get("action")
        active_tab = request.POST.get("active_tab", "narrative")
        hero_obj, _ = PageHero.objects.get_or_create(page="about")
        about_content = AboutContent.load()

        if action == "save_hero":
            active_tab = "narrative"
            if request.POST.get("hero-hero_image-clear") and hero_obj.hero_image:
                safe_delete_file(hero_obj.hero_image)
                hero_obj.hero_image = ""
            hero_form = PageHeroForm(request.POST, request.FILES, instance=hero_obj, prefix="hero")
            if hero_form.is_valid():
                hero_form.save()
                invalidate_site_cache()
                messages.success(request, "About Page Hero Banner updated.")
            else:
                messages.error(request, "Failed to save Hero Banner.")
        elif action == "save_narrative":
            active_tab = "narrative"
            about_form = AboutContentForm(request.POST, instance=about_content, prefix="about")
            if about_form.is_valid():
                about_form.save()
                invalidate_site_cache()
                messages.success(request, "About page narrative and Call-to-Action sections updated.")
            else:
                messages.error(request, "Failed to save About page narrative.")
        elif action == "create_stat":
            active_tab = "stats"
            stat_form = AboutStatisticForm(request.POST, prefix="stat")
            if stat_form.is_valid():
                stat = stat_form.save()
                invalidate_site_cache()
                messages.success(request, f"Credential '{stat.value}' added successfully.")
            else:
                messages.error(request, "Failed to add credential.")
        elif action == "update_stat":
            active_tab = "stats"
            stat_id = request.POST.get("stat_id")
            try:
                stat = get_object_or_404(AboutStatistic, pk=int(stat_id))
                stat_form = AboutStatisticForm(request.POST, instance=stat, prefix="stat")
                if stat_form.is_valid():
                    stat_form.save()
                    invalidate_site_cache()
                    messages.success(request, f"Credential '{stat.value}' updated.")
            except (ValueError, TypeError):
                messages.error(request, "Invalid stat ID.")
        elif action == "delete_stat":
            active_tab = "stats"
            stat_id = request.POST.get("stat_id")
            try:
                stat = get_object_or_404(AboutStatistic, pk=int(stat_id))
                stat.delete()
                invalidate_site_cache()
                messages.success(request, "Credential removed.")
            except (ValueError, TypeError):
                pass
        elif action == "create_pillar":
            active_tab = "pillars"
            pillar_form = CompanyPillarForm(request.POST, prefix="pillar")
            if pillar_form.is_valid():
                p = pillar_form.save()
                invalidate_site_cache()
                messages.success(request, f"Pillar '{p.title}' added.")
            else:
                messages.error(request, "Failed to add pillar.")
        elif action == "update_pillar":
            active_tab = "pillars"
            pillar_id = request.POST.get("pillar_id")
            try:
                p = get_object_or_404(CompanyPillar, pk=int(pillar_id))
                pillar_form = CompanyPillarForm(request.POST, instance=p, prefix="pillar")
                if pillar_form.is_valid():
                    pillar_form.save()
                    invalidate_site_cache()
                    messages.success(request, f"Pillar '{p.title}' updated.")
            except (ValueError, TypeError):
                pass
        elif action == "delete_pillar":
            active_tab = "pillars"
            pillar_id = request.POST.get("pillar_id")
            try:
                p = get_object_or_404(CompanyPillar, pk=int(pillar_id))
                p.delete()
                invalidate_site_cache()
                messages.success(request, "Pillar removed.")
            except (ValueError, TypeError):
                pass
        elif action == "create_service":
            active_tab = "services"
            service_form = ServiceItemForm(request.POST, prefix="service")
            if service_form.is_valid():
                s = service_form.save()
                invalidate_site_cache()
                messages.success(request, f"Service '{s.title}' added.")
            else:
                messages.error(request, "Failed to add service.")
        elif action == "update_service":
            active_tab = "services"
            service_id = request.POST.get("service_id")
            try:
                s = get_object_or_404(ServiceItem, pk=int(service_id))
                service_form = ServiceItemForm(request.POST, instance=s, prefix="service")
                if service_form.is_valid():
                    service_form.save()
                    invalidate_site_cache()
                    messages.success(request, f"Service '{s.title}' updated.")
            except (ValueError, TypeError):
                pass
        elif action == "delete_service":
            active_tab = "services"
            service_id = request.POST.get("service_id")
            try:
                s = get_object_or_404(ServiceItem, pk=int(service_id))
                s.delete()
                invalidate_site_cache()
                messages.success(request, "Service removed.")
            except (ValueError, TypeError):
                pass

        return redirect(f"{reverse('dashboard:content_about')}?tab={active_tab}")


class CareersPageManageView(StaffRequiredMixin, View):
    template_name = "dashboard/content/careers.html"

    def get(self, request):
        hero_obj, _ = PageHero.objects.get_or_create(page="careers")
        career_settings = CareerSettings.load()
        hero_form = PageHeroForm(instance=hero_obj, prefix="hero")
        settings_form = CareerSettingsForm(instance=career_settings, prefix="settings")
        pillars = CareerPillar.objects.all().order_by("order", "id")

        edit_pillar_id = request.GET.get("edit_pillar")
        editing_pillar = None
        if edit_pillar_id:
            try:
                editing_pillar = CareerPillar.objects.get(pk=int(edit_pillar_id))
                pillar_form = CareerPillarForm(instance=editing_pillar, prefix="pillar")
            except (CareerPillar.DoesNotExist, ValueError):
                pillar_form = CareerPillarForm(prefix="pillar")
        else:
            pillar_form = CareerPillarForm(prefix="pillar")

        return render(request, self.template_name, {
            "hero_obj": hero_obj,
            "career_settings": career_settings,
            "hero_form": hero_form,
            "settings_form": settings_form,
            "pillars": pillars,
            "pillar_form": pillar_form,
            "editing_pillar": editing_pillar,
        })

    def post(self, request):
        action = request.POST.get("action")
        hero_obj, _ = PageHero.objects.get_or_create(page="careers")
        career_settings = CareerSettings.load()

        if action == "save_hero":
            if request.POST.get("hero-hero_image-clear") and hero_obj.hero_image:
                safe_delete_file(hero_obj.hero_image)
                hero_obj.hero_image = ""
            hero_form = PageHeroForm(request.POST, request.FILES, instance=hero_obj, prefix="hero")
            if hero_form.is_valid():
                hero_form.save()
                invalidate_site_cache()
                messages.success(request, "Careers Page Hero Banner updated.")
            else:
                messages.error(request, "Failed to save Hero Banner.")
        elif action == "save_spontaneous":
            settings_form = CareerSettingsForm(request.POST, instance=career_settings, prefix="settings")
            if settings_form.is_valid():
                settings_form.save()
                invalidate_site_cache()
                messages.success(request, "Spontaneous Application banner updated.")
            else:
                messages.error(request, "Failed to save spontaneous application banner.")
        elif action == "create_pillar":
            pillar_form = CareerPillarForm(request.POST, prefix="pillar")
            if pillar_form.is_valid():
                p = pillar_form.save()
                invalidate_site_cache()
                messages.success(request, f"Culture pillar '{p.title}' added.")
            else:
                messages.error(request, "Failed to create pillar.")
        elif action == "update_pillar":
            pillar_id = request.POST.get("pillar_id")
            try:
                p = get_object_or_404(CareerPillar, pk=int(pillar_id))
                pillar_form = CareerPillarForm(request.POST, instance=p, prefix="pillar")
                if pillar_form.is_valid():
                    pillar_form.save()
                    invalidate_site_cache()
                    messages.success(request, f"Culture pillar '{p.title}' updated.")
            except (ValueError, TypeError):
                pass
        elif action == "delete_pillar":
            pillar_id = request.POST.get("pillar_id")
            try:
                p = get_object_or_404(CareerPillar, pk=int(pillar_id))
                p.delete()
                invalidate_site_cache()
                messages.success(request, "Culture pillar removed.")
            except (ValueError, TypeError):
                pass

        return redirect("dashboard:content_careers")


# ==========================================
# 8. PARTNERS & TESTIMONIALS (Social Proof)
# ==========================================
class PartnersManageView(StaffRequiredMixin, View):
    template_name = "dashboard/partners/index.html"

    def get(self, request):
        active_tab = request.GET.get("tab", "logos")
        logos = ClientLogo.objects.all().order_by("order", "name")
        testimonials = Testimonial.objects.all().order_by("order", "client_name")

        edit_logo_id = request.GET.get("edit_logo")
        editing_logo = None
        if edit_logo_id:
            try:
                editing_logo = ClientLogo.objects.get(pk=int(edit_logo_id))
                logo_form = ClientLogoForm(instance=editing_logo, prefix="logo")
            except (ClientLogo.DoesNotExist, ValueError):
                logo_form = ClientLogoForm(prefix="logo")
        else:
            logo_form = ClientLogoForm(prefix="logo")

        edit_testimonial_id = request.GET.get("edit_testimonial")
        editing_testimonial = None
        if edit_testimonial_id:
            try:
                editing_testimonial = Testimonial.objects.get(pk=int(edit_testimonial_id))
                testimonial_form = TestimonialForm(instance=editing_testimonial, prefix="testim")
            except (Testimonial.DoesNotExist, ValueError):
                testimonial_form = TestimonialForm(prefix="testim")
        else:
            testimonial_form = TestimonialForm(prefix="testim")

        return render(request, self.template_name, {
            "active_tab": active_tab,
            "logos": logos,
            "testimonials": testimonials,
            "logo_form": logo_form,
            "testimonial_form": testimonial_form,
            "editing_logo": editing_logo,
            "editing_testimonial": editing_testimonial,
        })

    def post(self, request):
        action = request.POST.get("action")
        active_tab = request.POST.get("active_tab", "logos")

        if action == "create_logo":
            active_tab = "logos"
            form = ClientLogoForm(request.POST, request.FILES, prefix="logo")
            if form.is_valid():
                logo = form.save()
                messages.success(request, f"Partner logo '{logo.name}' added.")
            else:
                messages.error(request, "Failed to add partner logo.")
        elif action == "update_logo":
            active_tab = "logos"
            logo_id = request.POST.get("logo_id")
            try:
                logo = get_object_or_404(ClientLogo, pk=int(logo_id))
                if request.POST.get("logo-logo_image-clear") and logo.logo_image:
                    safe_delete_file(logo.logo_image)
                    logo.logo_image = ""
                form = ClientLogoForm(request.POST, request.FILES, instance=logo, prefix="logo")
                if form.is_valid():
                    form.save()
                    messages.success(request, f"Partner logo '{logo.name}' updated.")
            except (ValueError, TypeError):
                pass
        elif action == "delete_logo":
            active_tab = "logos"
            logo_id = request.POST.get("logo_id")
            try:
                logo = get_object_or_404(ClientLogo, pk=int(logo_id))
                name = logo.name
                if logo.logo_image:
                    safe_delete_file(logo.logo_image)
                logo.delete()
                messages.success(request, f"Partner logo '{name}' removed.")
            except (ValueError, TypeError):
                pass
        elif action == "create_testimonial":
            active_tab = "testimonials"
            form = TestimonialForm(request.POST, request.FILES, prefix="testim")
            if form.is_valid():
                t = form.save()
                messages.success(request, f"Testimonial from '{t.client_name}' added.")
            else:
                messages.error(request, "Failed to add testimonial.")
        elif action == "update_testimonial":
            active_tab = "testimonials"
            t_id = request.POST.get("testimonial_id")
            try:
                t = get_object_or_404(Testimonial, pk=int(t_id))
                if request.POST.get("testim-avatar-clear") and t.avatar:
                    safe_delete_file(t.avatar)
                    t.avatar = ""
                form = TestimonialForm(request.POST, request.FILES, instance=t, prefix="testim")
                if form.is_valid():
                    form.save()
                    messages.success(request, f"Testimonial from '{t.client_name}' updated.")
            except (ValueError, TypeError):
                pass
        elif action == "delete_testimonial":
            active_tab = "testimonials"
            t_id = request.POST.get("testimonial_id")
            try:
                t = get_object_or_404(Testimonial, pk=int(t_id))
                name = t.client_name
                if t.avatar:
                    safe_delete_file(t.avatar)
                t.delete()
                messages.success(request, f"Testimonial from '{name}' removed.")
            except (ValueError, TypeError):
                pass

        return redirect(f"{reverse('dashboard:partners_manage')}?tab={active_tab}")


# ==========================================
# 9. SITE SETTINGS & HEROES
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
            safe_delete_file(settings_obj.header_logo)
            settings_obj.header_logo = ""
        if request.POST.get("footer_logo-clear") and settings_obj.footer_logo:
            safe_delete_file(settings_obj.footer_logo)
            settings_obj.footer_logo = ""
        if request.POST.get("favicon-clear") and settings_obj.favicon:
            safe_delete_file(settings_obj.favicon)
            settings_obj.favicon = ""
        form = SiteSettingsForm(request.POST, request.FILES, instance=settings_obj)
        if form.is_valid():
            form.save()
            invalidate_site_cache()
            messages.success(request, "Corporate site settings and identity parameters updated.")
            return redirect("dashboard:settings_general")
        return render(request, self.template_name, {"form": form, "settings": settings_obj})


class PageHeroEditView(StaffRequiredMixin, View):
    def post(self, request, pk):
        hero = get_object_or_404(PageHero, pk=pk)
        page_name = hero.page
        if request.POST.get("hero_image-clear") and hero.hero_image:
            safe_delete_file(hero.hero_image)
            hero.hero_image = ""
        form = PageHeroForm(request.POST, request.FILES, instance=hero)
        if form.is_valid():
            form.save()
            invalidate_site_cache()
            messages.success(request, f"{hero.get_page_display()} Hero Banner updated.")
        else:
            messages.error(request, f"Failed to update {hero.get_page_display()} banner.")

        # Redirect back to appropriate in-context page editor
        target_map = {
            "home": "dashboard:content_home",
            "about": "dashboard:content_about",
            "careers": "dashboard:content_careers",
            "projects": "dashboard:projects_list",
            "news": "dashboard:news_list",
            "contact": "dashboard:inquiries_list",
        }
        target_route = target_map.get(page_name, "dashboard:overview")
        return redirect(target_route)


# ==========================================
# 10. LEADERSHIP & TEAM
# ==========================================
class TeamManageView(StaffRequiredMixin, View):
    template_name = "dashboard/team/list.html"

    def get(self, request):
        members = TeamMember.objects.all().order_by("order", "name")
        edit_id = request.GET.get("edit")
        editing_member = None
        if edit_id:
            try:
                editing_member = TeamMember.objects.get(pk=int(edit_id))
                form = TeamMemberForm(instance=editing_member)
            except (TeamMember.DoesNotExist, ValueError):
                form = TeamMemberForm()
        else:
            form = TeamMemberForm()
        return render(request, self.template_name, {
            "members": members,
            "form": form,
            "editing_member": editing_member,
        })

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
            try:
                member = get_object_or_404(TeamMember, pk=int(member_id))
                if request.POST.get("photo-clear") and member.photo:
                    safe_delete_file(member.photo)
                    member.photo = ""
                form = TeamMemberForm(request.POST, request.FILES, instance=member)
                if form.is_valid():
                    form.save()
                    messages.success(request, f"Leadership profile '{member.name}' updated.")
                else:
                    messages.error(request, "Failed to update member. Please check fields.")
            except (ValueError, TypeError):
                messages.error(request, "Invalid member identifier.")
        elif action == "delete":
            member_id = request.POST.get("member_id")
            try:
                member = get_object_or_404(TeamMember, pk=int(member_id))
                name = member.name
                if member.photo:
                    safe_delete_file(member.photo)
                member.delete()
                messages.success(request, f"Team member '{name}' removed.")
            except (ValueError, TypeError):
                messages.error(request, "Invalid member identifier.")
        return redirect("dashboard:team_manage")


# ==========================================
# 11. STAFF & USER MANAGEMENT (Superuser Only)
# ==========================================
class StaffUserListView(SuperuserRequiredMixin, ListView):
    model = User
    template_name = "dashboard/users/list.html"
    context_object_name = "staff_users"

    def get_queryset(self):
        return User.objects.filter(is_staff=True).order_by("-is_superuser", "username")


class StaffUserCreateView(SuperuserRequiredMixin, CreateView):
    model = User
    form_class = StaffUserCreateForm
    template_name = "dashboard/users/form.html"
    success_url = reverse_lazy("dashboard:users_list")

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, f"Staff account for '{user.username}' created successfully.")
        return redirect("dashboard:users_list")


class StaffUserUpdateView(SuperuserRequiredMixin, UpdateView):
    model = User
    form_class = StaffUserUpdateForm
    template_name = "dashboard/users/form.html"
    success_url = reverse_lazy("dashboard:users_list")

    def form_valid(self, form):
        # Anti Self-Lockout Defense
        if self.object.pk == self.request.user.pk:
            if not form.cleaned_data.get("is_active"):
                messages.error(self.request, "Security constraint: You cannot deactivate your own currently active account.")
                return self.form_invalid(form)
            if not form.cleaned_data.get("is_superuser"):
                messages.error(self.request, "Security constraint: You cannot revoke superuser permissions from your own account.")
                return self.form_invalid(form)
        user = form.save()
        messages.success(self.request, f"Account settings for '{user.username}' updated.")
        return redirect("dashboard:users_list")


class StaffUserToggleStatusView(SuperuserRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user.pk == request.user.pk:
            messages.error(request, "Security constraint: You cannot deactivate your own active session account.")
            return redirect("dashboard:users_list")
        user.is_active = not user.is_active
        user.save()
        state = "Activated" if user.is_active else "Deactivated"
        messages.success(request, f"Staff account for '{user.username}' is now {state}.")
        return redirect("dashboard:users_list")
