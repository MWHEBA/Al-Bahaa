from django.core.cache import cache
from django.db.utils import OperationalError, ProgrammingError

from apps.projects.models import ProjectCategory
from .models import PageHero, SiteSettings


def site_settings(request):
    try:
        settings_obj = cache.get("site_settings_cached")
        if settings_obj is None:
            settings_obj = SiteSettings.load()
            cache.set("site_settings_cached", settings_obj, 3600)

        heroes_map = cache.get("page_heroes_cached")
        if heroes_map is None:
            heroes_map = {hero.page: hero for hero in PageHero.objects.all()}
            cache.set("page_heroes_cached", heroes_map, 3600)

        footer_categories = cache.get("footer_categories_cached")
        if footer_categories is None:
            footer_categories = list(ProjectCategory.objects.all()[:5])
            cache.set("footer_categories_cached", footer_categories, 3600)

    except (OperationalError, ProgrammingError):
        settings_obj = None
        heroes_map = {}
        footer_categories = []

    return {
        "site_settings": settings_obj,
        "page_heroes": heroes_map,
        "footer_categories": footer_categories,
    }
