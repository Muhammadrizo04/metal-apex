import io

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from apps.catalog.models import Accessory, Color, Panel, Pattern
from apps.core.models import SiteSettings
from apps.core.tests.utils import MediaTestCase, image_file


class CatalogTests(MediaTestCase):
    def setUp(self):
        self.stone = Pattern.objects.create(series=5, name_uz="Yirik tosh", order=5)
        self.line = Pattern.objects.create(series=6, name_uz="Chiziqli", order=6)
        self.beige = Color.objects.create(letter="E", name_uz="Bej", hex="#d8cdb8")
        self.black = Color.objects.create(letter="A", name_uz="Antratsit", hex="#2b2e33")
        self.unused = Color.objects.create(letter="Z", name_uz="Zaytun", hex="#8b8a70")
        self.e5 = self.make("E5-01", self.stone, self.beige)
        self.a5 = self.make("A5-01", self.stone, self.black)
        self.a6 = self.make("A6-01", self.line, self.black)
        self.ch = self.make("CH5-01", self.stone, None)
        self.hidden = self.make("G3-01-2", self.stone, self.beige, is_published=False)

    def make(self, code, pattern, color, **kwargs):
        return Panel.objects.create(code=code, pattern=pattern, color=color, image=image_file(), **kwargs)

    def codes(self, **params):
        return {p.code for p in self.client.get("/uz/katalog/", params).context["panels"]}

    def test_all_published(self):
        self.assertEqual(self.codes(), {"E5-01", "A5-01", "A6-01", "CH5-01"})

    def test_filter_by_pattern(self):
        self.assertEqual(self.codes(naqsh="6"), {"A6-01"})

    def test_filter_by_color(self):
        self.assertEqual(self.codes(rang="A"), {"A5-01", "A6-01"})

    def test_filter_by_both(self):
        self.assertEqual(self.codes(naqsh="5", rang="A"), {"A5-01"})

    def test_filter_ignores_garbage(self):
        response = self.client.get("/uz/katalog/", {"naqsh": "abc", "rang": "<script>alert(1)</script>"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["panels"]), 4)
        self.assertNotContains(response, "<script>alert")

    def test_huge_pattern_number_is_ignored(self):
        self.assertEqual(self.client.get("/uz/katalog/", {"naqsh": "9" * 40}).status_code, 200)

    def test_hidden_panel_absent_and_404(self):
        self.assertNotContains(self.client.get("/uz/katalog/"), "G3-01-2")
        self.assertEqual(self.client.get("/uz/katalog/g3-01-2/").status_code, 404)

    def test_detail_case_insensitive(self):
        self.assertEqual(self.client.get("/uz/katalog/e5-01/").status_code, 200)
        self.assertEqual(self.client.get("/uz/katalog/E5-01/").status_code, 200)

    def test_detail_two_letter_code(self):
        self.assertEqual(self.client.get("/uz/katalog/ch5-01/").status_code, 200)

    def test_detail_shows_specs(self):
        site = SiteSettings.load()
        site.metal_mm, site.foam_mm, site.weight_kg_m2, site.lifetime_years = "0.30", 16, "3.8", 50
        site.save()
        response = self.client.get("/uz/katalog/e5-01/")
        for text in ("0,3 mm", "16 mm", "3,8 kg/m²", "50 yilgacha"):
            self.assertContains(response, text)

    def test_detail_siblings_same_pattern_current_first(self):
        for i in range(8):
            self.make(f"X5-0{i}", self.stone, None)
        siblings = self.client.get("/uz/katalog/e5-01/").context["siblings"]
        self.assertEqual(siblings[0].code, "E5-01")
        self.assertEqual(len(siblings), 6)
        self.assertTrue(all(p.pattern == self.stone and p.is_published for p in siblings))

    def test_optional_dimensions_hidden_when_empty(self):
        self.assertNotContains(self.client.get("/uz/katalog/e5-01/"), "Uzunligi")
        Panel.objects.filter(pk=self.e5.pk).update(length_mm=3800)
        self.assertContains(self.client.get("/uz/katalog/e5-01/"), "Uzunligi")

    def test_ajax_returns_fragment_only(self):
        response = self.client.get("/uz/katalog/", {"naqsh": "6"}, HTTP_X_REQUESTED_WITH="fetch")
        self.assertNotContains(response, "<html")
        self.assertContains(response, "A6-01")

    def test_fragment_and_page_vary_by_request_header(self):
        for headers in ({}, {"HTTP_X_REQUESTED_WITH": "fetch"}):
            self.assertIn("X-Requested-With", self.client.get("/uz/katalog/", **headers)["Vary"])

    def test_phone_photo_orientation_applied(self):
        buffer = io.BytesIO()
        exif = Image.Exif()
        exif[0x0112] = 6
        Image.new("RGB", (400, 200), "gray").save(buffer, "JPEG", exif=exif)
        panel = Panel.objects.create(
            code="Y1-01", pattern=self.stone, image=SimpleUploadedFile("telefon.jpg", buffer.getvalue())
        )
        panel.image_card.generate()
        with panel.image_card.storage.open(panel.image_card.name) as handle:
            self.assertEqual(Image.open(handle).size, (200, 400))

    def test_swatch_caption_not_below_minimum_font(self):
        css = (settings.BASE_DIR / "static/css/site.css").read_text(encoding="utf-8")
        self.assertRegex(css, r"\.sw a \{[^}]*font-size: 14px")

    def test_only_used_colors_listed(self):
        colors = self.client.get("/uz/katalog/").context["color_links"]
        self.assertEqual({c["letter"] for c in colors}, {"E", "A"})

    def test_filter_links_keep_other_filter(self):
        links = self.client.get("/uz/katalog/", {"rang": "A"}).context["pattern_links"]
        self.assertIn("rang=A", next(p for p in links if p["series"] == 5)["url"])

    def test_accessories_page(self):
        Accessory.objects.create(name_uz="Burchak", image=image_file())
        Accessory.objects.create(name_uz="Yashirin", image=image_file(), is_published=False)
        response = self.client.get("/uz/katalog/aksessuarlar/")
        self.assertContains(response, "Burchak")
        self.assertNotContains(response, "Yashirin")
