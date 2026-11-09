from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin

from .models import Accessory, Color, Panel, Pattern


def _thumb(obj):
    if not obj.image:
        return ""
    return format_html('<img src="{}" alt="" style="height:48px">', obj.image.url)


@admin.register(Pattern)
class PatternAdmin(TranslationAdmin):
    list_display = ["series", "name", "order"]


@admin.register(Color)
class ColorAdmin(TranslationAdmin):
    list_display = ["letter", "name", "hex", "order"]


@admin.register(Panel)
class PanelAdmin(TranslationAdmin):
    list_display = ["thumb", "code", "pattern", "color", "is_published"]
    list_display_links = ["thumb", "code"]
    list_filter = ["pattern", "color", "is_published"]
    search_fields = ["code"]

    @admin.display(description="Rasm")
    def thumb(self, obj):
        return _thumb(obj)


@admin.register(Accessory)
class AccessoryAdmin(TranslationAdmin):
    list_display = ["thumb", "name", "is_published", "order"]
    list_display_links = ["thumb", "name"]

    @admin.display(description="Rasm")
    def thumb(self, obj):
        return _thumb(obj)
