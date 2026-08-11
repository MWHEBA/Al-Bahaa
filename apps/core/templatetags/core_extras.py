from django import template

from apps.core.models import ClientLogo, SiteSettings, Testimonial

register = template.Library()


@register.simple_tag
def get_site_settings():
    return SiteSettings.load()


@register.simple_tag
def get_client_logos():
    return ClientLogo.objects.all()


@register.simple_tag
def get_featured_testimonials():
    return Testimonial.objects.filter(is_featured=True)
