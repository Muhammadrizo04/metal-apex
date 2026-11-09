from apps.catalog.models import Panel, Pattern
from apps.core.models import AboutPage, SiteSettings
from apps.core.tests.utils import MediaTestCase, image_file
from apps.projects.models import Project


class RedirectTests(MediaTestCase):
    def test_old_urls_redirect_permanently(self):
        cases = [
            ("/products/", "/uz/katalog/"), ("/works/", "/uz/loyihalar/"), ("/about/", "/uz/mahsulot-haqida/"),
            ("/contact/", "/uz/aloqa/"), ("/glavnaya/", "/uz/"), ("/ru/products/", "/ru/katalog/"),
            ("/ru/works/", "/ru/loyihalar/"), ("/ru/about/", "/ru/mahsulot-haqida/"), ("/ru/contact/", "/ru/aloqa/"),
            ("/ru/glavnaya/", "/ru/"),
        ]
        for old, new in cases:
            response = self.client.get(old)
            self.assertEqual((response.status_code, response["Location"]), (301, new), old)


class PageTests(MediaTestCase):
    def test_pages_open_on_empty_db(self):
        for lang in ("uz", "ru"):
            for page in ("loyihalar", "mahsulot-haqida", "aloqa"):
                self.assertEqual(self.client.get(f"/{lang}/{page}/").status_code, 200, page)

    def test_project_caption_only_when_set(self):
        Project.objects.create(image=image_file("a.png"))
        self.assertNotContains(self.client.get("/uz/loyihalar/"), "<figcaption")
        Project.objects.create(image=image_file("b.png"), title_uz="Maktab", city_uz="Qo'qon")
        self.assertContains(self.client.get("/uz/loyihalar/"), "Maktab")

    def test_hidden_project_absent(self):
        Project.objects.create(image=image_file("a.png"), is_published=False)
        self.assertEqual(len(self.client.get("/uz/loyihalar/").context["projects"]), 0)

    def test_about_body_rendered_as_html(self):
        about = AboutPage.load()
        about.title_uz, about.body_uz = "Haqida", "<p>Matn <b>qalin</b></p>"
        about.save()
        self.assertContains(self.client.get("/uz/mahsulot-haqida/"), "<b>qalin</b>")

    def test_contact_shows_details_and_map(self):
        site = SiteSettings.load()
        site.phone_1, site.email_2 = "+998 93 503 23 23", "b@mail.ru"
        site.map_url = "https://yandex.uz/map-widget/v1/?text=Qoqon"
        site.save()
        response = self.client.get("/uz/aloqa/")
        self.assertContains(response, "+998 93 503 23 23")
        self.assertContains(response, "b@mail.ru")
        self.assertContains(response, '<iframe class="map" src="https://yandex.uz/map-widget')
        self.assertContains(response, 'id="buyurtma"')

    def test_contact_no_map_when_blank(self):
        self.assertNotContains(self.client.get("/uz/aloqa/"), "<iframe")

    def test_404_styled(self):
        response = self.client.get("/uz/mavjud-emas/")
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "METAL APEX", status_code=404)

    def test_500_template_is_standalone(self):
        from django.template.loader import render_to_string

        self.assertIn("Metal Apex", render_to_string("500.html"))

    def test_seo_tags(self):
        response = self.client.get("/uz/aloqa/")
        self.assertContains(response, 'hreflang="uz" href="http://testserver/uz/aloqa/"')
        self.assertContains(response, 'hreflang="ru" href="http://testserver/ru/aloqa/"')
        self.assertContains(response, 'property="og:title"')
        self.assertContains(response, 'name="description"')

    def test_sitemap_and_robots(self):
        pattern = Pattern.objects.create(series=5, name_uz="T")
        Panel.objects.create(code="E5-01", pattern=pattern, image="a.png")
        Panel.objects.create(code="G3-01-2", pattern=pattern, image="b.png", is_published=False)
        sitemap = self.client.get("/sitemap.xml")
        self.assertContains(sitemap, "/uz/katalog/e5-01/")
        self.assertContains(sitemap, "/ru/aloqa/")
        self.assertNotContains(sitemap, "g3-01-2")
        robots = self.client.get("/robots.txt")
        self.assertContains(robots, "Disallow: /boshqaruv/")
        self.assertContains(robots, "Sitemap: http://testserver/sitemap.xml")
