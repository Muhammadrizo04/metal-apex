from django.db.models import QuerySet

from .models import Color

MAX_SERIES_DIGITS = 2


def parse_series(value: str | None) -> int | None:
    if value and value.isdecimal() and len(value) <= MAX_SERIES_DIGITS:
        return int(value)
    return None


def parse_letter(value: str | None) -> str | None:
    if value and Color.objects.filter(letter=value).exists():
        return value
    return None


def filter_panels(qs: QuerySet, naqsh: str | None, rang: str | None) -> QuerySet:
    series = parse_series(naqsh)
    letter = parse_letter(rang)
    if series is not None:
        qs = qs.filter(pattern__series=series)
    if letter is not None:
        qs = qs.filter(color__letter=letter)
    return qs
