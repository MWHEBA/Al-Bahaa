from django.contrib import admin
from django.utils.html import format_html

from .models import Project, ProjectCategory, ProjectImage


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ("image", "image_preview", "caption", "order")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height: 40px; border-radius: 4px; object-fit: cover;">',
                obj.image.url,
            )
        return "-"

    image_preview.short_description = "Preview"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "cover_preview", "status", "location", "is_featured", "order")
    list_filter = ("category", "status", "is_featured", "date")
    list_editable = ("order", "is_featured", "status")
    search_fields = ("title", "short_description", "full_description", "client_name", "location", "architect_consultant")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectImageInline]

    fieldsets = (
        (
            "Primary Information",
            {
                "fields": (
                    "title",
                    "slug",
                    "category",
                    "status",
                    "is_featured",
                    "order",
                )
            },
        ),
        (
            "Media & Visuals",
            {
                "fields": (
                    "cover_image",
                )
            },
        ),
        (
            "Project Narrative & Descriptions",
            {
                "fields": (
                    "short_description",
                    "full_description",
                )
            },
        ),
        (
            "Technical Specifications & Metrics",
            {
                "fields": (
                    "client_name",
                    "location",
                    "date",
                    "built_up_area",
                    "scope_of_work",
                    "architect_consultant",
                    "sustainability",
                )
            },
        ),
        (
            "Engineering Disciplines & Highlights",
            {
                "fields": (
                    "engineering_highlights",
                ),
                "description": "Enter each key engineering achievement/bullet on a separate line.",
            },
        ),
    )

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="height: 38px; width: 60px; border-radius: 4px; object-fit: cover;">',
                obj.cover_image.url,
            )
        return format_html('<span style="color: #999;">Fallback</span>')

    cover_preview.short_description = "Cover Preview"


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
