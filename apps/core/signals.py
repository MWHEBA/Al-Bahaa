import os
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from apps.news.models import NewsCategory, Post
from apps.projects.models import Project, ProjectCategory, ProjectImage
from .models import (
    AboutContent,
    CareerSettings,
    ClientLogo,
    HomeContent,
    JobApplication,
    PageHero,
    SiteSettings,
    TeamMember,
    Testimonial,
)


from io import BytesIO
from PIL import Image, ImageOps
from django.core.files.base import ContentFile
from django.db.backends.signals import connection_created


@receiver(connection_created)
def set_sqlite_pragmas(sender, connection, **kwargs):
    """Enable WAL mode, fast synchronization and in-memory cache for SQLite."""
    if connection.vendor == "sqlite":
        try:
            cursor = connection.cursor()
            cursor.execute("PRAGMA journal_mode = WAL;")
            cursor.execute("PRAGMA synchronous = NORMAL;")
            cursor.execute("PRAGMA cache_size = -64000;")
            cursor.execute("PRAGMA temp_store = MEMORY;")
        except Exception:
            pass


def auto_optimize_image_field(field_file, max_dim=1920, quality=82):
    """Automatically resize and compress newly uploaded images to WebP."""
    if not field_file or not hasattr(field_file, "file"):
        return
    try:
        # Avoid re-processing if already a webp file
        if field_file.name.lower().endswith(".webp"):
            return

        with Image.open(field_file) as img:
            try:
                img = ImageOps.exif_transpose(img)
            except Exception:
                pass

            w, h = img.size
            if max(w, h) > max_dim:
                ratio = max_dim / max(w, h)
                new_size = (max(1, int(w * ratio)), max(1, int(h * ratio)))
                img = img.resize(new_size, Image.Resampling.LANCZOS)

            output = BytesIO()
            if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                img = img.convert("RGBA")
                img.save(output, format="WEBP", quality=quality, method=6)
            else:
                img = img.convert("RGB")
                img.save(output, format="WEBP", quality=quality, method=6)

            output.seek(0)
            base_name = os.path.splitext(field_file.name)[0]
            new_name = f"{base_name}.webp"
            field_file.save(new_name, ContentFile(output.read()), save=False)
    except Exception:
        pass


@receiver([post_save, post_delete], sender=SiteSettings)
@receiver([post_save, post_delete], sender=PageHero)
@receiver([post_save, post_delete], sender=HomeContent)
@receiver([post_save, post_delete], sender=AboutContent)
@receiver([post_save, post_delete], sender=CareerSettings)
@receiver([post_save, post_delete], sender=ProjectCategory)
@receiver([post_save, post_delete], sender=NewsCategory)
def clear_site_cache(sender, **kwargs):
    """Clear memory cache when global settings, heroes, or categories are updated."""
    cache.delete("site_settings_cached")
    cache.delete("page_heroes_cached")
    cache.delete("footer_categories_cached")
    cache.delete("home_content_cached")
    cache.delete("about_content_cached")
    cache.delete("career_settings_cached")


def delete_file_safely(file_field):
    if file_field and hasattr(file_field, "path"):
        try:
            if os.path.isfile(file_field.path):
                os.remove(file_field.path)
        except Exception:
            pass


# ==========================================
# Post-Delete File Cleaners
# ==========================================
@receiver(post_delete, sender=ClientLogo)
def auto_delete_client_logo(sender, instance, **kwargs):
    delete_file_safely(instance.logo_image)


@receiver(post_delete, sender=TeamMember)
def auto_delete_team_photo(sender, instance, **kwargs):
    delete_file_safely(instance.photo)


@receiver(post_delete, sender=PageHero)
def auto_delete_page_hero_image(sender, instance, **kwargs):
    delete_file_safely(instance.hero_image)


@receiver(post_delete, sender=HomeContent)
def auto_delete_home_blueprints_image(sender, instance, **kwargs):
    delete_file_safely(instance.blueprints_image)


@receiver(post_delete, sender=Project)
def auto_delete_project_cover(sender, instance, **kwargs):
    delete_file_safely(instance.cover_image)


@receiver(post_delete, sender=ProjectImage)
def auto_delete_project_gallery_image(sender, instance, **kwargs):
    delete_file_safely(instance.image)


@receiver(post_delete, sender=Post)
def auto_delete_post_cover(sender, instance, **kwargs):
    delete_file_safely(instance.cover_image)


@receiver(post_delete, sender=JobApplication)
def auto_delete_job_application_resume(sender, instance, **kwargs):
    delete_file_safely(instance.resume)


