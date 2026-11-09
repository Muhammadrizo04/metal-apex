from django.contrib import admin

from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ["created_at", "name", "phone", "panel_code", "status", "telegram_sent"]
    list_filter = ["status", "telegram_sent"]
    search_fields = ["name", "phone", "panel_code"]
    readonly_fields = [
        "name", "phone", "company", "panel", "panel_code", "source_url", "language",
        "telegram_sent", "telegram_error", "created_at",
    ]

    def has_add_permission(self, request):
        return False
