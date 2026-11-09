from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.catalog.models import Panel


class StaticSitemap(Sitemap):
    i18n = True
    languages = ["uz", "ru"]

    def items(self):
        return ["core:home", "catalog:list", "catalog:accessories", "projects:list", "core:about", "core:contact"]

    def location(self, item):
        return reverse(item)


class PanelSitemap(Sitemap):
    i18n = True
    languages = ["uz", "ru"]

    def items(self):
        return Panel.objects.published().order_by("pk")

    def location(self, item):
        return item.get_absolute_url()
