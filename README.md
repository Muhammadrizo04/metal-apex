# Metal Apex sayti

Django 5.2 asosidagi `metal-apex.uz` sayti. O'zbek va rus tillarida, kontent Django admin (`/boshqaruv/`) orqali boshqariladi.

## Kompyuterda ishga tushirish

Windows Git Bash buyruqlari. Python 3.12 kerak.

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
cp .env.example .env
```

`.env` faylida `SECRET_KEY` ga uzun tasodifiy qiymat yozing. So'ng:

```bash
.venv/Scripts/python manage.py migrate
.venv/Scripts/python manage.py createcachetable
.venv/Scripts/python manage.py import_wordpress --sql D:/claude/metal-apex/metalap1_site.sql --uploads D:/claude/metal-apex/public_html/wp-content/uploads
.venv/Scripts/python manage.py generateimages
.venv/Scripts/python manage.py createsuperuser
.venv/Scripts/python manage.py runserver
```

`generateimages` rasmlarning WebP nusxalarini oldindan tayyorlaydi, shunda birinchi ochilish sekin bo'lmaydi.

Testlar:

```bash
.venv/Scripts/python manage.py test
```

## Telegram

Xabarlar `.env` dagi ikki qiymat bo'yicha yuboriladi:

```
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

Sinov uchun @BotFather orqali test bot oching, uni test guruhga qo'shing va shu qiymatlarni yozing. Guruh ID'sini bilish uchun guruhga xabar yozib, brauzerda `https://api.telegram.org/bot<TOKEN>/getUpdates` manzilini oching. Ishga tushirishda ikkala qiymatni asl bot va guruhnikiga almashtiring, kodga tegish kerak emas.

## Ishga tushirish tartibi

1. Saytni boshqaruvchiga ko'rsatish.
2. U rozi bo'lsa, hosting tanlash va vaqtinchalik manzilda sinash.
3. `.env` da quyidagilarni qo'yish: `DEBUG=False`, `PRODUCTION=True`, `ALLOWED_HOSTS=metal-apex.uz,www.metal-apex.uz`, `CSRF_TRUSTED_ORIGINS=https://metal-apex.uz,https://www.metal-apex.uz`. Sayt proksi orqasida ishlasa, `TRUST_PROXY=True`. Hosting `media/` ni o'zi bermasa, `SERVE_MEDIA=True`.
4. `python manage.py collectstatic`, `migrate`, `createcachetable` buyruqlarini bajarish.
5. Telegram'ni asl bot va guruhga o'tkazish.
6. Boshqaruvchining ruxsati bilan domenni yangi saytga ulash.
7. Eski WordPress va uning zaxirasini o'chirmaslik, muammo bo'lsa domen qaytariladi.

Maxfiy fayllar (`.env`, SQL dump, `media/`, `db.sqlite3`) git'ga kirmaydi.
