from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

from .models import AboutPage, Advantage, HomeContent, Layer, MontageStep, SiteSettings, Stat

admin.site.site_header = "Metal Apex boshqaruvi"
admin.site.site_title = "Metal Apex"
admin.site.index_title = "Sayt kontenti"


class SingletonAdmin(TranslationAdmin):
    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


class StatInline(TranslationTabularInline):
    model = Stat
    extra = 0


class LayerInline(TranslationTabularInline):
    model = Layer
    extra = 0


class AdvantageInline(TranslationTabularInline):
    model = Advantage
    extra = 0


class MontageStepInline(TranslationTabularInline):
    model = MontageStep
    extra = 0


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    pass


@admin.register(HomeContent)
class HomeContentAdmin(SingletonAdmin):
    inlines = [StatInline, LayerInline, AdvantageInline, MontageStepInline]


@admin.register(AboutPage)
class AboutPageAdmin(SingletonAdmin):
    pass
