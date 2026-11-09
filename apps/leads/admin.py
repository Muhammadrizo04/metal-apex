from django.contrib import admin, messages

from .models import Lead
from .telegram import deliver


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ["created_at", "name", "phone", "panel_code", "status", "telegram_sent"]
    list_filter = ["status", "telegram_sent"]
    search_fields = ["name", "phone", "panel_code"]
    actions = ["resend_telegram"]
    readonly_fields = [
        "name", "phone", "company", "panel", "panel_code", "source_url", "language",
        "telegram_sent", "telegram_error", "created_at",
    ]

    def has_add_permission(self, request):
        return False

    @admin.action(description="Telegramga qayta yuborish")
    def resend_telegram(self, request, queryset):
        sent = sum(deliver(lead) for lead in queryset)
        self.message_user(request, f"Yuborildi: {sent} ta, jami {queryset.count()} ta.", messages.INFO)
