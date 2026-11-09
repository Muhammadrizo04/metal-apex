from urllib.parse import urlencode

from django.shortcuts import get_object_or_404, render

from .filters import filter_panels, parse_letter, parse_series
from .models import Accessory, Color, Panel, Pattern

MAX_SIBLINGS = 6


def _query(series, letter):
    params = {}
    if series is not None:
        params["naqsh"] = series
    if letter:
        params["rang"] = letter
    return "?" + urlencode(params) if params else "?"


def panel_list(request):
    naqsh, rang = request.GET.get("naqsh"), request.GET.get("rang")
    series, letter = parse_series(naqsh), parse_letter(rang)
    published = Panel.objects.published()
    panels = list(filter_panels(published, naqsh, rang).select_related("pattern", "color"))
    pattern_links = [
        {
            "series": p.series,
            "name": p.name,
            "on": p.series == series,
            "url": _query(None if p.series == series else p.series, letter),
        }
        for p in Pattern.objects.all()
    ]
    color_links = [
        {
            "letter": c.letter,
            "name": c.name,
            "hex": c.hex,
            "on": c.letter == letter,
            "url": _query(series, None if c.letter == letter else c.letter),
        }
        for c in Color.objects.filter(panels__is_published=True).distinct()
    ]
    context = {
        "panels": panels,
        "pattern_links": pattern_links,
        "color_links": color_links,
        "any_pattern_url": _query(None, letter),
        "no_pattern": series is None,
        "panel_total": published.count(),
    }
    template = "catalog/_grid.html" if request.headers.get("X-Requested-With") == "fetch" else "catalog/list.html"
    return render(request, template, context)


def accessories(request):
    return render(request, "catalog/accessories.html", {"items": Accessory.objects.filter(is_published=True)})


def detail(request, code):
    panel = get_object_or_404(Panel.objects.published().select_related("pattern", "color"), code__iexact=code)
    others = (
        Panel.objects.published().filter(pattern=panel.pattern).exclude(pk=panel.pk).select_related("color")
    )
    return render(
        request,
        "catalog/detail.html",
        {"panel": panel, "siblings": [panel, *others[: MAX_SIBLINGS - 1]]},
    )
