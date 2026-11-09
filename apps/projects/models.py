from urllib.parse import parse_qs, urlparse

from django.db import models
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFit, Transpose


class Project(models.Model):
    wp_id = models.IntegerField(null=True, blank=True, unique=True, editable=False)
    title = models.CharField("Nomi", max_length=160, blank=True)
    city = models.CharField("Shahar", max_length=80, blank=True)
    image = models.ImageField("Foto", upload_to="projects/")
    order = models.PositiveIntegerField("Tartib", default=0)
    is_published = models.BooleanField("Saytda ko'rinsin", default=True)

    image_card = ImageSpecField(
        source="image",
        processors=[Transpose(), ResizeToFit(900, 900, upscale=False)],
        format="WEBP",
        options={"quality": 82},
    )
    image_large = ImageSpecField(
        source="image",
        processors=[Transpose(), ResizeToFit(1920, 1920, upscale=False)],
        format="WEBP",
        options={"quality": 85},
    )

    class Meta:
        ordering = ["order", "pk"]
        verbose_name = "Loyiha"
        verbose_name_plural = "Loyihalar"

    def __str__(self):
        return self.title or f"Loyiha {self.pk}"


class Video(models.Model):
    url = models.URLField("YouTube havolasi", unique=True)
    title = models.CharField("Nomi", max_length=160, blank=True)
    order = models.PositiveIntegerField("Tartib", default=0)

    class Meta:
        ordering = ["order", "pk"]
        verbose_name = "Video"
        verbose_name_plural = "Videolar"

    def __str__(self):
        return self.title or self.url

    @property
    def youtube_id(self):
        parsed = urlparse(self.url)
        host = parsed.netloc.lower().removeprefix("www.").removeprefix("m.")
        parts = [p for p in parsed.path.split("/") if p]
        if host == "youtu.be" and parts:
            return parts[0]
        if host == "youtube.com":
            if parts[:1] == ["watch"]:
                return parse_qs(parsed.query).get("v", [""])[0]
            if len(parts) >= 2 and parts[0] in {"shorts", "embed", "live"}:
                return parts[1]
        return ""


class Partner(models.Model):
    name = models.CharField("Nomi", max_length=120)
    logo = models.ImageField("Logotip", upload_to="partners/")
    order = models.PositiveIntegerField("Tartib", default=0)

    class Meta:
        ordering = ["order", "pk"]
        verbose_name = "Hamkor"
        verbose_name_plural = "Hamkorlar"

    def __str__(self):
        return self.name
