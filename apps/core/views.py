from django.http import HttpResponse
from django.shortcuts import render

from apps.catalog.models import Panel, Pattern
from apps.core.models import AboutPage, HomeContent
from apps.leads.forms import LeadForm
from apps.projects.models import Partner, Project, Video


def home(request):
    content = HomeContent.load()
    published = Panel.objects.published().select_related("pattern", "color")
    panel_total = published.count()
    stats = list(content.stats.all())
    for stat in stats:
        stat.display = str(panel_total) if stat.auto_panel_count else stat.value
    return render(
        request,
        "core/home.html",
        {
            "home": content,
            "stats": stats,
            "layers": content.layers.all(),
            "advantages": content.advantages.all(),
            "montage_steps": content.montage_steps.all(),
            "panels": list(published[:4]),
            "layer_panel": published.first(),
            "panel_total": panel_total,
            "patterns": Pattern.objects.all(),
            "projects": list(Project.objects.filter(is_published=True)[:5]),
            "videos": [v for v in Video.objects.all() if v.youtube_id],
            "partners": Partner.objects.all(),
            "lead_form": LeadForm(),
        },
    )


def about(request):
    return render(request, "core/about.html", {"about": AboutPage.load(), "lead_form": LeadForm()})


def contact(request):
    return render(request, "core/contact.html", {"lead_form": LeadForm()})


def robots(request):
    sitemap = request.build_absolute_uri("/sitemap.xml")
    lines = ["User-agent: *", "Disallow: /boshqaruv/", "Disallow: /uz/buyurtma/", "Disallow: /ru/buyurtma/", f"Sitemap: {sitemap}"]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain")
