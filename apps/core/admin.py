import csv
from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html

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
    PageHero,
    ServiceItem,
    SiteSettings,
    SpecializationItem,
    TeamMember,
    Testimonial,
)

# ==========================================
# 1. LUXURY CORPORATE ADMIN BRANDING
# ==========================================
admin.site.site_header = "AL BAHAA CONTRACTING (S.A.E)"
admin.site.site_title = "Al Bahaa Executive Control Panel"
admin.site.index_title = "Corporate Operations & Content Management"


# ==========================================
# 2. SINGLETON ADMIN BASE
# ==========================================
class SingletonModelAdmin(admin.ModelAdmin):
    """Admin class for single-instance models to prevent deletion and multiple entries."""

    def has_add_permission(self, request):
        count = self.model.objects.count()
        return count == 0

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj, _ = self.model.objects.get_or_create(pk=1)
        return HttpResponseRedirect(
            reverse(
                f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change",
                args=[obj.pk],
            )
        )


# ==========================================
# 3. SITE SETTINGS & HEROES
# ==========================================
@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonModelAdmin):
    fieldsets = (
        (
            "Corporate Identity & Branding",
            {
                "fields": (
                    "company_name",
                    "header_logo",
                    "footer_logo",
                    "favicon",
                    "copyright_text",
                )
            },
        ),
        (
            "Contact Phone Numbers",
            {
                "fields": (
                    "phone_main",
                    "phone_tenders",
                    "phone_sale",
                    "phone_support",
                )
            },
        ),
        (
            "Official Email Addresses",
            {
                "fields": (
                    "email_general",
                    "email_tenders",
                    "email_careers",
                    "email_sale",
                    "email_support",
                )
            },
        ),
        (
            "Headquarters & Interactive Google Maps",
            {
                "fields": (
                    "address_line1",
                    "address_line2",
                    "address",
                    "map_embed_url",
                    "map_directions_url",
                )
            },
        ),
        (
            "Working Hours",
            {
                "fields": (
                    "working_hours_weekdays",
                    "working_hours_emergencies",
                )
            },
        ),
        (
            "Official Social Media Channels",
            {
                "fields": (
                    "linkedin_url",
                    "facebook_url",
                    "instagram_url",
                    "youtube_url",
                ),
            },
        ),
        (
            "Footer Foundation Quote",
            {
                "fields": (
                    "footer_quote",
                    "footer_quote_author",
                )
            },
        ),
    )


@admin.register(PageHero)
class PageHeroAdmin(admin.ModelAdmin):
    list_display = ("page", "eyebrow", "title_line1", "title_line2", "hero_preview")
    list_filter = ("page",)
    search_fields = ("page", "eyebrow", "title_line1", "title_line2", "description")

    fieldsets = (
        ("Page Target", {"fields": ("page",)}),
        (
            "Typography & Titles",
            {
                "fields": (
                    "eyebrow",
                    "title_line1",
                    "title_line2",
                    "description",
                )
            },
        ),
        ("Banner Visual Media", {"fields": ("hero_image",)}),
    )

    def hero_preview(self, obj):
        if obj.hero_image:
            return format_html(
                '<img src="{}" style="height: 38px; width: 68px; object-fit: cover; border-radius: 4px;">',
                obj.hero_image.url,
            )
        return format_html('<span style="color: #999;">Fallback</span>')

    hero_preview.short_description = "Visual Preview"


# ==========================================
# 4. HOME & ABOUT SPECIFIC CONTENT
# ==========================================
@admin.register(HomeContent)
class HomeContentAdmin(SingletonModelAdmin):
    fieldsets = (
        (
            "Blueprints & Enduring Reality Section",
            {
                "fields": (
                    "blueprints_eyebrow",
                    "blueprints_title_line1",
                    "blueprints_title_line2",
                    "blueprints_description",
                    "blueprints_btn_text",
                    "blueprints_btn_url",
                    "blueprints_image",
                )
            },
        ),
    )


