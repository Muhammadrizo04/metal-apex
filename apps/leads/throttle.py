import logging
import time

from django.conf import settings
from django.core.cache import cache
from django.db import DatabaseError

WINDOW_SECONDS = 600
MAX_SUBMISSIONS = 5

logger = logging.getLogger(__name__)


def client_ip(request) -> str:
    if settings.TRUST_PROXY:
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if forwarded:
            return forwarded.split(",")[-1].strip()
    return request.META.get("REMOTE_ADDR", "")


def is_throttled(ip: str) -> bool:
    """Ruxsat berilgan yuborish hisobga olinadi. Oynadan oshsa True qaytadi.

    Kesh ishlamasa buyurtma yo'qolmasligi uchun cheklov qo'llanmaydi.
    """
    key = f"lead-throttle:{ip}"
    now = time.time()
    try:
        hits = [t for t in cache.get(key, []) if now - t < WINDOW_SECONDS]
        if len(hits) >= MAX_SUBMISSIONS:
            return True
        hits.append(now)
        cache.set(key, hits, WINDOW_SECONDS)
    except DatabaseError:
        logger.exception("Buyurtma cheklovi keshi ishlamadi")
    return False
