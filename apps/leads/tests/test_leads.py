from unittest.mock import Mock, patch

import requests
from django.contrib.auth import get_user_model
from django.db import OperationalError
from django.test import Client, TestCase, override_settings

from apps.catalog.models import Panel, Pattern
from apps.leads.forms import LeadForm
from apps.leads.models import Lead

URL = "/uz/buyurtma/"
THANKS = "/uz/buyurtma/qabul/"
VALID = {"name": "Ali", "phone": "+998 90 123-45-67", "company": "Qurilish"}


def ok_response():
    return Mock(status_code=200)


@override_settings(TELEGRAM_BOT_TOKEN="123:SECRET", TELEGRAM_CHAT_ID="-100")
@patch("apps.leads.telegram.requests.post")
class LeadTests(TestCase):
    def setUp(self):
        pattern = Pattern.objects.create(series=5, name_uz="Yirik tosh")
        self.panel = Panel.objects.create(code="E5-01", pattern=pattern, image="p.png")

    def test_valid_saves_sends_and_redirects(self, post):
        post.return_value = ok_response()
        response = self.client.post(URL, VALID)
        self.assertRedirects(response, THANKS, fetch_redirect_response=False)
        lead = Lead.objects.get()
        self.assertEqual((lead.name, lead.status, lead.language), ("Ali", "new", "uz"))
        self.assertTrue(lead.telegram_sent)

    def test_message_text(self, post):
        post.return_value = ok_response()
        self.client.post(URL, {**VALID, "panel_code": "E5-01"})
        args, kwargs = post.call_args
        self.assertEqual(args[0], "https://api.telegram.org/bot123:SECRET/sendMessage")
        self.assertEqual(kwargs["timeout"], 5)
        self.assertEqual(kwargs["json"]["chat_id"], "-100")
        self.assertNotIn("parse_mode", kwargs["json"])
        for line in ("Yangi buyurtma", "Ism: Ali", "Telefon: +998 90 123-45-67", "Kompaniya: Qurilish", "Panel: E5-01", "Til: uz"):
            self.assertIn(line, kwargs["json"]["text"])

    def test_phone_formats(self, post):
        for good in ("+998 90 123-45-67", "901234567", "(90) 123 45 67"):
            self.assertTrue(LeadForm({"name": "A", "phone": good}).is_valid(), good)
        for bad in ("salom", "123", "+998abc4567"):
            self.assertFalse(LeadForm({"name": "A", "phone": bad}).is_valid(), bad)

    def test_invalid_keeps_values_and_shows_error(self, post):
        response = self.client.post(URL, {"name": "Valijon", "phone": "salom"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Valijon")
        self.assertContains(response, 'class="err"')
        self.assertEqual(Lead.objects.count(), 0)
        post.assert_not_called()

    def test_honeypot_silent(self, post):
        response = self.client.post(URL, {**VALID, "website": "http://spam.uz"})
        self.assertRedirects(response, THANKS, fetch_redirect_response=False)
        self.assertEqual(Lead.objects.count(), 0)
        post.assert_not_called()

    def test_throttle(self, post):
        post.return_value = ok_response()
        for _ in range(5):
            self.assertEqual(self.client.post(URL, VALID).status_code, 302)
        response = self.client.post(URL, VALID)
        self.assertEqual(response.status_code, 429)
        self.assertContains(response, 'class="err"', status_code=429)
        self.assertEqual(Lead.objects.count(), 5)

    @override_settings(TRUST_PROXY=True)
    def test_throttle_separates_clients_behind_proxy(self, post):
        post.return_value = ok_response()
        for i in range(6):
            r = self.client.post(URL, VALID, HTTP_X_FORWARDED_FOR=f"10.0.0.{i}")
            self.assertEqual(r.status_code, 302)

    def test_cache_failure_does_not_lose_lead(self, post):
        post.return_value = ok_response()
        with patch("apps.leads.throttle.cache.get", side_effect=OperationalError("no such table")):
            response = self.client.post(URL, VALID)
        self.assertRedirects(response, THANKS, fetch_redirect_response=False)
        self.assertEqual(Lead.objects.count(), 1)

    def test_telegram_failure_still_succeeds(self, post):
        post.side_effect = requests.ConnectionError("xato")
        self.assertRedirects(self.client.post(URL, VALID), THANKS, fetch_redirect_response=False)
        lead = Lead.objects.get()
        self.assertFalse(lead.telegram_sent)
        self.assertEqual(lead.telegram_error, "ConnectionError")

    def test_http_error_recorded(self, post):
        post.return_value = Mock(status_code=403)
        self.client.post(URL, VALID)
        self.assertEqual(Lead.objects.get().telegram_error, "HTTP 403")

    def test_error_never_contains_token(self, post):
        post.side_effect = requests.ConnectionError("https://api.telegram.org/bot123:SECRET/sendMessage")
        self.client.post(URL, VALID)
        self.assertNotIn("SECRET", Lead.objects.get().telegram_error)

    @override_settings(TELEGRAM_BOT_TOKEN="", TELEGRAM_CHAT_ID="")
    def test_unconfigured_telegram(self, post):
        self.assertRedirects(self.client.post(URL, VALID), THANKS, fetch_redirect_response=False)
        self.assertFalse(Lead.objects.get().telegram_sent)
        post.assert_not_called()

    def test_panel_linked_case_insensitive(self, post):
        post.return_value = ok_response()
        self.client.post(URL, {**VALID, "panel_code": "e5-01"})
        lead = Lead.objects.get()
        self.assertEqual((lead.panel, lead.panel_code), (self.panel, "E5-01"))

    def test_unknown_panel_code(self, post):
        post.return_value = ok_response()
        self.client.post(URL, {**VALID, "panel_code": "YOQ-1"})
        lead = Lead.objects.get()
        self.assertIsNone(lead.panel)
        self.assertEqual(lead.panel_code, "")

    def test_panel_code_snapshot_survives_delete(self, post):
        post.return_value = ok_response()
        self.client.post(URL, {**VALID, "panel_code": "E5-01"})
        self.panel.delete()
        lead = Lead.objects.get()
        self.assertIsNone(lead.panel)
        self.assertEqual(lead.panel_code, "E5-01")

    def test_admin_resend_action(self, post):
        post.return_value = ok_response()
        lead = Lead.objects.create(name="A", phone="901234567")
        self.client.force_login(get_user_model().objects.create_superuser("a", "a@a.uz", "uzun-parol-123456"))
        self.client.post(
            "/boshqaruv/leads/lead/", {"action": "resend_telegram", "_selected_action": [lead.pk]}, follow=True
        )
        lead.refresh_from_db()
        self.assertTrue(lead.telegram_sent)

    def test_csrf_enforced(self, post):
        self.assertEqual(Client(enforce_csrf_checks=True).post(URL, VALID).status_code, 403)

    def test_get_not_allowed(self, post):
        self.assertEqual(self.client.get(URL).status_code, 405)

    def test_thanks_page(self, post):
        self.assertEqual(self.client.get(THANKS).status_code, 200)


class LeadFormRenderTests(TestCase):
    def test_home_has_form(self):
        response = self.client.get("/uz/")
        self.assertContains(response, 'id="buyurtma"')
        self.assertContains(response, 'action="/uz/buyurtma/"')

    def test_panel_page_form_has_code(self):
        pattern = Pattern.objects.create(series=5, name_uz="Yirik tosh")
        Panel.objects.create(code="E5-01", pattern=pattern, image="p.png")
        self.assertContains(self.client.get("/uz/katalog/e5-01/"), 'name="panel_code" value="E5-01"')
