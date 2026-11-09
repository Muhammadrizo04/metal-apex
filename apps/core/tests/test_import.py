import re
import shutil
import tempfile
from io import StringIO
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import SimpleTestCase, TestCase, override_settings
from PIL import Image

from apps.catalog.models import Accessory, Color, Panel, Pattern
from apps.core.management.commands.import_wordpress import autop
from apps.core.models import AboutPage, Advantage, HomeContent, Layer, MontageStep, SiteSettings
from apps.core.wordpress.parser import parse_inserts, parse_panel_code, php_id_list, split_translations
from apps.projects.models import Project, Video

SQL_PATH = Path(__file__).parent / "fixtures" / "sample_dump.sql"
SQL = SQL_PATH.read_text(encoding="utf-8")


class ParserTests(SimpleTestCase):
    def test_parse_only_requested_tables(self):
        result = parse_inserts(SQL, {"mx_posts"})
        self.assertEqual(set(result), {"mx_posts"})
        self.assertNotIn("hash-qiymat", str(result))
        self.assertNotIn("MAXFIY-TOKEN", str(result))

    def test_parse_unescapes_quotes(self):
        rows = parse_inserts(SQL, {"mx_postmeta"})["mx_postmeta"]
        value = next(r["meta_value"] for r in rows if r["meta_key"] == "what_components_0_text_2")
        self.assertEqual(value, "[:uz]Po'lat plita[:ru]Стальной лист[:]")

    def test_parse_doubled_quote_and_null(self):
        sql = "INSERT INTO `t` (`a`, `b`, `c`) VALUES ('O''zbek', NULL, 5);"
        self.assertEqual(parse_inserts(sql, {"t"})["t"], [{"a": "O'zbek", "b": None, "c": 5}])

    def test_parse_parens_inside_string_do_not_split(self):
        rows = parse_inserts(SQL, {"mx_posts"})["mx_posts"]
        self.assertEqual(next(r for r in rows if r["ID"] == 204)["post_content"], "qavs ), ( ichida")

    def test_split_translations(self):
        self.assertEqual(split_translations("[:uz]a[:ru]b[:]"), ("a", "b"))

    def test_split_plain(self):
        self.assertEqual(split_translations("a"), ("a", "a"))

    def test_php_id_list(self):
        self.assertEqual(php_id_list('a:2:{i:0;s:2:"97";i:1;s:2:"60";}'), [97, 60])

    def test_panel_code(self):
        self.assertEqual(parse_panel_code("CH5-01"), ("CH", 5, "CH5-01"))
        self.assertEqual(parse_panel_code("Q3-101"), ("Q", 3, "Q3-101"))
        self.assertEqual(parse_panel_code("G3-01 ."), ("G", 3, "G3-01"))
        self.assertEqual(parse_panel_code("[:uz]T4-04[:ru]T4-04[:]"), ("T", 4, "T4-04"))
        self.assertIsNone(parse_panel_code("наружный угол"))


class AutopTests(SimpleTestCase):
    def test_plain_paragraphs(self):
        self.assertEqual(autop("a\r\n\r\nb"), "<p>a</p>\n<p>b</p>")

    def test_text_before_list_stays_separate(self):
        self.assertEqual(autop("Sarlavha:\n<ol>\n<li>a</li>\n</ol>"), "<p>Sarlavha:</p>\n<ol>\n<li>a</li>\n</ol>")

    def test_nbsp_block_dropped(self):
        self.assertEqual(autop("a\n\n&nbsp;\n\nb"), "<p>a</p>\n<p>b</p>")

    def test_inline_style_removed(self):
        self.assertEqual(autop('<h3 style="text-align: center;">x</h3>'), "<h3>x</h3>")


class ImportCommandTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tmp = Path(tempfile.mkdtemp())
        cls.uploads = cls.tmp / "uploads"
        for rel in re.findall(r"'_wp_attached_file', '([^']+)'", SQL):
            if rel.endswith("yoq.png"):
                continue
            path = cls.uploads / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            Image.new("RGB", (40, 30), "gray").save(path)
        cls.media = cls.tmp / "media"
        cls.override = override_settings(MEDIA_ROOT=cls.media)
        cls.override.enable()

    @classmethod
    def tearDownClass(cls):
        cls.override.disable()
        shutil.rmtree(cls.tmp, ignore_errors=True)
        super().tearDownClass()

    def run_import(self):
        out = StringIO()
        call_command("import_wordpress", sql=str(SQL_PATH), uploads=str(self.uploads), stdout=out)
        return out.getvalue()

    def test_import_counts_and_duplicate(self):
        self.run_import()
        self.assertEqual(Panel.objects.count(), 6)
        self.assertEqual(Accessory.objects.count(), 2)
        self.assertTrue(Panel.objects.get(code="G3-01").is_published)
        self.assertFalse(Panel.objects.get(code="G3-01-2").is_published)

    def test_import_links_pattern_and_color(self):
        self.run_import()
        panel = Panel.objects.get(code="CH5-01")
        self.assertEqual(panel.pattern.series, 5)
        self.assertEqual(panel.color.letter, "CH")
        self.assertEqual(Pattern.objects.count(), 6)
        self.assertEqual(Color.objects.get(letter="E").name_uz, "Bej")

    def test_accessory_name_cleaned(self):
        self.run_import()
        self.assertEqual(set(Accessory.objects.values_list("name_ru", flat=True)), {"наружный угол"})

    def test_import_translations_and_inlines(self):
        self.run_import()
        self.assertEqual(Layer.objects.get().title_ru, "Внешний слой")
        self.assertEqual(Advantage.objects.get().title_uz, "Engil vazn")
        self.assertEqual(MontageStep.objects.get().text_ru, "Профиль")
        self.assertEqual(HomeContent.load().layers_kicker_ru, "Что такое Metal Apex?")

    def test_settings_and_about_imported(self):
        self.run_import()
        site = SiteSettings.load()
        self.assertEqual(site.phone_1, "+998 93 503 23 23")
        self.assertEqual(site.phone_2, "+998 94 447 77 17")
        self.assertEqual(site.address_uz, "Qo'qon, Temura Malik ko'chasi, 79A")
        self.assertIn("yandex", site.map_url)
        self.assertEqual(str(site.foam_mm), "16")
        about = AboutPage.load()
        self.assertEqual(about.title_ru, "О продукции")
        self.assertIn("<p>Первый абзац.</p>", about.body_ru)

    def test_hero_and_montage_images(self):
        self.run_import()
        home = HomeContent.load()
        self.assertTrue(home.hero_image)
        self.assertIn("1", Path(home.hero_image.name).stem)
        self.assertTrue(home.montage_image)

    def test_projects_unique_and_unverified_photos_hidden(self):
        self.run_import()
        self.assertEqual(Project.objects.count(), 4)
        self.assertEqual(set(Project.objects.filter(is_published=False).values_list("wp_id", flat=True)), {202, 205})

    def test_video_imported(self):
        self.run_import()
        self.assertEqual(Video.objects.get().youtube_id, "CAGMRjMMQxI")

    def test_import_idempotent(self):
        self.run_import()
        self.run_import()
        self.assertEqual(Panel.objects.count(), 6)
        self.assertEqual(Accessory.objects.count(), 2)
        self.assertEqual(Project.objects.count(), 4)
        self.assertEqual(Layer.objects.count(), 1)

    def test_reimport_keeps_admin_edits(self):
        self.run_import()
        Panel.objects.filter(code="A1-02").update(description_uz="tahrir")
        HomeContent.objects.filter(pk=1).update(hero_title_uz="Yangi")
        self.run_import()
        self.assertEqual(Panel.objects.get(code="A1-02").description_uz, "tahrir")
        self.assertEqual(HomeContent.load().hero_title_uz, "Yangi")

    def test_missing_file_skipped_and_reported(self):
        output = self.run_import()
        self.assertFalse(Panel.objects.filter(code="Z6-01").exists())
        self.assertIn("2024/07/yoq.png", output)

    def test_no_users_imported(self):
        self.run_import()
        self.assertEqual(get_user_model().objects.count(), 0)
