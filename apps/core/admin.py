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
    list_display = ("name", "email", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "message")
    readonly_fields = ("created_at",)

