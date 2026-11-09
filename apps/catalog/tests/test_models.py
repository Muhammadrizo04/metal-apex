from django.test import TestCase
from django.utils import translation

from apps.catalog.models import Color, Panel, Pattern


class PanelModelTests(TestCase):
    def setUp(self):
        self.pattern = Pattern.objects.create(series=5, name_uz="Yirik tosh", order=5)
        self.panel = Panel.objects.create(code="E5-01", pattern=self.pattern, image="p/e.webp")

    def test_panel_url_is_lowercase(self):
        with translation.override("uz"):
            self.assertEqual(self.panel.get_absolute_url(), "/uz/katalog/e5-01/")

    def test_published_excludes_hidden(self):
        Panel.objects.create(code="G3-01-2", pattern=self.pattern, image="p/g.webp", is_published=False)
        self.assertEqual(list(Panel.objects.published()), [self.panel])

    def test_translation_falls_back_to_uz(self):
        with translation.override("ru"):
            self.assertEqual(Pattern.objects.get(pk=self.pattern.pk).name, "Yirik tosh")

    def test_color_letter_unique_key(self):
        Color.objects.create(letter="E", name_uz="Bej", hex="#d8cdb8")
        self.assertEqual(Color.objects.get(letter="E").hex, "#d8cdb8")
