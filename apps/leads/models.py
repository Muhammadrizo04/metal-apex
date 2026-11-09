from django.db import models


class Lead(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Yangi"
        CONTACTED = "contacted", "Bog'lanildi"
        CLOSED = "closed", "Yopildi"

    name = models.CharField("Ism", max_length=120)
    phone = models.CharField("Telefon", max_length=40)
    company = models.CharField("Kompaniya", max_length=160, blank=True)
    panel = models.ForeignKey(
        "catalog.Panel", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Panel"
    )
    panel_code = models.CharField("Panel kodi", max_length=20, blank=True)
    source_url = models.CharField("Sahifa", max_length=500, blank=True)
    language = models.CharField("Til", max_length=5, blank=True)
    status = models.CharField("Holat", max_length=12, choices=Status.choices, default=Status.NEW)
    telegram_sent = models.BooleanField("Telegramga yuborildi", default=False)
    telegram_error = models.CharField("Telegram xatosi", max_length=255, blank=True)
    created_at = models.DateTimeField("Sana", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"

    def __str__(self):
        return f"{self.name} {self.phone}"
