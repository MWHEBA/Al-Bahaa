import re
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.text import slugify

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

User = get_user_model()

MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024   # 5 MB
MAX_DOC_SIZE_BYTES = 10 * 1024 * 1024    # 10 MB


def validate_file_size(file_obj, max_size, label="file"):
    if file_obj and hasattr(file_obj, "size") and file_obj.size > max_size:
        max_mb = max_size // (1024 * 1024)
        raise ValidationError(f"The selected {label} exceeds the maximum allowed size of {max_mb}MB.")


# ==========================================
# 1. AUTH & PROFILE FORMS
# ==========================================
class ExecutiveProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "dash-input", "placeholder": "First Name", "dir": "auto"}),
            "last_name": forms.TextInput(attrs={"class": "dash-input", "placeholder": "Last Name", "dir": "auto"}),
            "email": forms.EmailInput(attrs={"class": "dash-input", "placeholder": "corporate@albahaa.com", "dir": "ltr"}),
        }


class StaffUserCreateForm(UserCreationForm):
    first_name = forms.CharField(max_length=60, required=True, widget=forms.TextInput(attrs={"class": "dash-input", "placeholder": "First Name", "dir": "auto"}))
    last_name = forms.CharField(max_length=60, required=True, widget=forms.TextInput(attrs={"class": "dash-input", "placeholder": "Last Name", "dir": "auto"}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "dash-input", "placeholder": "user@albahaacontracting.com", "dir": "ltr"}))
    is_staff = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={"class": "dash-checkbox"}))
    is_superuser = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={"class": "dash-checkbox"}))

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "is_staff", "is_superuser"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "dash-input", "placeholder": "Username (e.g. ahmed.bahaa)", "dir": "ltr"}),
        }


class StaffUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "is_staff", "is_superuser", "is_active"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "dash-input", "placeholder": "First Name", "dir": "auto"}),
            "last_name": forms.TextInput(attrs={"class": "dash-input", "placeholder": "Last Name", "dir": "auto"}),
            "email": forms.EmailInput(attrs={"class": "dash-input", "placeholder": "user@albahaacontracting.com", "dir": "ltr"}),
            "is_staff": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
            "is_superuser": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
            "is_active": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
        }


class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


