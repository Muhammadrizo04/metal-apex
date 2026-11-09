"""phpMyAdmin SQL dumpini o'qish va WordPress qiymatlarini ajratish."""

import re

_INSERT = re.compile(r"INSERT INTO `([^`]+)` \(([^)]*)\) VALUES\s*")
_ESCAPES = {"n": "\n", "r": "\r", "t": "\t", "0": "\0", "b": "\b", "Z": "\x1a"}
_CODE = re.compile(r"^([A-Z]+)(\d)-(\d+)$")


def _read_string(sql: str, i: int) -> tuple[str, int]:
    """`i` ochuvchi qo'shtirnoqdan keyingi belgi. Satr va undan keyingi o'rin qaytariladi."""
    chars: list[str] = []
    while True:
        c = sql[i]
        if c == "\\":
            next_char = sql[i + 1]
            chars.append(_ESCAPES.get(next_char, next_char))
            i += 2
        elif c == "'":
            if sql[i + 1 : i + 2] == "'":
                chars.append("'")
                i += 2
            else:
                return "".join(chars), i + 1
        else:
            chars.append(c)
            i += 1


def _convert(token: str) -> object:
    token = token.strip()
    if token.upper() == "NULL":
        return None
    try:
        return int(token)
    except ValueError:
        pass
    try:
        return float(token)
    except ValueError:
        return token


def _read_row(sql: str, i: int) -> tuple[list[object], int]:
    """`i` `(` belgisida turadi."""
    i += 1
    values: list[object] = []
    while True:
        while sql[i].isspace():
            i += 1
        if sql[i] == "'":
            value, i = _read_string(sql, i + 1)
        else:
            start = i
            while sql[i] not in ",)":
                i += 1
            value = _convert(sql[start:i])
        values.append(value)
        while sql[i].isspace():
            i += 1
        if sql[i] == ")":
            return values, i + 1
        i += 1


def parse_inserts(sql: str, tables: set[str]) -> dict[str, list[dict[str, object]]]:
    """Faqat `tables` dagi INSERT qatorlarini qaytaradi. Boshqalari o'tkazib yuboriladi."""
    result: dict[str, list[dict[str, object]]] = {}
    pos = 0
    while match := _INSERT.search(sql, pos):
        table = match.group(1)
        columns = [c.strip(" `") for c in match.group(2).split(",")]
        i = match.end()
        while True:
            row, i = _read_row(sql, i)
            if table in tables:
                result.setdefault(table, []).append(dict(zip(columns, row)))
            while sql[i].isspace():
                i += 1
            if sql[i] == ",":
                i += 1
                while sql[i].isspace():
                    i += 1
                continue
            break
        pos = i
    return result


def split_translations(text: str) -> tuple[str, str]:
    """`[:uz]a[:ru]b[:]` ko'rinishidagi matnni (uz, ru) ga ajratadi."""
    if "[:" not in text:
        return text, text
    parts = dict(re.findall(r"\[:(uz|ru)\](.*?)(?=\[:|\Z)", text, flags=re.DOTALL))
    uz = parts.get("uz", "")
    ru = parts.get("ru", "")
    return uz or ru, ru or uz


def php_id_list(value: str) -> list[int]:
    return [int(x) for x in re.findall(r's:\d+:"(\d+)"', value)]


def clean_title(title: str) -> str:
    return split_translations(title)[0].strip(" ,.")


def parse_panel_code(title: str) -> tuple[str, int, str] | None:
    code = clean_title(title)
    match = _CODE.match(code)
    if not match:
        return None
    return match.group(1), int(match.group(2)), code
