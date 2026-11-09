from django.test import TestCase

from apps.core.models import HomeContent, SiteSettings, Stat


class SingletonTests(TestCase):
    def test_singleton_load_is_single(self):
        a = SiteSettings.load()
        b = SiteSettings.load()
        self.assertEqual(a.pk, b.pk)
        self.assertEqual(SiteSettings.objects.count(), 1)

    def test_singleton_save_forces_pk_one(self):
        SiteSettings(phone_1="1").save()
        SiteSettings(phone_1="2").save()
        self.assertEqual(SiteSettings.objects.get().phone_1, "2")

    def test_home_children_use_related_names(self):
        home = HomeContent.load()
        Stat.objects.create(home=home, value="16 mm", title="qatlam", order=1)
        self.assertEqual(home.stats.count(), 1)
