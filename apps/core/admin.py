from django.contrib import admin

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


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("__str__", "phone_sale", "email_sale")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("client_name", "position", "company", "is_featured", "order")
    list_filter = ("is_featured",)
    search_fields = ("client_name", "company", "quote")


@admin.register(ClientLogo)
class ClientLogoAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    search_fields = ("name",)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "order")
    search_fields = ("name", "position", "quote")


@admin.register(ServiceItem)
class ServiceItemAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    search_fields = ("title", "description")


@admin.register(JobDepartment)
class JobDepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ("title", "department", "location", "job_type", "experience", "is_active", "order")
    list_filter = ("department", "job_type", "is_active")
    search_fields = ("title", "summary", "responsibilities", "requirements")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "job", "email", "phone", "submitted_at")
    list_filter = ("job", "submitted_at")
    search_fields = ("full_name", "email", "phone", "cover_note")
    readonly_fields = ("submitted_at",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "inquiry_type", "email", "phone", "created_at", "is_read")
    list_filter = ("inquiry_type", "is_read", "created_at")
    search_fields = ("name", "company", "email", "phone", "message")
    readonly_fields = ("created_at",)

