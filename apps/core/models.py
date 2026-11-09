from django.db import models


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SiteSettings(SingletonModel):
    logo = models.ImageField("Logotip", upload_to="site/", blank=True)
    address = models.CharField("Manzil", max_length=255, blank=True)
    phone_1 = models.CharField("Telefon 1", max_length=40, blank=True)
    phone_2 = models.CharField("Telefon 2", max_length=40, blank=True)
    email_1 = models.EmailField("Email 1", blank=True)
    email_2 = models.EmailField("Email 2", blank=True)
    facebook = models.URLField("Facebook", blank=True)
    instagram = models.URLField("Instagram", blank=True)
    youtube = models.URLField("YouTube", blank=True)
    telegram = models.URLField("Telegram", blank=True)
    x = models.URLField("X", blank=True)
    map_url = models.URLField("Xarita havolasi", max_length=500, blank=True)
    metal_mm = models.DecimalField("Metall qalinligi, mm", max_digits=4, decimal_places=2, null=True, blank=True)
    foam_mm = models.PositiveSmallIntegerField("Poliuretan qatlami, mm", null=True, blank=True)
    weight_kg_m2 = models.DecimalField("Vazni, kg/m²", max_digits=4, decimal_places=1, null=True, blank=True)
    lifetime_years = models.PositiveSmallIntegerField("Xizmat muddati, yil", null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = "Sayt sozlamalari"

    def __str__(self):
        return "Sayt sozlamalari"


def _text(label, length=200):
    return models.CharField(label, max_length=length, blank=True)


class HomeContent(SingletonModel):
    hero_kicker = _text("Asosiy ekran: kichik yozuv")
    hero_title = _text("Asosiy ekran: sarlavha")
    hero_text = models.TextField("Asosiy ekran: matn", blank=True)
    hero_image = models.ImageField("Asosiy ekran: foto", upload_to="home/", blank=True)
    layers_kicker = _text("Qatlamlar: kichik yozuv")
    layers_title = _text("Qatlamlar: sarlavha")
    adv_kicker = _text("Afzalliklar: kichik yozuv")
    adv_title = _text("Afzalliklar: sarlavha")
    catalog_kicker = _text("Katalog: kichik yozuv")
    catalog_title = _text("Katalog: sarlavha")
    projects_kicker = _text("Loyihalar: kichik yozuv")
    projects_title = _text("Loyihalar: sarlavha")
    videos_kicker = _text("Videolar: kichik yozuv")
    videos_title = _text("Videolar: sarlavha")
    montage_kicker = _text("Montaj: kichik yozuv")
    montage_title = _text("Montaj: sarlavha")
    montage_image = models.ImageField("Montaj: rasm", upload_to="home/", blank=True)
    partners_title = _text("Hamkorlar: sarlavha")
    form_kicker = _text("Forma: kichik yozuv")
    form_title = _text("Forma: sarlavha")

    class Meta:
        verbose_name = verbose_name_plural = "Bosh sahifa"

    def __str__(self):
        return "Bosh sahifa"


class HomeChild(models.Model):
    title = models.CharField("Sarlavha", max_length=200)
    text = models.TextField("Matn", blank=True)
    order = models.PositiveSmallIntegerField("Tartib", default=0)

    class Meta:
        abstract = True
        ordering = ["order", "pk"]

    def __str__(self):
        return self.title


class Layer(HomeChild):
    home = models.ForeignKey(HomeContent, on_delete=models.CASCADE, related_name="layers")

    class Meta(HomeChild.Meta):
        verbose_name = "Qatlam"
        verbose_name_plural = "Qatlamlar"


class Advantage(HomeChild):
    home = models.ForeignKey(HomeContent, on_delete=models.CASCADE, related_name="advantages")

    class Meta(HomeChild.Meta):
        verbose_name = "Afzallik"
        verbose_name_plural = "Afzalliklar"


class MontageStep(HomeChild):
    home = models.ForeignKey(HomeContent, on_delete=models.CASCADE, related_name="montage_steps")

    class Meta(HomeChild.Meta):
        verbose_name = "Montaj qadami"
        verbose_name_plural = "Montaj qadamlari"


class Stat(models.Model):
    home = models.ForeignKey(HomeContent, on_delete=models.CASCADE, related_name="stats")
    value = models.CharField("Qiymat", max_length=40, blank=True)
    title = models.CharField("Izoh", max_length=120)
    auto_panel_count = models.BooleanField("Panellar sonini avtomatik hisoblash", default=False)
    order = models.PositiveSmallIntegerField("Tartib", default=0)

    class Meta:
        ordering = ["order", "pk"]
        verbose_name = "Raqam"
        verbose_name_plural = "Raqamlar"

    def __str__(self):
        return f"{self.value} {self.title}"


class AboutPage(SingletonModel):
    title = _text("Sarlavha")
    body = models.TextField("Matn (HTML)", blank=True)

    class Meta:
        verbose_name = verbose_name_plural = "Mahsulot haqida sahifasi"

    def __str__(self):
        return "Mahsulot haqida"
