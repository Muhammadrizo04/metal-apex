from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase, TestCase

from apps.core.ui import UI
from config.settings import absolute_sqlite


class VideoEmbedTests(SimpleTestCase):
    def test_embed_sends_referrer_youtube_requires(self):
        script = (settings.BASE_DIR / "static/js/site.js").read_text(encoding="utf-8")
        self.assertIn('frame.referrerPolicy = "strict-origin-when-cross-origin"', script)


class DatabasePathTests(SimpleTestCase):
    def test_relative_sqlite_is_anchored_to_project(self):
        db = {"ENGINE": "django.db.backends.sqlite3", "NAME": "db.sqlite3"}
        self.assertEqual(absolute_sqlite(db, Path("D:/loyiha"))["NAME"], str(Path("D:/loyiha/db.sqlite3")))

    def test_absolute_sqlite_unchanged(self):
        name = str(Path("D:/boshqa/db.sqlite3"))
        db = {"ENGINE": "django.db.backends.sqlite3", "NAME": name}
        self.assertEqual(absolute_sqlite(db, Path("D:/loyiha"))["NAME"], name)

    def test_other_engines_unchanged(self):
        db = {"ENGINE": "django.db.backends.mysql", "NAME": "metal"}
        self.assertEqual(absolute_sqlite(db, Path("D:/loyiha"))["NAME"], "metal")


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

    def test_page_declares_icon(self):
        self.assertContains(self.client.get("/uz/"), 'rel="icon"')

    def test_ui_has_both_languages(self):
        for key, value in UI.items():
            self.assertEqual(set(value), {"uz", "ru"}, key)
