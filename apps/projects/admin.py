from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Partner, Project, Video


@admin.register(Project)
class ProjectAdmin(TranslationAdmin):
    list_display = ["__str__", "city", "is_published", "order"]
    list_filter = ["is_published"]


@admin.register(Video)
class VideoAdmin(TranslationAdmin):
    list_display = ["__str__", "order"]


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ["name", "order"]