@admin.register(SpecializationItem)
class SpecializationItemAdmin(admin.ModelAdmin):
    list_display = ("discipline", "title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("discipline", "title", "description")


@admin.register(AboutContent)
class AboutContentAdmin(SingletonModelAdmin):
    fieldsets = (
        (
            "Who We Are - Narrative Block",
            {
                "fields": (
                    "who_we_are_title",
                    "who_we_are_p1",
                    "who_we_are_p2",
                )
            },
        ),
        (
            "Bottom Call-To-Action (CTA)",
            {
                "fields": (
                    "cta_eyebrow",
                    "cta_title",
                    "cta_description",
                    "cta_primary_btn_text",
                    "cta_primary_btn_url",
                    "cta_secondary_btn_text",
                    "cta_secondary_btn_url",
                )
            },
        ),
    )


@admin.register(AboutStatistic)
class AboutStatisticAdmin(admin.ModelAdmin):
    list_display = ("value", "label", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("value", "label")


@admin.register(CompanyPillar)
class CompanyPillarAdmin(admin.ModelAdmin):
    list_display = ("number", "title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "description")


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "member_type", "photo_preview", "order", "is_active")
    list_filter = ("member_type", "is_active")
    list_editable = ("order", "is_active", "member_type")
    search_fields = ("name", "position", "quote", "bio")

    fieldsets = (
        ("Personal Information", {"fields": ("name", "position", "member_type", "photo")}),
        ("Biography & Quotes", {"fields": ("quote", "bio")}),
        ("Display Settings", {"fields": ("order", "is_active")}),
    )

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="height: 38px; width: 38px; border-radius: 50%; object-fit: cover;">',
                obj.photo.url,
            )
        return "-"

    photo_preview.short_description = "Photo"


@admin.register(ServiceItem)
class ServiceItemAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "description")


# ==========================================
# 5. CAREERS CONTENT & RECRUITMENT
# ==========================================
@admin.register(CareerSettings)
class CareerSettingsAdmin(SingletonModelAdmin):
    fieldsets = (
        (
            "Spontaneous Application Banner",
            {
                "fields": (
                    "spontaneous_eyebrow",
                    "spontaneous_title",
                    "spontaneous_description",
                    "spontaneous_btn_text",
                    "spontaneous_email",
                )
            },
        ),
    )


@admin.register(CareerPillar)
class CareerPillarAdmin(admin.ModelAdmin):
    list_display = ("number", "title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "description")


@admin.register(JobDepartment)
class JobDepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ("title", "department", "location", "job_type", "experience", "is_active", "order")
    list_filter = ("department", "job_type", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "summary", "responsibilities", "requirements")
    prepopulated_fields = {"slug": ("title",)}


def export_applications_to_csv(modeladmin, request, queryset):
    """Export selected job applications into standard CSV."""
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="AlBahaa_Job_Applications.csv"'
    writer = csv.writer(response)
    writer.writerow(["Candidate Name", "Email", "Phone", "Applied Role", "Status", "Date Submitted", "CV File URL"])
    for app in queryset:
        cv_url = request.build_absolute_uri(app.resume.url) if app.resume else "N/A"
        writer.writerow([app.full_name, app.email, app.phone, app.job.title, app.get_status_display(), app.submitted_at.strftime("%Y-%m-%d %H:%M"), cv_url])
    return response

export_applications_to_csv.short_description = "Export Selected to CSV / Excel"


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "job", "email", "phone", "status_badge", "resume_download_btn", "submitted_at")
    list_filter = ("status", "job__department", "job", "submitted_at")
    search_fields = ("full_name", "email", "phone", "cover_note", "internal_notes")
    readonly_fields = ("submitted_at", "resume_preview")
    actions = [export_applications_to_csv]

    fieldsets = (
        (
            "Candidate Information",
            {
                "fields": (
                    "job",
                    "full_name",
                    "email",
                    "phone",
                    "cover_note",
                    "resume",
                    "resume_preview",
                    "submitted_at",
                )
            },
        ),
        (
            "Recruitment Review & Workflow",
            {
                "fields": (
                    "status",
                    "internal_notes",
                )
            },
        ),
    )

    def status_badge(self, obj):
        colors = {
            "new": ("#10b981", "#ffffff"),
            "reviewed": ("#f59e0b", "#ffffff"),
            "shortlisted": ("#3b82f6", "#ffffff"),
            "rejected": ("#6b7280", "#ffffff"),
        }
        bg, fg = colors.get(obj.status, ("#6b7280", "#ffffff"))
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 4px 10px; border-radius: 9999px; font-size: 11px; font-weight: 600; text-transform: uppercase;">{}</span>',
            bg,
            fg,
            obj.get_status_display(),
        )

    status_badge.short_description = "Status"

    def resume_download_btn(self, obj):
        if obj.resume:
            return format_html(
                '<a href="{}" target="_blank" style="display: inline-block; background-color: #1e293b; color: #fff; padding: 4px 10px; border-radius: 4px; font-size: 12px; text-decoration: none; font-weight: 600;">Download CV</a>',
                obj.resume.url,
            )
        return format_html('<span style="color: #999;">No Resume</span>')

    resume_download_btn.short_description = "CV File"

    def resume_preview(self, obj):
        if obj.resume:
            return format_html(
                '<a href="{}" target="_blank" style="font-weight: bold; color: #0284c7;">Click here to view / download attached CV ({})</a>',
                obj.resume.url,
                obj.resume.name,
            )
        return "No resume file attached"

    resume_preview.short_description = "Resume File"


