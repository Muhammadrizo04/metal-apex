from modeltranslation.translator import TranslationOptions, register

from .models import Project, Video


@register(Project)
class ProjectTR(TranslationOptions):
    fields = ("title", "city")


@register(Video)
class VideoTR(TranslationOptions):
    fields = ("title",)
