from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
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


# ==========================================
# 1. AUTH & PROFILE FORMS
# ==========================================
class ExecutiveProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "dash-input", "placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"class": "dash-input", "placeholder": "Last Name"}),
            "email": forms.EmailInput(attrs={"class": "dash-input", "placeholder": "corporate@albahaa.com"}),
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
        help_text="Select one or multiple high-resolution site execution photos for the project gallery.",
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
            "title": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. Eastern Al-Ma'abda Sewerage System"}),
            "slug": forms.TextInput(attrs={"class": "dash-input", "placeholder": "auto-generated-if-left-empty"}),
            "category": forms.Select(attrs={"class": "dash-select"}),
            "status": forms.Select(attrs={"class": "dash-select"}),
            "location": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. Assiut, Egypt"}),
            "client_name": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. NOPWASD"}),
            "architect_consultant": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. Dar Al-Handasah"}),
            "scope_of_work": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. Turnkey Infrastructure Contracting"}),
            "built_up_area": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. 350,000 LM Network Scale"}),
            "date": forms.DateInput(attrs={"class": "dash-input", "type": "date"}),
            "cover_image": forms.FileInput(attrs={"class": "dash-file-input", "accept": "image/*", "id": "id_cover_image"}),
            "short_description": forms.Textarea(attrs={"class": "dash-textarea", "rows": 3, "placeholder": "Brief 1-2 sentence executive summary"}),
            "full_description": forms.Textarea(attrs={"class": "dash-textarea", "rows": 6, "placeholder": "Detailed multi-paragraph project description..."}),
            "engineering_highlights": forms.Textarea(attrs={"class": "dash-textarea", "rows": 5, "placeholder": "One engineering highlight per line..."}),
            "sustainability": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. EDGE Green Building compliant"}),
            "is_featured": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
            "order": forms.NumberInput(attrs={"class": "dash-input", "style": "width: 120px;"}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get("slug", "").strip()
        title = self.cleaned_data.get("title", "")
        if not slug and title:
            base_slug = slugify(title)
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
            "name": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. Water & Sewage Infrastructure"}),
            "slug": forms.TextInput(attrs={"class": "dash-input", "placeholder": "auto-generated"}),
            "order": forms.NumberInput(attrs={"class": "dash-input", "style": "width: 120px;"}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get("slug", "").strip()
        name = self.cleaned_data.get("name", "")
        if not slug and name:
            slug = slugify(name)
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
            "title": forms.TextInput(attrs={"class": "dash-input", "placeholder": "Article Title"}),
            "slug": forms.TextInput(attrs={"class": "dash-input", "placeholder": "auto-generated-if-empty"}),
            "category": forms.Select(attrs={"class": "dash-select"}),
            "author": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. Eng. Ahmed Bahaa (CEO)"}),
            "cover_image": forms.FileInput(attrs={"class": "dash-file-input", "accept": "image/*", "id": "id_cover_image"}),
            "excerpt": forms.Textarea(attrs={"class": "dash-textarea", "rows": 3, "placeholder": "Brief summary kicker"}),
            "content": forms.Textarea(attrs={"class": "dash-textarea", "rows": 8, "placeholder": "Full article content..."}),
            "published_at": forms.DateTimeInput(attrs={"class": "dash-input", "type": "datetime-local"}),
            "is_published": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
            "order": forms.NumberInput(attrs={"class": "dash-input", "style": "width: 120px;"}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get("slug", "").strip()
        title = self.cleaned_data.get("title", "")
        if not slug and title:
            base_slug = slugify(title)
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
            "name": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. Infrastructure"}),
            "slug": forms.TextInput(attrs={"class": "dash-input", "placeholder": "auto-generated"}),
            "order": forms.NumberInput(attrs={"class": "dash-input", "style": "width: 120px;"}),
        }


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
            "title": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. Senior Infrastructure Project Manager"}),
            "slug": forms.TextInput(attrs={"class": "dash-input", "placeholder": "auto-generated-if-empty"}),
            "department": forms.Select(attrs={"class": "dash-select"}),
            "location": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. New Cairo, Egypt"}),
            "job_type": forms.Select(attrs={"class": "dash-select"}),
            "experience": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. 8-12 Years"}),
            "summary": forms.Textarea(attrs={"class": "dash-textarea", "rows": 3, "placeholder": "Executive role summary"}),
            "responsibilities": forms.Textarea(attrs={"class": "dash-textarea", "rows": 5, "placeholder": "One bullet per line..."}),
            "requirements": forms.Textarea(attrs={"class": "dash-textarea", "rows": 5, "placeholder": "One requirement per line..."}),
            "benefits": forms.Textarea(attrs={"class": "dash-textarea", "rows": 4, "placeholder": "One benefit per line..."}),
            "is_active": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
            "order": forms.NumberInput(attrs={"class": "dash-input", "style": "width: 120px;"}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get("slug", "").strip()
        title = self.cleaned_data.get("title", "")
        if not slug and title:
            base_slug = slugify(title)
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
            "name": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. Site Engineering"}),
            "slug": forms.TextInput(attrs={"class": "dash-input", "placeholder": "auto-generated"}),
            "order": forms.NumberInput(attrs={"class": "dash-input", "style": "width: 120px;"}),
        }


class JobApplicationReviewForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ["status", "internal_notes"]
        widgets = {
            "status": forms.Select(attrs={"class": "dash-select"}),
            "internal_notes": forms.Textarea(attrs={"class": "dash-textarea", "rows": 4, "placeholder": "Private HR internal notes and evaluation..."}),
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
            "internal_notes": forms.Textarea(attrs={"class": "dash-textarea", "rows": 4, "placeholder": "Internal reply status, assigned engineer, or follow-up notes..."}),
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
            "company_name": forms.TextInput(attrs={"class": "dash-input"}),
            "header_logo": forms.FileInput(attrs={"class": "dash-file-input", "accept": "image/*", "id": "id_header_logo"}),
            "footer_logo": forms.FileInput(attrs={"class": "dash-file-input", "accept": "image/*", "id": "id_footer_logo"}),
            "favicon": forms.FileInput(attrs={"class": "dash-file-input", "accept": "image/*,.ico,.svg", "id": "id_favicon"}),
            "copyright_text": forms.TextInput(attrs={"class": "dash-input"}),
            "footer_quote": forms.Textarea(attrs={"class": "dash-textarea", "rows": 3}),
            "footer_quote_author": forms.TextInput(attrs={"class": "dash-input"}),
            "phone_main": forms.TextInput(attrs={"class": "dash-input"}),
            "phone_tenders": forms.TextInput(attrs={"class": "dash-input"}),
            "phone_sale": forms.TextInput(attrs={"class": "dash-input"}),
            "phone_support": forms.TextInput(attrs={"class": "dash-input"}),
            "email_general": forms.EmailInput(attrs={"class": "dash-input"}),
            "email_tenders": forms.EmailInput(attrs={"class": "dash-input"}),
            "email_careers": forms.EmailInput(attrs={"class": "dash-input"}),
            "email_sale": forms.EmailInput(attrs={"class": "dash-input"}),
            "email_support": forms.EmailInput(attrs={"class": "dash-input"}),
            "address_line1": forms.TextInput(attrs={"class": "dash-input"}),
            "address_line2": forms.TextInput(attrs={"class": "dash-input"}),
            "address": forms.Textarea(attrs={"class": "dash-textarea", "rows": 2}),
            "map_embed_url": forms.Textarea(attrs={"class": "dash-textarea", "rows": 2}),
            "map_directions_url": forms.URLInput(attrs={"class": "dash-input"}),
            "working_hours_weekdays": forms.TextInput(attrs={"class": "dash-input"}),
            "working_hours_emergencies": forms.TextInput(attrs={"class": "dash-input"}),
            "linkedin_url": forms.URLInput(attrs={"class": "dash-input"}),
            "facebook_url": forms.URLInput(attrs={"class": "dash-input"}),
            "instagram_url": forms.URLInput(attrs={"class": "dash-input"}),
            "youtube_url": forms.URLInput(attrs={"class": "dash-input"}),
        }


class PageHeroForm(forms.ModelForm):
    class Meta:
        model = PageHero
        fields = ["eyebrow", "title_line1", "title_line2", "description", "hero_image"]
        widgets = {
            "eyebrow": forms.TextInput(attrs={"class": "dash-input", "placeholder": "Upper Kicker"}),
            "title_line1": forms.TextInput(attrs={"class": "dash-input", "placeholder": "Architectural Title Line 1"}),
            "title_line2": forms.TextInput(attrs={"class": "dash-input", "placeholder": "Architectural Title Line 2 (Optional)"}),
            "description": forms.Textarea(attrs={"class": "dash-textarea", "rows": 3, "placeholder": "Hero Banner Description..."}),
            "hero_image": forms.ClearableFileInput(attrs={"class": "dash-file-input"}),
        }


# ==========================================
# 7. CLIENTS, TESTIMONIALS & TEAM FORMS
# ==========================================
class ClientLogoForm(forms.ModelForm):
    class Meta:
        model = ClientLogo
        fields = ["name", "logo_image", "show_on_home", "show_on_about", "is_active", "order"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "dash-input", "placeholder": "Partner / Client Name"}),
            "logo_image": forms.FileInput(attrs={"class": "dash-file-input", "accept": "image/*", "id": "id_logo_image"}),
            "show_on_home": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
            "show_on_about": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
            "is_active": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
            "order": forms.NumberInput(attrs={"class": "dash-input", "style": "width: 120px;"}),
        }


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ["name", "position", "member_type", "photo", "quote", "bio", "order", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "dash-input", "placeholder": "Full Name"}),
            "position": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. CEO / Board Member"}),
            "member_type": forms.Select(attrs={"class": "dash-select"}),
            "photo": forms.FileInput(attrs={"class": "dash-file-input", "accept": "image/*", "id": "id_photo"}),
            "quote": forms.Textarea(attrs={"class": "dash-textarea", "rows": 3, "placeholder": "Executive quote or vision statement"}),
            "bio": forms.Textarea(attrs={"class": "dash-textarea", "rows": 4, "placeholder": "Detailed biographical summary..."}),
            "order": forms.NumberInput(attrs={"class": "dash-input", "style": "width: 120px;"}),
            "is_active": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
        }


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["client_name", "position", "company", "quote", "avatar", "is_accent", "is_featured", "show_on_home", "show_on_about", "order"]
        widgets = {
            "client_name": forms.TextInput(attrs={"class": "dash-input", "placeholder": "Client Name or Authority"}),
            "position": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. Project Director"}),
            "company": forms.TextInput(attrs={"class": "dash-input", "placeholder": "e.g. Cairo Regional Office"}),
            "quote": forms.Textarea(attrs={"class": "dash-textarea", "rows": 4, "placeholder": "Testimonial quote text..."}),
            "avatar": forms.ClearableFileInput(attrs={"class": "dash-file-input"}),
            "is_accent": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
            "is_featured": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
            "show_on_home": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
            "show_on_about": forms.CheckboxInput(attrs={"class": "dash-checkbox"}),
            "order": forms.NumberInput(attrs={"class": "dash-input", "style": "width: 120px;"}),
        }
