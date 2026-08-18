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
# Pre-Save File Cleaners (Delete Replaced Files)
# ==========================================
@receiver(pre_save, sender=SiteSettings)
def cleanup_sitesettings_on_update(sender, instance, **kwargs):
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
    if not instance.pk:
        return
    try:
        old_obj = PageHero.objects.get(pk=instance.pk)
        if old_obj.hero_image and old_obj.hero_image != instance.hero_image:
            delete_file_safely(old_obj.hero_image)
    except PageHero.DoesNotExist:
        pass


@receiver(pre_save, sender=Project)
def cleanup_project_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_obj = Project.objects.get(pk=instance.pk)
        if old_obj.cover_image and old_obj.cover_image != instance.cover_image:
            delete_file_safely(old_obj.cover_image)
    except Project.DoesNotExist:
        pass


@receiver(pre_save, sender=Post)
def cleanup_post_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_obj = Post.objects.get(pk=instance.pk)
        if old_obj.cover_image and old_obj.cover_image != instance.cover_image:
            delete_file_safely(old_obj.cover_image)
    except Post.DoesNotExist:
        pass