# ==========================================
# Pre-Save File Cleaners & Auto-WebP Compression
# ==========================================
@receiver(pre_save, sender=SiteSettings)
def cleanup_sitesettings_on_update(sender, instance, **kwargs):
    if instance.header_logo:
        auto_optimize_image_field(instance.header_logo, max_dim=600, quality=85)
    if instance.footer_logo:
        auto_optimize_image_field(instance.footer_logo, max_dim=600, quality=85)
    if instance.favicon:
        auto_optimize_image_field(instance.favicon, max_dim=128, quality=90)

    if not instance.pk:
        return
    try:
        old_obj = SiteSettings.objects.get(pk=instance.pk)
        if old_obj.header_logo and old_obj.header_logo != instance.header_logo:
            delete_file_safely(old_obj.header_logo)
        if old_obj.footer_logo and old_obj.footer_logo != instance.footer_logo:
            delete_file_safely(old_obj.footer_logo)
        if old_obj.favicon and old_obj.favicon != instance.favicon:
            delete_file_safely(old_obj.favicon)
    except SiteSettings.DoesNotExist:
        pass


@receiver(pre_save, sender=PageHero)
def cleanup_hero_on_update(sender, instance, **kwargs):
    if instance.hero_image:
        auto_optimize_image_field(instance.hero_image, max_dim=1920, quality=82)

    if not instance.pk:
        return
    try:
        old_obj = PageHero.objects.get(pk=instance.pk)
        if old_obj.hero_image and old_obj.hero_image != instance.hero_image:
            delete_file_safely(old_obj.hero_image)
    except PageHero.DoesNotExist:
        pass


@receiver(pre_save, sender=HomeContent)
def cleanup_home_content_on_update(sender, instance, **kwargs):
    if instance.blueprints_image:
        auto_optimize_image_field(instance.blueprints_image, max_dim=1200, quality=82)

    if not instance.pk:
        return
    try:
        old_obj = HomeContent.objects.get(pk=instance.pk)
        if old_obj.blueprints_image and old_obj.blueprints_image != instance.blueprints_image:
            delete_file_safely(old_obj.blueprints_image)
    except HomeContent.DoesNotExist:
        pass


@receiver(pre_save, sender=TeamMember)
def cleanup_team_on_update(sender, instance, **kwargs):
    if instance.photo:
        auto_optimize_image_field(instance.photo, max_dim=800, quality=82)

    if not instance.pk:
        return
    try:
        old_obj = TeamMember.objects.get(pk=instance.pk)
        if old_obj.photo and old_obj.photo != instance.photo:
            delete_file_safely(old_obj.photo)
    except TeamMember.DoesNotExist:
        pass


@receiver(pre_save, sender=ClientLogo)
def cleanup_client_logo_on_update(sender, instance, **kwargs):
    if instance.logo_image:
        auto_optimize_image_field(instance.logo_image, max_dim=600, quality=85)

    if not instance.pk:
        return
    try:
        old_obj = ClientLogo.objects.get(pk=instance.pk)
        if old_obj.logo_image and old_obj.logo_image != instance.logo_image:
            delete_file_safely(old_obj.logo_image)
    except ClientLogo.DoesNotExist:
        pass


@receiver(pre_save, sender=Project)
def cleanup_project_on_update(sender, instance, **kwargs):
    if instance.cover_image:
        auto_optimize_image_field(instance.cover_image, max_dim=1920, quality=82)

    if not instance.pk:
        return
    try:
        old_obj = Project.objects.get(pk=instance.pk)
        if old_obj.cover_image and old_obj.cover_image != instance.cover_image:
            delete_file_safely(old_obj.cover_image)
    except Project.DoesNotExist:
        pass


@receiver(pre_save, sender=ProjectImage)
def cleanup_project_image_on_update(sender, instance, **kwargs):
    if instance.image:
        auto_optimize_image_field(instance.image, max_dim=1200, quality=82)

    if not instance.pk:
        return
    try:
        old_obj = ProjectImage.objects.get(pk=instance.pk)
        if old_obj.image and old_obj.image != instance.image:
            delete_file_safely(old_obj.image)
    except ProjectImage.DoesNotExist:
        pass


@receiver(pre_save, sender=Post)
def cleanup_post_on_update(sender, instance, **kwargs):
    if instance.cover_image:
        auto_optimize_image_field(instance.cover_image, max_dim=1600, quality=82)

    if not instance.pk:
        return
    try:
        old_obj = Post.objects.get(pk=instance.pk)
        if old_obj.cover_image and old_obj.cover_image != instance.cover_image:
            delete_file_safely(old_obj.cover_image)
    except Post.DoesNotExist:
        pass
