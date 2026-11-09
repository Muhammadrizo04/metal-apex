from django.test import TestCase

from apps.core.ui import UI


class FoundationTests(TestCase):
    def test_root_redirects_to_language(self):
        r = self.client.get("/", HTTP_ACCEPT_LANGUAGE="ru")
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r["Location"], "/ru/")

    def test_root_default_is_uz(self):
        r = self.client.get("/", HTTP_ACCEPT_LANGUAGE="en")
        self.assertEqual(r["Location"], "/uz/")

    def test_home_renders_nav_in_language(self):
        self.assertContains(self.client.get("/uz/"), "Mahsulotlar")
        self.assertContains(self.client.get("/ru/"), "Продукция")

    def test_ui_has_both_languages(self):
        for key, value in UI.items():
            self.assertEqual(set(value), {"uz", "ru"}, key)
