from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.core.models import SiteSettings


class AdminTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_superuser("a", "a@a.uz", "uzun-parol-123456")
        self.client.force_login(user)

    def test_admin_singleton_add_forbidden_when_exists(self):
        SiteSettings.load()
        self.assertEqual(self.client.get("/boshqaruv/core/sitesettings/add/").status_code, 403)

    def test_admin_pages_open(self):
        for model in admin.site._registry:
            url = reverse(f"admin:{model._meta.app_label}_{model._meta.model_name}_changelist")
            self.assertEqual(self.client.get(url, follow=True).status_code, 200, url)
