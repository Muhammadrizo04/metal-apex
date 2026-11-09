from apps.catalog.models import Panel, Pattern
from apps.core.models import HomeContent, Layer, Stat
from apps.core.tests.utils import MediaTestCase, image_file
from apps.projects.models import Partner, Project, Video


class HomeEmptyTests(MediaTestCase):
    def test_empty_database_renders(self):
        for lang in ("uz", "ru"):
            self.assertEqual(self.client.get(f"/{lang}/").status_code, 200)

    def test_empty_sections_hidden(self):
        response = self.client.get("/uz/")
        for section in ("hamkorlar", "videolar", "loyihalar", "katalog-namuna"):
            self.assertNotContains(response, f'id="{section}"')

    def test_layers_without_published_panels_render(self):
        Layer.objects.create(home=HomeContent.load(), title="Tashqi qatlam")
        self.assertEqual(self.client.get("/uz/").status_code, 200)

    def test_missing_image_file_does_not_crash(self):
        pattern = Pattern.objects.create(series=1, name_uz="A")
        Panel.objects.create(code="A1-01", pattern=pattern, image="panels/yoq.png")
        self.assertEqual(self.client.get("/uz/").status_code, 200)


class HomeContentTests(MediaTestCase):
    def setUp(self):
        self.pattern = Pattern.objects.create(series=5, name_uz="Yirik tosh")

    def make_panels(self, count, **kwargs):
        for i in range(count):
            Panel.objects.create(
                code=f"E5-{kwargs.get('prefix', '')}{i}", pattern=self.pattern, image=image_file(),
                is_published=kwargs.get("published", True),
            )

    def test_partners_shown_when_present(self):
        Partner.objects.create(name="X", logo=image_file())
        self.assertContains(self.client.get("/uz/"), 'id="hamkorlar"')

    def test_auto_stat_counts_published_only(self):
        self.make_panels(2)
        self.make_panels(1, prefix="y", published=False)
        Stat.objects.create(home=HomeContent.load(), title="panel", auto_panel_count=True)
        self.assertEqual(self.client.get("/uz/").context["stats"][0].display, "2")

    def test_sample_shows_four_panels_with_total(self):
        self.make_panels(5)
        response = self.client.get("/uz/")
        self.assertEqual(len(response.context["panels"]), 4)
        self.assertContains(response, "Barcha 5 panel")

    def test_russian_content(self):
        home = HomeContent.load()
        home.hero_title_uz = "Sarlavha"
        home.hero_title_ru = "Заголовок"
        home.save()
        self.assertContains(self.client.get("/ru/"), "Заголовок")

    def test_video_loads_only_on_click(self):
        Video.objects.create(url="https://youtu.be/CAGMRjMMQxI")
        response = self.client.get("/uz/")
        self.assertContains(response, 'data-youtube-id="CAGMRjMMQxI"')
        self.assertNotContains(response, "<iframe")

    def test_only_published_projects(self):
        Project.objects.create(image=image_file("ochiq.png"))
        Project.objects.create(image=image_file("yopiq.png"), is_published=False)
        self.assertEqual(len(self.client.get("/uz/").context["projects"]), 1)
