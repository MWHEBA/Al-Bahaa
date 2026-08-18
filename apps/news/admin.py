from django.contrib import admin
from django.utils.html import format_html

from .models import NewsCategory, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "cover_preview", "published_at", "is_published", "order")
    list_filter = ("category", "is_published", "published_at")
    list_editable = ("order", "is_published")
    search_fields = ("title", "excerpt", "content", "author")
    prepopulated_fields = {"slug": ("title",)}

    fieldsets = (
        (
            "Article Essentials",
            {
                "fields": (
                    "title",
                    "slug",
                    "category",
                    "author",
                    "published_at",
                    "is_published",
                    "order",
                )
            },
        ),
        (
            "Media",
            {
                "fields": (
                    "cover_image",
                )
            },
        ),
        (
            "Article Body",
            {
                "fields": (
                    "excerpt",
                    "content",
                )
            },
        ),
    )

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="height: 38px; width: 60px; border-radius: 4px; object-fit: cover;">',
                obj.cover_image.url,
            )
        return format_html('<span style="color: #999;">Default</span>')

    cover_preview.short_description = "Cover Preview"


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
