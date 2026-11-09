import requests
from django.conf import settings

from .models import Lead

TIMEOUT_SECONDS = 5


def _message(lead: Lead) -> str:
    lines = ["Yangi buyurtma", f"Ism: {lead.name}", f"Telefon: {lead.phone}"]
    if lead.company:
        lines.append(f"Kompaniya: {lead.company}")
    if lead.panel_code:
        lines.append(f"Panel: {lead.panel_code}")
    lines.append(f"Til: {lead.language}")
    return "\n".join(lines)


def send_lead(lead: Lead) -> tuple[bool, str]:
    """Xato matnida manzil bo'lmaydi, chunki manzil ichida bot tokeni turadi."""
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        return False, "Telegram sozlanmagan"
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        response = requests.post(
            url, json={"chat_id": settings.TELEGRAM_CHAT_ID, "text": _message(lead)}, timeout=TIMEOUT_SECONDS
        )
    except requests.RequestException as error:
        return False, type(error).__name__
    if response.status_code != 200:
        return False, f"HTTP {response.status_code}"
    return True, ""


def deliver(lead: Lead) -> bool:
    sent, error = send_lead(lead)
    lead.telegram_sent = sent
    lead.telegram_error = error
    lead.save(update_fields=["telegram_sent", "telegram_error"])
    return sent
