"""Yangi saytning boshlang'ich matnlari va ma'lumotnomalari."""

PATTERNS = {
    1: ("Mayda g'isht", "Мелкий кирпич"),
    2: ("Ingichka g'isht", "Тонкий кирпич"),
    3: ("Tekis tekstura", "Гладкая текстура"),
    4: ("Keng panel", "Широкая панель"),
    5: ("Yirik tosh", "Крупный камень"),
    6: ("Chiziqli", "Линейная"),
}

COLORS = {
    "A": ("Antratsit", "Антрацит", "#2b2e33"),
    "B": ("Ko'k", "Синий", "#1f4fc4"),
    "C": ("Krem", "Кремовый", "#d9d0ae"),
    "CH": ("Jigarrang", "Коричневый", "#5a4638"),
    "E": ("Bej", "Бежевый", "#d8cdb8"),
    "F": ("G'isht bosma", "Кирпичный принт", "#a8654a"),
    "G": ("Binafsha-jigarrang", "Фиолетово-коричневый", "#5d4a5c"),
    "K": ("Yashil", "Зелёный", "#1f6b4f"),
    "L": ("Och krem", "Светло-кремовый", "#e3dcb8"),
    "O": ("Marjon", "Коралловый", "#e4694f"),
    "Q": ("Tosh bosma", "Каменный принт", "#8a6a55"),
    "R": ("To'q sariq", "Оранжевый", "#dd8a3f"),
    "S": ("Kulrang", "Серый", "#8a8f94"),
    "T": ("Tabiiy bosma", "Природный принт", "#a39a86"),
    "V": ("Oqish", "Беловатый", "#dfe7ee"),
    "W": ("Yog'och", "Дерево", "#9a6a3f"),
    "Y": ("Sariq", "Жёлтый", "#e8b860"),
    "Z": ("Zaytun", "Оливковый", "#8b8a70"),
}

HOME_COPY = {
    "hero_kicker": ("01 — Fasad panellari", "01 — Фасадные панели"),
    "hero_title": ("Uyingizning yuzi o'zgarsin", "Новый облик вашего дома"),
    "hero_text": (
        "Po'lat, poliuretan va folga — bir panelda chiroy va issiqlik.",
        "Сталь, пенополиуретан и фольга — красота и тепло в одной панели.",
    ),
    "layers_title": ("Uch qatlam — bitta panel", "Три слоя — одна панель"),
    "adv_title": ("To'qqiz sabab", "Девять причин"),
    "catalog_title": ("Naqshingizni tanlang", "Выберите свой рисунок"),
    "projects_kicker": ("Bajarilgan ishlar", "Выполненные работы"),
    "projects_title": ("Bizning panellar binolarda", "Наши панели на зданиях"),
    "videos_title": ("O'z ko'zingiz bilan ko'ring", "Увидьте своими глазами"),
    "montage_title": ("Uch qadamda", "В три шага"),
    "form_title": ("Narxini bilib oling", "Узнайте цену"),
}

# WordPress ACF maydoni -> HomeContent maydoni
HOME_FROM_WP = {
    "what_title": "layers_kicker",
    "offer_title": "adv_kicker",
    "products_title": "catalog_kicker",
    "works_title": "videos_kicker",
    "montage_title": "montage_kicker",
    "form_title": "form_kicker",
    "partners_title": "partners_title",
}

STATS = [
    {"value": ("3,8 kg/m²", "3,8 кг/м²"), "title": ("yengil — poydevorga yuk yo'q", "лёгкая — без нагрузки на фундамент")},
    {"value": ("16 mm", "16 мм"), "title": ("poliuretan issiqlik qatlami", "слой пенополиуретана")},
    {"value": ("", ""), "title": ("panel", "панелей"), "auto": True},
    {"value": ("50 yil", "50 лет"), "title": ("xizmat muddati", "срок службы")},
]

PANEL_SPECS = {"metal_mm": "0.30", "foam_mm": 16, "weight_kg_m2": "3.8", "lifetime_years": 50}

# YouTube: "bog'langan akkaunt o'chirilgan", video ochilmaydi.
DEAD_VIDEO_IDS = {"XuN47W_qGYk"}

MAP_BASE ="https://yandex.uz/map-widget/v1/?text="
# Eski slayder rasmlari: boshqa kompaniya reklamasi yoki tayyor rasmlar bo'lishi mumkin.
# Boshqaruvchi o'z ishi deb tasdiqlasa, admin'dan ochiladi.
HIDDEN_PROJECT_SUFFIXES = ("2024/07/11.jpg", "2024/07/12.jpg", "2024/07/13.jpg", "2024/07/14.jpg")
