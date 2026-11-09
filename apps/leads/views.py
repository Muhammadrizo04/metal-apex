from django.shortcuts import redirect, render
from django.utils.translation import get_language
from django.views.decorators.http import require_POST

from apps.catalog.models import Panel
from apps.core.ui import UI

from .forms import LeadForm
from .telegram import deliver
from .throttle import client_ip, is_throttled


def _form_page(request, form, status=200):
    return render(request, "leads/form_page.html", {"lead_form": form}, status=status)


@require_POST
def submit(request):
    if request.POST.get("website"):
        return redirect("leads:thanks")
    form = LeadForm(request.POST)
    if not form.is_valid():
        return _form_page(request, form)
    lang = (get_language() or "uz")[:2]
    if is_throttled(client_ip(request)):
        form.add_error(None, UI["err_throttle"].get(lang, UI["err_throttle"]["uz"]))
        return _form_page(request, form, status=429)
    lead = form.save(commit=False)
    code = form.cleaned_data.get("panel_code", "").strip()
    lead.panel = Panel.objects.filter(code__iexact=code).first() if code else None
    lead.panel_code = lead.panel.code if lead.panel else ""
    lead.source_url = request.META.get("HTTP_REFERER", "")[:500]
    lead.language = lang
    lead.save()
    deliver(lead)
    return redirect("leads:thanks")


def thanks(request):
    return render(request, "leads/thanks.html")
