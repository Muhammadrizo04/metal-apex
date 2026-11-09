from django import template
from django.urls import translate_url
from django.utils.translation import get_language

from apps.core.ui import UI

register = template.Library()


@register.simple_tag
def t(key):
    lang = (get_language() or "uz")[:2]
    return UI[key].get(lang) or UI[key]["uz"]


@register.simple_tag(takes_context=True)
def lang_url(context, lang):
    return translate_url(context["request"].get_full_path(), lang)
