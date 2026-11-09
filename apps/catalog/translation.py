from modeltranslation.translator import TranslationOptions, register

from .models import Accessory, Color, Panel, Pattern


@register(Pattern)
class PatternTR(TranslationOptions):
    fields = ("name",)


@register(Color)
class ColorTR(TranslationOptions):
    fields = ("name",)


@register(Panel)
class PanelTR(TranslationOptions):
    fields = ("description",)


@register(Accessory)
class AccessoryTR(TranslationOptions):
    fields = ("name",)
