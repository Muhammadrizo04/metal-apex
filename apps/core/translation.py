from modeltranslation.translator import TranslationOptions, register

from .models import AboutPage, Advantage, HomeContent, Layer, MontageStep, SiteSettings, Stat


@register(SiteSettings)
class SiteSettingsTR(TranslationOptions):
    fields = ("address",)


@register(HomeContent)
class HomeContentTR(TranslationOptions):
    fields = (
        "hero_kicker", "hero_title", "hero_text", "layers_kicker", "layers_title", "adv_kicker", "adv_title",
        "catalog_kicker", "catalog_title", "projects_kicker", "projects_title", "videos_kicker", "videos_title",
        "montage_kicker", "montage_title", "partners_title", "form_kicker", "form_title",
    )


@register(Layer)
class LayerTR(TranslationOptions):
    fields = ("title", "text")


@register(Advantage)
class AdvantageTR(TranslationOptions):
    fields = ("title", "text")


@register(MontageStep)
class MontageStepTR(TranslationOptions):
    fields = ("title", "text")


@register(Stat)
class StatTR(TranslationOptions):
    fields = ("value", "title")


@register(AboutPage)
class AboutPageTR(TranslationOptions):
    fields = ("title", "body")