# ==========================================
# 6. CLIENTS, TESTIMONIALS & INQUIRIES
# ==========================================
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        "client_name",
        "position",
        "company",
        "is_featured",
        "is_accent",
        "show_on_home",
        "show_on_about",
        "order",
    )
    list_filter = ("is_featured", "is_accent", "show_on_home", "show_on_about")
    list_editable = ("order", "is_featured", "is_accent", "show_on_home", "show_on_about")
    search_fields = ("client_name", "company", "quote")


@admin.register(ClientLogo)
class ClientLogoAdmin(admin.ModelAdmin):
    list_display = ("name", "logo_preview", "show_on_home", "show_on_about", "is_active", "order")
    list_filter = ("show_on_home", "show_on_about", "is_active")
    list_editable = ("order", "show_on_home", "show_on_about", "is_active")
    search_fields = ("name",)

    def logo_preview(self, obj):
        if obj.logo_image:
            return format_html(
                '<img src="{}" style="height: 30px; max-width: 120px; object-fit: contain; background: #f8fafc; padding: 2px; border-radius: 4px;">',
                obj.logo_image.url,
            )
        return "-"

    logo_preview.short_description = "Logo Preview"


def export_messages_to_csv(modeladmin, request, queryset):
    """Export selected contact inquiries into standard CSV."""
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="AlBahaa_Contact_Inquiries.csv"'
    writer = csv.writer(response)
    writer.writerow(["Client Name", "Company", "Inquiry Type", "Email", "Phone", "Status", "Date Submitted", "Message Body"])
    for msg in queryset:
        writer.writerow([msg.name, msg.company, msg.get_inquiry_type_display(), msg.email, msg.phone, msg.get_status_display(), msg.created_at.strftime("%Y-%m-%d %H:%M"), msg.message])
    return response

export_messages_to_csv.short_description = "Export Selected to CSV / Excel"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "inquiry_type", "email", "phone", "status_badge", "created_at")
    list_filter = ("status", "inquiry_type", "created_at")
    search_fields = ("name", "company", "email", "phone", "message", "internal_notes")
    readonly_fields = ("created_at",)
    actions = [export_messages_to_csv]

    fieldsets = (
        (
            "Inquiry Details",
            {
                "fields": (
                    "name",
                    "company",
                    "inquiry_type",
                    "email",
                    "phone",
                    "message",
                    "created_at",
                )
            },
        ),
        (
            "Management Status & Response Notes",
            {
                "fields": (
                    "status",
                    "internal_notes",
                )
            },
        ),
    )

    def status_badge(self, obj):
        colors = {
            "unread": ("#ef4444", "#ffffff"),
            "read": ("#f59e0b", "#ffffff"),
            "resolved": ("#10b981", "#ffffff"),
        }
        bg, fg = colors.get(obj.status, ("#6b7280", "#ffffff"))
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 4px 10px; border-radius: 9999px; font-size: 11px; font-weight: 600; text-transform: uppercase;">{}</span>',
            bg,
            fg,
            obj.get_status_display(),
        )

    status_badge.short_description = "Inquiry Status"
