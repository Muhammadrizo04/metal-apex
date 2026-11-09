from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from django.views.static import serve

from apps.core.sitemaps import PanelSitemap, StaticSitemap
from apps.core.views import robots

OLD_PAGES = {
    "products": "katalog/",
    "works": "loyihalar/",
    "about": "mahsulot-haqida/",
    "contact": "aloqa/",
    "glavnaya": "",
}

urlpatterns = [
    path("boshqaruv/", admin.site.urls),
    path("robots.txt", robots),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {"pages": StaticSitemap, "panels": PanelSitemap}},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

for old, new in OLD_PAGES.items():
    urlpatterns += [
        path(f"{old}/", RedirectView.as_view(url=f"/uz/{new}", permanent=True)),
        path(f"ru/{old}/", RedirectView.as_view(url=f"/ru/{new}", permanent=True)),
    ]

if settings.DEBUG or settings.SERVE_MEDIA:
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    ]

urlpatterns += i18n_patterns(
    path("", include("apps.core.urls")),
    path("", include("apps.catalog.urls")),
    path("", include("apps.leads.urls")),
    path("", include("apps.projects.urls")),
    prefix_default_language=True,
)
