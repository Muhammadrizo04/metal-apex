from django.db import models
from django.urls import reverse
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFit, Transpose


def _spec(width):
    return ImageSpecField(
        source="image",
        processors=[Transpose(), ResizeToFit(width, width, upscale=False)],
        format="WEBP",
        options={"quality": 82},
    )


class Pattern(models.Model):
    series = models.PositiveSmallIntegerField("Seriya raqami", unique=True)
    name = models.CharField("Nomi", max_length=80)
    order = models.PositiveSmallIntegerField("Tartib", default=0)

    class Meta:
        ordering = ["order", "series"]
        verbose_name = "Naqsh turi"
        verbose_name_plural = "Naqsh turlari"

    def __str__(self):
        return self.name


class Color(models.Model):
    letter = models.CharField("Harf", max_length=4, unique=True)
    name = models.CharField("Nomi", max_length=80)
    hex = models.CharField("Rang kodi", max_length=7, default="#cccccc")
    order = models.PositiveSmallIntegerField("Tartib", default=0)

    class Meta:
        ordering = ["order", "letter"]
        verbose_name = "Rang"
        verbose_name_plural = "Ranglar"

    def __str__(self):
        return self.name


class PanelQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)


class Panel(models.Model):
    wp_id = models.IntegerField(null=True, blank=True, unique=True, editable=False)
    code = models.CharField("Kod", max_length=20, unique=True)
    pattern = models.ForeignKey(Pattern, on_delete=models.PROTECT, verbose_name="Naqsh turi", related_name="panels")
    color = models.ForeignKey(
        Color, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Rang", related_name="panels"
    )
    image = models.ImageField("Rasm", upload_to="panels/")
    description = models.TextField("Tavsif", blank=True)
    length_mm = models.PositiveIntegerField("Uzunligi, mm", null=True, blank=True)
    width_mm = models.PositiveIntegerField("Eni, mm", null=True, blank=True)
    is_published = models.BooleanField("Saytda ko'rinsin", default=True)
    order = models.PositiveIntegerField("Tartib", default=0)

    image_card = _spec(600)
    image_large = _spec(1400)

    objects = PanelQuerySet.as_manager()

    class Meta:
        ordering = ["order", "code"]
        verbose_name = "Panel"
        verbose_name_plural = "Panellar"

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse("catalog:detail", kwargs={"code": self.code.lower()})


class Accessory(models.Model):
    wp_id = models.IntegerField(null=True, blank=True, unique=True, editable=False)
    name = models.CharField("Nomi", max_length=120)
    image = models.ImageField("Rasm", upload_to="accessories/")
    order = models.PositiveIntegerField("Tartib", default=0)
    is_published = models.BooleanField("Saytda ko'rinsin", default=True)

    image_card = _spec(600)

    class Meta:
        ordering = ["order", "pk"]
        verbose_name = "Aksessuar"
        verbose_name_plural = "Aksessuarlar"

    def __str__(self):
        return self.name
