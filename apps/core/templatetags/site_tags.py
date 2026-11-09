from django import template
from django.urls import translate_url
from django.utils.translation import get_language

from apps.core.ui import UI

register = template.Library()


@register.simple_tag
def t(key, **kwargs):
    lang = (get_language() or "uz")[:2]
    text = UI[key].get(lang) or UI[key]["uz"]
    return text.format(**kwargs) if kwargs else text


@register.simple_tag(takes_context=True)
def lang_url(context, lang):
    return translate_url(context["request"].get_full_path(), lang)


@register.filter
def num(value):
    """0.30 -> 0,3"""
    if value in (None, ""):
        return ""
    return f"{float(value):g}".replace(".", ",")


@register.simple_tag
def spec_url(spec):
    """Rasm fayli yo'q yoki buzilgan bo'lsa sahifa yiqilmasligi uchun bo'sh qiymat qaytaradi."""
    try:
        return spec.url
    except (OSError, ValueError):
        return ""
