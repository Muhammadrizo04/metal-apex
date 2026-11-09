import re

from django import forms
from django.utils.translation import get_language

from apps.core.ui import UI

from .models import Lead

_PHONE = re.compile(r"^\+?[\d\s()\-]{7,20}$")
MIN_PHONE_DIGITS = 9


class LeadForm(forms.ModelForm):
    panel_code = forms.CharField(required=False, max_length=20, widget=forms.HiddenInput)
    website = forms.CharField(required=False)

    class Meta:
        model = Lead
        fields = ["name", "phone", "company", "panel_code"]

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        digits = sum(c.isdigit() for c in phone)
        if not _PHONE.match(phone) or digits < MIN_PHONE_DIGITS:
            lang = (get_language() or "uz")[:2]
            raise forms.ValidationError(UI["err_phone"].get(lang, UI["err_phone"]["uz"]))
        return phone