# ==========================================
# 2. PROJECTS FORMS
# ==========================================
class ProjectForm(forms.ModelForm):
    gallery_images = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={"class": "dash-file-input", "accept": "image/*", "multiple": True}),
        help_text="Select up to 15 high-resolution site execution photos for the project gallery (Max 5MB each).",
    )

    class Meta:
        model = Project
        fields = [
            "title",
            "slug",
            "category",
            "status",
            "location",
            "client_name",
            "architect_consultant",
            "scope_of_work",
            "built_up_area",
            "date",
            "cover_image",
            "short_description",
            "full_description",
            "engineering_highlights",
            "sustainability",
            "is_featured",
            "order",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. Eastern Al-Ma'abda Sewerage System", "dir": "auto"}),
            "slug": forms.TextInput(attrs={"class": "dash-input", "placeholder": "auto-generated-if-left-empty", "dir": "ltr"}),
            "category": forms.Select(attrs={"class": "dash-select"}),
            "status": forms.Select(attrs={"class": "dash-select"}),
            "location": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. Assiut, Egypt", "dir": "auto"}),
            "client_name": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. NOPWASD", "dir": "auto"}),
            "architect_consultant": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. Dar Al-Handasah", "dir": "auto"}),
            "scope_of_work": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. Turnkey Infrastructure Contracting", "dir": "auto"}),
            "built_up_area": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. 350,000 LM Network Scale", "dir": "auto"}),
            "date": forms.DateInput(attrs={"class": "dash-input", "type": "date", "dir": "ltr"}),
            "cover_image": forms.FileInput(attrs={"class": "dash-file-input", "accept": "image/*", "id": "id_cover_image"}),
            "short_description": forms.Textarea(attrs={"class": "dash-textarea", "rows": 3, "placeholder": "Brief 1-2 sentence executive summary", "dir": "auto"}),
            "full_description": forms.Textarea(attrs={"class": "dash-textarea", "rows": 6, "placeholder": "Detailed multi-paragraph project description...", "dir": "auto"}),
            "engineering_highlights": forms.Textarea(attrs={"class": "dash-textarea", "rows": 5, "placeholder": "One engineering highlight per line...", "dir": "auto"}),
            "sustainability": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. EDGE Green Building compliant", "dir": "auto"}),
            "is_featured": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
            "order": forms.NumberInput(attrs={"class": "dash-input", "style": "width: 120px;", "dir": "ltr"}),
        }

    def clean_cover_image(self):
        img = self.cleaned_data.get("cover_image")
        validate_file_size(img, MAX_IMAGE_SIZE_BYTES, "cover image")
        return img

    def clean_gallery_images(self):
        files = self.cleaned_data.get("gallery_images")
        if files:
            if len(files) > 15:
                raise ValidationError("You can upload a maximum of 15 gallery images in a single batch.")
            for f in files:
                validate_file_size(f, MAX_IMAGE_SIZE_BYTES, "gallery image")
        return files

    def clean_slug(self):
        slug = self.cleaned_data.get("slug", "").strip()
        title = self.cleaned_data.get("title", "")
        if not slug and title:
            base_slug = slugify(title) or "project"
            slug = base_slug
            counter = 1
            pk = self.instance.pk
            while Project.objects.filter(slug=slug).exclude(pk=pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
        return slug


class ProjectCategoryForm(forms.ModelForm):
    class Meta:
        model = ProjectCategory
        fields = ["name", "slug", "order"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. Water & Sewage Infrastructure", "dir": "auto"}),
            "slug": forms.TextInput(attrs={"class": "dash-input", "placeholder": "auto-generated", "dir": "ltr"}),
            "order": forms.NumberInput(attrs={"class": "dash-input", "style": "width: 120px;", "dir": "ltr"}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get("slug", "").strip()
        name = self.cleaned_data.get("name", "")
        if not slug and name:
            base_slug = slugify(name) or "category"
            slug = base_slug
            counter = 1
            pk = self.instance.pk
            while ProjectCategory.objects.filter(slug=slug).exclude(pk=pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
        return slug


# ==========================================
# 3. NEWS & ARTICLES FORMS
# ==========================================
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "slug",
            "category",
            "author",
            "cover_image",
            "excerpt",
            "content",
            "published_at",
            "is_published",
            "order",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "dash-input", "placeholder": "Article Title", "dir": "auto"}),
            "slug": forms.TextInput(attrs={"class": "dash-input", "placeholder": "auto-generated-if-empty", "dir": "ltr"}),
            "category": forms.Select(attrs={"class": "dash-select"}),
            "author": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. Technical Office & QA/QC", "dir": "auto"}),
            "cover_image": forms.FileInput(attrs={"class": "dash-file-input", "accept": "image/*", "id": "id_cover_image"}),
            "excerpt": forms.Textarea(attrs={"class": "dash-textarea", "rows": 3, "placeholder": "Brief summary kicker", "dir": "auto"}),
            "content": forms.Textarea(attrs={"class": "dash-textarea", "rows": 8, "placeholder": "Full article content...", "dir": "auto"}),
            "published_at": forms.DateTimeInput(format="%Y-%m-%dT%H:%M", attrs={"class": "dash-input", "type": "datetime-local", "dir": "ltr"}),
            "is_published": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
            "order": forms.NumberInput(attrs={"class": "dash-input", "style": "width: 120px;", "dir": "ltr"}),
        }

    def clean_cover_image(self):
        img = self.cleaned_data.get("cover_image")
        validate_file_size(img, MAX_IMAGE_SIZE_BYTES, "cover image")
        return img

    def clean_slug(self):
        slug = self.cleaned_data.get("slug", "").strip()
        title = self.cleaned_data.get("title", "")
        if not slug and title:
            base_slug = slugify(title) or "article"
            slug = base_slug
            counter = 1
            pk = self.instance.pk
            while Post.objects.filter(slug=slug).exclude(pk=pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
        return slug


class NewsCategoryForm(forms.ModelForm):
    class Meta:
        model = NewsCategory
        fields = ["name", "slug", "order"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. Infrastructure Updates", "dir": "auto"}),
            "slug": forms.TextInput(attrs={"class": "dash-input", "placeholder": "auto-generated", "dir": "ltr"}),
            "order": forms.NumberInput(attrs={"class": "dash-input", "style": "width: 120px;", "dir": "ltr"}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get("slug", "").strip()
        name = self.cleaned_data.get("name", "")
        if not slug and name:
            base_slug = slugify(name) or "category"
            slug = base_slug
            counter = 1
            pk = self.instance.pk
            while NewsCategory.objects.filter(slug=slug).exclude(pk=pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
        return slug


# ==========================================
# 4. RECRUITMENT & CAREERS FORMS
# ==========================================
class JobOpeningForm(forms.ModelForm):
    class Meta:
        model = JobOpening
        fields = [
            "title",
            "slug",
            "department",
            "location",
            "job_type",
            "experience",
            "summary",
            "responsibilities",
            "requirements",
            "benefits",
            "is_active",
            "order",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. Senior Infrastructure Project Manager", "dir": "auto"}),
            "slug": forms.TextInput(attrs={"class": "dash-input", "placeholder": "auto-generated-if-empty", "dir": "ltr"}),
            "department": forms.Select(attrs={"class": "dash-select"}),
            "location": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. New Cairo, Egypt", "dir": "auto"}),
            "job_type": forms.Select(attrs={"class": "dash-select"}),
            "experience": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. 8-12 Years", "dir": "auto"}),
            "summary": forms.Textarea(attrs={"class": "dash-textarea", "rows": 3, "placeholder": "Executive role summary", "dir": "auto"}),
            "responsibilities": forms.Textarea(attrs={"class": "dash-textarea", "rows": 5, "placeholder": "One bullet per line...", "dir": "auto"}),
            "requirements": forms.Textarea(attrs={"class": "dash-textarea", "rows": 5, "placeholder": "One requirement per line...", "dir": "auto"}),
            "benefits": forms.Textarea(attrs={"class": "dash-textarea", "rows": 4, "placeholder": "One benefit per line...", "dir": "auto"}),
            "is_active": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
            "order": forms.NumberInput(attrs={"class": "dash-input", "style": "width: 120px;", "dir": "ltr"}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get("slug", "").strip()
        title = self.cleaned_data.get("title", "")
        if not slug and title:
            base_slug = slugify(title) or "job"
            slug = base_slug
            counter = 1
            pk = self.instance.pk
            while JobOpening.objects.filter(slug=slug).exclude(pk=pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
        return slug


class JobDepartmentForm(forms.ModelForm):
    class Meta:
        model = JobDepartment
        fields = ["name", "slug", "order"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. Site Engineering", "dir": "auto"}),
            "slug": forms.TextInput(attrs={"class": "dash-input", "placeholder": "auto-generated", "dir": "ltr"}),
            "order": forms.NumberInput(attrs={"class": "dash-input", "style": "width: 120px;", "dir": "ltr"}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get("slug", "").strip()
        name = self.cleaned_data.get("name", "")
        if not slug and name:
            base_slug = slugify(name) or "dept"
            slug = base_slug
            counter = 1
            pk = self.instance.pk
            while JobDepartment.objects.filter(slug=slug).exclude(pk=pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
        return slug


class JobApplicationReviewForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ["status", "internal_notes"]
        widgets = {
            "status": forms.Select(attrs={"class": "dash-select"}),
            "internal_notes": forms.Textarea(attrs={"class": "dash-textarea", "rows": 4, "placeholder": "Private HR internal notes and candidate evaluation...", "dir": "auto"}),
        }


# ==========================================
# 5. INQUIRIES FORMS
# ==========================================
class ContactMessageReviewForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["status", "internal_notes"]
        widgets = {
            "status": forms.Select(attrs={"class": "dash-select"}),
            "internal_notes": forms.Textarea(attrs={"class": "dash-textarea", "rows": 4, "placeholder": "Internal reply status, assigned engineer, or follow-up notes...", "dir": "auto"}),
        }


# ==========================================
# 6. SITE SETTINGS & HEROES FORMS
# ==========================================
class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            # Identity
            "company_name",
            "header_logo",
            "footer_logo",
            "favicon",
            "copyright_text",
            "footer_quote",
            "footer_quote_author",
            # Contacts
            "phone_main",
            "phone_tenders",
            "phone_sale",
            "phone_support",
            "email_general",
            "email_tenders",
            "email_careers",
            "email_sale",
            "email_support",
            # Address & Hours
            "address_line1",
            "address_line2",
            "address",
            "map_embed_url",
            "map_directions_url",
            "working_hours_weekdays",
            "working_hours_emergencies",
            # Social Channels
            "linkedin_url",
            "facebook_url",
            "instagram_url",
            "youtube_url",
        ]
        widgets = {
            "company_name": forms.TextInput(attrs={"class": "dash-input", "dir": "auto"}),
            "header_logo": forms.FileInput(attrs={"class": "dash-file-input", "accept": "image/*", "id": "id_header_logo"}),
            "footer_logo": forms.FileInput(attrs={"class": "dash-file-input", "accept": "image/*", "id": "id_footer_logo"}),
            "favicon": forms.FileInput(attrs={"class": "dash-file-input", "accept": "image/*,.ico,.svg", "id": "id_favicon"}),
            "copyright_text": forms.TextInput(attrs={"class": "dash-input", "dir": "auto"}),
            "footer_quote": forms.Textarea(attrs={"class": "dash-textarea", "rows": 3, "dir": "auto"}),
            "footer_quote_author": forms.TextInput(attrs={"class": "dash-input", "dir": "auto"}),
            "phone_main": forms.TextInput(attrs={"class": "dash-input", "dir": "ltr"}),
            "phone_tenders": forms.TextInput(attrs={"class": "dash-input", "dir": "ltr"}),
            "phone_sale": forms.TextInput(attrs={"class": "dash-input", "dir": "ltr"}),
            "phone_support": forms.TextInput(attrs={"class": "dash-input", "dir": "ltr"}),
            "email_general": forms.EmailInput(attrs={"class": "dash-input", "dir": "ltr"}),
            "email_tenders": forms.EmailInput(attrs={"class": "dash-input", "dir": "ltr"}),
            "email_careers": forms.EmailInput(attrs={"class": "dash-input", "dir": "ltr"}),
            "email_sale": forms.EmailInput(attrs={"class": "dash-input", "dir": "ltr"}),
            "email_support": forms.EmailInput(attrs={"class": "dash-input", "dir": "ltr"}),
            "address_line1": forms.TextInput(attrs={"class": "dash-input", "dir": "auto"}),
            "address_line2": forms.TextInput(attrs={"class": "dash-input", "dir": "auto"}),
            "address": forms.Textarea(attrs={"class": "dash-textarea", "rows": 2, "dir": "auto"}),
            "map_embed_url": forms.Textarea(attrs={"class": "dash-textarea", "rows": 2, "dir": "ltr"}),
            "map_directions_url": forms.URLInput(attrs={"class": "dash-input", "dir": "ltr"}),
            "working_hours_weekdays": forms.TextInput(attrs={"class": "dash-input", "dir": "auto"}),
            "working_hours_emergencies": forms.TextInput(attrs={"class": "dash-input", "dir": "auto"}),
            "linkedin_url": forms.URLInput(attrs={"class": "dash-input", "dir": "ltr"}),
            "facebook_url": forms.URLInput(attrs={"class": "dash-input", "dir": "ltr"}),
            "instagram_url": forms.URLInput(attrs={"class": "dash-input", "dir": "ltr"}),
            "youtube_url": forms.URLInput(attrs={"class": "dash-input", "dir": "ltr"}),
        }

    def clean_header_logo(self):
        f = self.cleaned_data.get("header_logo")
        validate_file_size(f, MAX_IMAGE_SIZE_BYTES, "header logo")
        return f

    def clean_footer_logo(self):
        f = self.cleaned_data.get("footer_logo")
        validate_file_size(f, MAX_IMAGE_SIZE_BYTES, "footer logo")
        return f

    def clean_favicon(self):
        f = self.cleaned_data.get("favicon")
        validate_file_size(f, MAX_IMAGE_SIZE_BYTES, "favicon")
        return f


class PageHeroForm(forms.ModelForm):
    class Meta:
        model = PageHero
        fields = ["eyebrow", "title_line1", "title_line2", "description", "hero_image"]
        widgets = {
            "eyebrow": forms.TextInput(attrs={"class": "dash-input", "placeholder": "Upper Kicker", "dir": "auto"}),
            "title_line1": forms.TextInput(attrs={"class": "dash-input", "placeholder": "Architectural Title Line 1", "dir": "auto"}),
            "title_line2": forms.TextInput(attrs={"class": "dash-input", "placeholder": "Architectural Title Line 2 (Optional)", "dir": "auto"}),
            "description": forms.Textarea(attrs={"class": "dash-textarea", "rows": 3, "placeholder": "Hero Banner Description...", "dir": "auto"}),
            "hero_image": forms.FileInput(attrs={"class": "dash-file-input", "accept": "image/*"}),
        }

    def clean_hero_image(self):
        img = self.cleaned_data.get("hero_image")
        validate_file_size(img, MAX_IMAGE_SIZE_BYTES, "hero banner image")
        return img


# ==========================================
# 7. PAGE CMS EDITORS (Home, About, Careers)
# ==========================================
class HomeContentForm(forms.ModelForm):
    class Meta:
        model = HomeContent
        fields = [
            "blueprints_eyebrow",
            "blueprints_title_line1",
            "blueprints_title_line2",
            "blueprints_description",
            "blueprints_btn_text",
            "blueprints_btn_url",
            "blueprints_image",
        ]
        widgets = {
            "blueprints_eyebrow": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. OUR SPECIALIZATION", "dir": "auto"}),
            "blueprints_title_line1": forms.TextInput(attrs={"class": "dash-input", "placeholder": "WE TURN BLUEPRINTS INTO", "dir": "auto"}),
            "blueprints_title_line2": forms.TextInput(attrs={"class": "dash-input", "placeholder": "ENDURING REALITY.", "dir": "auto"}),
            "blueprints_description": forms.Textarea(attrs={"class": "dash-textarea", "rows": 4, "placeholder": "Section narrative...", "dir": "auto"}),
            "blueprints_btn_text": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. View More", "dir": "auto"}),
            "blueprints_btn_url": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. /about/", "dir": "ltr"}),
            "blueprints_image": forms.FileInput(attrs={"class": "dash-file-input", "accept": "image/*", "id": "id_blueprints_image"}),
        }

    def clean_blueprints_image(self):
        img = self.cleaned_data.get("blueprints_image")
        validate_file_size(img, MAX_IMAGE_SIZE_BYTES, "section image")
        return img


class SpecializationItemForm(forms.ModelForm):
    class Meta:
        model = SpecializationItem
        fields = ["discipline", "title", "description", "order", "is_active"]
        widgets = {
            "discipline": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. GRADE A INFRASTRUCTURE", "dir": "auto"}),
            "title": forms.TextInput(attrs={"class": "dash-input", "placeholder": "Full Discipline Title", "dir": "auto"}),
            "description": forms.Textarea(attrs={"class": "dash-textarea", "rows": 3, "placeholder": "Engineering capabilities...", "dir": "auto"}),
            "order": forms.NumberInput(attrs={"class": "dash-input", "style": "width: 120px;", "dir": "ltr"}),
            "is_active": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
        }


class AboutContentForm(forms.ModelForm):
    class Meta:
        model = AboutContent
        fields = [
            "who_we_are_title",
            "who_we_are_p1",
            "who_we_are_p2",
            "cta_eyebrow",
            "cta_title",
            "cta_description",
            "cta_primary_btn_text",
            "cta_primary_btn_url",
            "cta_secondary_btn_text",
            "cta_secondary_btn_url",
        ]
        widgets = {
            "who_we_are_title": forms.TextInput(attrs={"class": "dash-input", "placeholder": "WHO WE ARE", "dir": "auto"}),
            "who_we_are_p1": forms.Textarea(attrs={"class": "dash-textarea", "rows": 4, "placeholder": "First narrative paragraph...", "dir": "auto"}),
            "who_we_are_p2": forms.Textarea(attrs={"class": "dash-textarea", "rows": 4, "placeholder": "Second narrative paragraph...", "dir": "auto"}),
            "cta_eyebrow": forms.TextInput(attrs={"class": "dash-input", "placeholder": "START A PROJECT", "dir": "auto"}),
            "cta_title": forms.TextInput(attrs={"class": "dash-input", "placeholder": "Ready to build something iconic?", "dir": "auto"}),
            "cta_description": forms.Textarea(attrs={"class": "dash-textarea", "rows": 3, "placeholder": "Call to action description...", "dir": "auto"}),
            "cta_primary_btn_text": forms.TextInput(attrs={"class": "dash-input", "placeholder": "Contact Our Team", "dir": "auto"}),
            "cta_primary_btn_url": forms.TextInput(attrs={"class": "dash-input", "placeholder": "/contact/", "dir": "ltr"}),
            "cta_secondary_btn_text": forms.TextInput(attrs={"class": "dash-input", "placeholder": "Explore Projects", "dir": "auto"}),
            "cta_secondary_btn_url": forms.TextInput(attrs={"class": "dash-input", "placeholder": "/projects/", "dir": "ltr"}),
        }


class AboutStatisticForm(forms.ModelForm):
    class Meta:
        model = AboutStatistic
        fields = ["value", "label", "order", "is_active"]
        widgets = {
            "value": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. 30+, Grade A, 1994", "dir": "auto"}),
            "label": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. Years of Industry Leadership", "dir": "auto"}),
            "order": forms.NumberInput(attrs={"class": "dash-input", "style": "width: 120px;", "dir": "ltr"}),
            "is_active": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
        }


class CompanyPillarForm(forms.ModelForm):
    class Meta:
        model = CompanyPillar
        fields = ["number", "title", "description", "order", "is_active"]
        widgets = {
            "number": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. 01, 02", "style": "width: 100px;", "dir": "ltr"}),
            "title": forms.TextInput(attrs={"class": "dash-input", "placeholder": "Pillar Title", "dir": "auto"}),
            "description": forms.Textarea(attrs={"class": "dash-textarea", "rows": 3, "placeholder": "Pillar description...", "dir": "auto"}),
            "order": forms.NumberInput(attrs={"class": "dash-input", "style": "width: 120px;", "dir": "ltr"}),
            "is_active": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
        }


class ServiceItemForm(forms.ModelForm):
    class Meta:
        model = ServiceItem
        fields = ["title", "description", "icon", "order", "is_active"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "dash-input", "placeholder": "Service Title", "dir": "auto"}),
            "description": forms.Textarea(attrs={"class": "dash-textarea", "rows": 3, "placeholder": "Scope and engineering overview...", "dir": "auto"}),
            "icon": forms.TextInput(attrs={"class": "dash-input", "placeholder": "Optional icon code/name", "dir": "ltr"}),
            "order": forms.NumberInput(attrs={"class": "dash-input", "style": "width: 120px;", "dir": "ltr"}),
            "is_active": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
        }


class CareerSettingsForm(forms.ModelForm):
    class Meta:
        model = CareerSettings
        fields = [
            "spontaneous_eyebrow",
            "spontaneous_title",
            "spontaneous_description",
            "spontaneous_btn_text",
            "spontaneous_email",
        ]
        widgets = {
            "spontaneous_eyebrow": forms.TextInput(attrs={"class": "dash-input", "placeholder": "SPONTANEOUS APPLICATION", "dir": "auto"}),
            "spontaneous_title": forms.TextInput(attrs={"class": "dash-input", "placeholder": "Didn't find the right role for you?", "dir": "auto"}),
            "spontaneous_description": forms.Textarea(attrs={"class": "dash-textarea", "rows": 3, "placeholder": "Banner description...", "dir": "auto"}),
            "spontaneous_btn_text": forms.TextInput(attrs={"class": "dash-input", "placeholder": "Send Your CV", "dir": "auto"}),
            "spontaneous_email": forms.EmailInput(attrs={"class": "dash-input", "placeholder": "careers@albahaacontracting.com", "dir": "ltr"}),
        }


class CareerPillarForm(forms.ModelForm):
    class Meta:
        model = CareerPillar
        fields = ["number", "title", "description", "order", "is_active"]
        widgets = {
            "number": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. 01, 02", "style": "width: 100px;", "dir": "ltr"}),
            "title": forms.TextInput(attrs={"class": "dash-input", "placeholder": "Culture Pillar Title", "dir": "auto"}),
            "description": forms.Textarea(attrs={"class": "dash-textarea", "rows": 3, "placeholder": "Culture & values description...", "dir": "auto"}),
            "order": forms.NumberInput(attrs={"class": "dash-input", "style": "width: 120px;", "dir": "ltr"}),
            "is_active": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
        }


# ==========================================
# 8. PARTNERS & LEADERSHIP FORMS
# ==========================================
class ClientLogoForm(forms.ModelForm):
    class Meta:
        model = ClientLogo
        fields = ["name", "logo_image", "show_on_home", "show_on_about", "is_active", "order"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "dash-input", "placeholder": "Partner / Client Name", "dir": "auto"}),
            "logo_image": forms.FileInput(attrs={"class": "dash-file-input", "accept": "image/*", "id": "id_logo_image"}),
            "show_on_home": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
            "show_on_about": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
            "is_active": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
            "order": forms.NumberInput(attrs={"class": "dash-input", "style": "width: 120px;", "dir": "ltr"}),
        }

    def clean_logo_image(self):
        img = self.cleaned_data.get("logo_image")
        validate_file_size(img, MAX_IMAGE_SIZE_BYTES, "logo image")
        return img


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ["name", "position", "member_type", "photo", "quote", "bio", "order", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "dash-input", "placeholder": "Full Name", "dir": "auto"}),
            "position": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. CEO / Board Member", "dir": "auto"}),
            "member_type": forms.Select(attrs={"class": "dash-select"}),
            "photo": forms.FileInput(attrs={"class": "dash-file-input", "accept": "image/*", "id": "id_photo"}),
            "quote": forms.Textarea(attrs={"class": "dash-textarea", "rows": 3, "placeholder": "Executive quote or vision statement", "dir": "auto"}),
            "bio": forms.Textarea(attrs={"class": "dash-textarea", "rows": 4, "placeholder": "Detailed biographical summary...", "dir": "auto"}),
            "order": forms.NumberInput(attrs={"class": "dash-input", "style": "width: 120px;", "dir": "ltr"}),
            "is_active": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
        }

    def clean_photo(self):
        img = self.cleaned_data.get("photo")
        validate_file_size(img, MAX_IMAGE_SIZE_BYTES, "member photo")
        return img


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["client_name", "position", "company", "quote", "avatar", "is_accent", "is_featured", "show_on_home", "show_on_about", "order"]
        widgets = {
            "client_name": forms.TextInput(attrs={"class": "dash-input", "placeholder": "Client Name or Authority", "dir": "auto"}),
            "position": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. Project Director", "dir": "auto"}),
            "company": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. Cairo Regional Office", "dir": "auto"}),
            "quote": forms.Textarea(attrs={"class": "dash-textarea", "rows": 4, "placeholder": "Testimonial quote text...", "dir": "auto"}),
            "avatar": forms.FileInput(attrs={"class": "dash-file-input", "accept": "image/*", "id": "id_avatar"}),
            "is_accent": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
            "is_featured": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
            "show_on_home": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
            "show_on_about": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
            "order": forms.NumberInput(attrs={"class": "dash-input", "style": "width: 120px;", "dir": "ltr"}),
        }

    def clean_avatar(self):
        img = self.cleaned_data.get("avatar")
        validate_file_size(img, MAX_IMAGE_SIZE_BYTES, "client avatar")
        return img
