# Metal Apex: Django'dagi yangi sayt — spetsifikatsiya

Sana: 2026-11-09
Holat: foydalanuvchi ko'rib chiqishi kutilmoqda

## 1. Maqsad

`metal-apex.uz` saytini (hozir WordPress) Django'da noldan, mavjud materiallar asosida, ancha chiroyli qilib qayta yaratish. Sayt kompaniya boshqaruvchisiga sovg'a sifatida ko'rsatiladi. U ma'qullasa, domen yangi saytga o'tkaziladi.

**Muvaffaqiyat mezonlari**
- Boshqaruvchi ko'rganda "eskisidan ancha yaxshi" degan taassurot qoladi.
- Sayt kompyuter va telefonda chiroyli ochiladi.
- Boshqaruvchi yoki xodim kontentni dasturchisiz, admin paneldan o'zgartira oladi.
- Forma orqali kelgan buyurtma yo'qolmaydi.

**Ko'lamdan tashqari:** narx kalkulyatori, yangiliklar yoki blog, onlayn to'lov, mijoz hisoblari, inglizcha versiya, filiallar xaritasi.

## 2. Texnologiyalar

| Qism | Tanlov |
|---|---|
| Til va freymvork | Python 3.12, Django 5.2 LTS |
| Sahifalar | Django shablonlari, serverda tayyorlanadi |
| Frontend | Qo'lda yozilgan CSS va oddiy JavaScript, yig'ish vositasisiz |
| Tarjima | `django-modeltranslation` (uz, ru maydonlari yonma-yon) |
| Rasmlar | Pillow va `django-imagekit`: WebP, bir necha o'lcham |
| Statik fayllar | WhiteNoise |
| Baza | SQLite. `DATABASE_URL` orqali MariaDB'ga o'tish mumkin |
| Kesh va cheklov | Django bazadagi keshi (Redis kerak emas) |
| Telegram | `requests` orqali to'g'ridan-to'g'ri Bot API |
| Sozlamalar | `.env` fayli, git'ga kirmaydi |

Sayt oddiy WSGI ilova. Celery, Redis yoki alohida fon jarayonlari yo'q, shuning uchun cPanel "Setup Python App"da ham, VPS'da ham ishlaydi. Hosting keyin tanlanadi.

Loyiha joyi: `D:\claude\metal-apex-sayt`. Eski sayt `D:\claude\metal-apex` faqat o'qiladi va o'zgartirilmaydi.

## 3. Vizual uslub

Tasdiqlangan maketlar: `.superpowers/brainstorm/352-1794215025/content/bosh-sahifa-v3.html` va `katalog.html`.

| Token | Qiymat | Qo'llanishi |
|---|---|---|
| Fon | `#f4f1ec` | Sahifa foni |
| Matn | `#1c1c1c` | Asosiy matn, sarlavha |
| Xira matn | `#5d564f` | Izohlar |
| Chiziq | `#ddd6cc` | Chegaralar |
| Mis | `#c46a26` | Katta raqamlar va bezak |
| To'q mis | `#a8561a` | Kichik yozuvlar va tugma foni (o'qilishi uchun kontrast 4.6:1) |

- Sarlavhalar: Oswald 700, katta harflar. Matn: Inter 400/600. Ikkalasi ham lotin va kirill harflari bilan, sayt ichidan yuklanadi.
- Tuzilish: B varianti, ya'ni och fon, matn chapda, foto o'ngda.
- Telefon uchun 760 pikseldan past kenglikda ustunlar ustma-ust tushadi. Gorizontal aylantirish bo'lmaydi.
- Oddiy matn 14 pikseldan kichik bo'lmaydi. Foydalanuvchi izohi: shrift kichik va bo'sh joy ko'p bo'lmasin, kartochka va qutilar proporsional tursin.

## 4. Sahifalar va manzillar

Barcha sahifalar `/uz/` va `/ru/` prefiksida. `/` brauzer tiliga qarab `/uz/` yoki `/ru/`ga yo'naltiradi, standart til o'zbekcha.

| Manzil | Sahifa |
|---|---|
| `/uz/` | Bosh sahifa |
| `/uz/katalog/` | Panellar, filtr bilan |
| `/uz/katalog/aksessuarlar/` | Aksessuarlar |
| `/uz/katalog/<kod>/` | Panel sahifasi, masalan `/uz/katalog/e5-01/` |
| `/uz/loyihalar/` | Loyihalar galereyasi |
| `/uz/mahsulot-haqida/` | Mahsulot haqida matn |
| `/uz/aloqa/` | Kontaktlar, forma, xarita |
| `POST /uz/buyurtma/` | Forma qabul qilish |
| `/uz/buyurtma/qabul/` | "Qabul qilindi" sahifasi |
| `/boshqaruv/` | Django admin |
| `/sitemap.xml`, `/robots.txt` | SEO |

Eski manzillar 301 bilan yo'naltiriladi, uz va `/ru/` variantlari bilan:
`/products/` → `katalog`, `/works/` → `loyihalar`, `/about/` → `mahsulot-haqida`, `/contact/` → `aloqa`, `/glavnaya/` → bosh sahifa.

### Bosh sahifa bo'limlari (tartib bilan)
1. Asosiy ekran: sarlavha, matn, "Katalogni ko'rish" va "Narxini so'rash" tugmalari, bino fotosi.
2. Raqamlar: 3,8 kg/m², 16 mm, panellar soni, 50 yil. Panellar soni ochiq panellardan avtomatik hisoblanadi (`Stat.auto_panel_count`).
3. Panel ichida nima bor: 3 qatlam va ularning tasviri.
4. 9 ta afzallik: 3 ustun, ustida chiziq, kartochkasiz. Sarlavha 21px, matn 14px, raqam 16px.
5. Katalogdan namuna: filtr chiplari, 4 panel, "Barcha N panel" tugmasi (N ochiq panellar soni).
6. Loyihalar: 1 katta va 4 kichik foto.
7. Videolar: 6 ta, 16:9, YouTube muqovasi, bosilganda video yuklanadi.
8. Montaj: chapda chegaralangan rasm (eng ko'pi 340px), o'ngda 3 qadam.
9. Hamkorlar: logotip qutilari, 3:2 nisbat, ustun enining yarmi. Eski bazada logotip yo'q, shuning uchun bu bo'lim kamida bitta `Partner` qo'shilgandagina ko'rinadi.
10. Buyurtma formasi: qora fon, kontaktlar va forma.

Menyu: Mahsulotlar, Loyihalar, Mahsulot haqida, Aloqa, UZ / RU.

### Katalog
- Yorliqlar: Panellar, Aksessuarlar.
- Filtr: naqsh turi (6 ta) va rang. Filtr `?naqsh=5&rang=E` ko'rinishidagi havola, ya'ni JavaScript'siz ham ishlaydi. JavaScript bor bo'lsa, ro'yxat sahifani qayta yuklamasdan yangilanadi.
- 4 ustunli kartochkalar, telefonda 2 ustun.

### Panel sahifasi
Katta rasm, kod, naqsh va rang nomi, ko'rsatkichlar jadvali (metall 0,3 mm, poliuretan 16 mm, vazn 3,8 kg/m², xizmat muddati 50 yilgacha), shu naqshning boshqa ranglari, "Narxini so'rash" tugmasi. Bu tugma formani panel kodi bilan birga ochadi. Uzunlik va en maydonlari ixtiyoriy, bo'sh bo'lsa ko'rsatilmaydi.

### Boshqa sahifalar
- **Mahsulot haqida:** eski `about` sahifasi matni. Kompaniya tarixi to'qib yozilmaydi.
- **Loyihalar:** foto setkasi, to'liq ekranli ko'rish. Nom va shahar kiritilgan bo'lsagina ko'rsatiladi.
- **Aloqa:** manzil, 2 telefon, 2 email, forma, xarita (Yandex xarita vidjeti, manzil admin'dagi havoladan olinadi).

## 5. Ma'lumotlar modeli

`[t]` belgisi uz va ru tarjimali maydonni bildiradi.

**`core`**
- `SiteSettings` (yagona yozuv): logo, `address[t]`, `phone_1`, `phone_2`, `email_1`, `email_2`, facebook, instagram, youtube, telegram, x, `map_url`, va panel ko'rsatkichlari `metal_mm`, `foam_mm`, `weight_kg_m2`, `lifetime_years`.
- `HomeContent` (yagona yozuv): asosiy ekran matnlari `[t]` va fotosi, bo'lim sarlavhalari `[t]`, forma sarlavhasi `[t]`, montaj rasmi.
- `Layer`, `Advantage`, `MontageStep`: `HomeContent`ga bog'langan, `title[t]`, `text[t]`, `order`.
- `Stat`: `HomeContent`ga bog'langan, `value[t]`, `title[t]`, `auto_panel_count`, `order`. `auto_panel_count` yoqilsa, `value` o'rniga ochiq panellar soni chiqadi.
- `AboutPage` (yagona yozuv): `title[t]`, `body[t]` (HTML).

**`catalog`**
- `Pattern`: `series` (1 dan 6 gacha, yagona), `name[t]`, `order`.
- `Color`: `letter` (yagona), `name[t]`, `hex`, `order`.
- `Panel`: `code` (yagona), `pattern` FK, `color` FK, `image`, `description[t]`, `length_mm` va `width_mm` (ixtiyoriy), `is_published`, `order`.
- `Accessory`: `name[t]`, `image`, `order`, `is_published`.

**`projects`**
- `Project`: `title[t]` (ixtiyoriy), `city[t]` (ixtiyoriy), `image`, `order`, `is_published`.
- `Video`: `url`, `title[t]` (ixtiyoriy), `order`. YouTube ID manzildan avtomatik olinadi, Shorts ham qo'llanadi.
- `Partner`: `name`, `logo`, `order`.

**`leads`**
- `Lead`: `name`, `phone`, `company`, `panel` FK (ixtiyoriy, panel o'chsa bo'sh qoladi), `panel_code` (matn nusxa), `source_url`, `language`, `status` (yangi, bog'lanildi, yopildi), `telegram_sent`, `telegram_error`, `created_at`.

## 6. Admin panel

Barcha modellar o'zbekcha nomlar bilan. `SiteSettings`, `HomeContent`, `AboutPage` faqat bitta yozuvli. Panel ro'yxatida kichik rasm, naqsh va rang bo'yicha filtr va qidiruv bor. Buyurtmalar ro'yxatida holat va Telegram belgisi ko'rinadi, shuningdek "Telegramga qayta yuborish" amali mavjud.

## 7. Eski saytdan ko'chirish

Bitta buyruq: `python manage.py import_wordpress --sql <fayl> --uploads <papka>`. Qayta ishga tushirilsa nusxa yaratmaydi.

Buyruq SQL dumpdan faqat `mx_posts` va `mx_postmeta` jadvallaridagi kerakli yozuvlarni oladi. `mx_users`, `mx_usermeta`, `mx_options` (bot tokeni shu yerda) va xavfsizlik plagini jadvallari o'qilmaydi. Mavjud yozuvlar qayta import paytida o'zgartirilmaydi, shuning uchun admin'da qilingan tahrirlar saqlanadi. Foydalanuvchilar va parollar ko'chirilmaydi. SQL fayl loyiha ichiga va git'ga qo'shilmaydi.

| Nima | Manba | Natija |
|---|---|---|
| Panellar | 16-sahifa `products` (82 rasm) | 67 panel, kod shablon bo'yicha ajratiladi: harf(lar) + raqam + `-` + tartib |
| Aksessuarlar | O'sha ro'yxatning qolgan 15 tasi | 15 aksessuar, nom oxiridagi `,` `.` belgilari tozalanadi |
| Matnlar | 8, 10, 12-sahifalar | `HomeContent`, inline'lar, `AboutPage`, `SiteSettings`. `[:uz]..[:ru]..[:]` belgilari ikki tilga ajratiladi |
| Loyihalar | Slayder va 14-sahifa `works` | `Project`, nomsiz. Bir xil fayl qayta olinmaydi |
| Videolar | `works_video_*` | 6 ta `Video` |
| Hamkorlar | `partners_images` | Eski bazada bo'sh, hech narsa import qilinmaydi. Logotiplar admin'dan qo'shiladi |

Maxsus holatlar:
- `G3-01` kodi ikki xil panelda. Birinchisi `G3-01` bo'lib ochiq turadi, ikkinchisi `G3-01-2` kodi bilan `is_published=False`da qoladi va boshqaruvchi to'g'ri kodni aytguncha ko'rinmaydi. Shu sababli import 67 yozuv yaratadi, lekin saytda dastlab 66 panel ko'rinadi.
- Eski slayderdagi `2024/07/11.jpg`, `12.jpg`, `13.jpg`, `14.jpg` (mis fasad, tayyor uy rasmlari va boshqa kompaniya reklamasi yozilgan foto) `is_published=False`da import qilinadi. Boshqaruvchi o'zining ishi deb tasdiqlasa ochiladi.
- Eski matnlardagi "Engil vazn" kabi imlo va mashina tarjimasi xatolari saqlanib qoladi. Ularni admin'dan tuzatish mumkin.

Naqsh turlari (taklif, boshqaruvchi tasdiqlaydi): 1 Mayda g'isht, 2 Ingichka g'isht, 3 Tekis tekstura, 4 Keng panel, 5 Yirik tosh, 6 Chiziqli.

Boshlang'ich ranglar (rasmlardan taxmin, admin'dan o'zgartiriladi):

| Harf | Nomi | Hex | | Harf | Nomi | Hex |
|---|---|---|---|---|---|---|
| A | Antratsit | `#2b2e33` | | L | Och krem | `#e3dcb8` |
| B | Ko'k | `#1f4fc4` | | O | Marjon | `#e4694f` |
| C | Krem | `#d9d0ae` | | Q | Tosh bosma | `#8a6a55` |
| CH | Jigarrang | `#5a4638` | | R | To'q sariq | `#dd8a3f` |
| E | Bej | `#d8cdb8` | | S | Kulrang | `#8a8f94` |
| F | G'isht bosma | `#a8654a` | | T | Tabiiy bosma | `#a39a86` |
| G | Binafsha-jigarrang | `#5d4a5c` | | V | Oqish | `#dfe7ee` |
| K | Yashil | `#1f6b4f` | | W | Yog'och | `#9a6a3f` |
| Y | Sariq | `#e8b860` | | Z | Zaytun | `#8b8a70` |

## 8. Buyurtma oqimi

1. Forma: ism (majburiy), telefon (majburiy), kompaniya (ixtiyoriy), yashirin panel kodi, spam uchun yashirin maydon.
2. Server tekshiradi. Xato bo'lsa, xabar maydon yonida chiqadi va kiritilgan qiymatlar saqlanib qoladi.
3. `Lead` bazaga yoziladi.
4. Telegram'ga oddiy matn yuboriladi (`parse_mode`siz, shuning uchun mijoz matni formatni buzmaydi), kutish chegarasi 5 soniya.
5. Mijozga "Qabul qilindi" chiqadi. Telegram xato bersa ham javob o'zgarmaydi, xato `telegram_error`ga yoziladi va `telegram_sent=False` bo'ladi.

Xabar ko'rinishi:

```
Yangi buyurtma
Ism: ...
Telefon: ...
Kompaniya: ...
Panel: E5-01
Til: uz
```

Bot tokeni va guruh ID'si `.env`dagi `TELEGRAM_BOT_TOKEN` va `TELEGRAM_CHAT_ID`da. Ishlab chiqishda test bot va test guruh ishlatiladi. Boshqaruvchining bot va guruhi faqat ishga tushirishda qo'yiladi. Eski bazadagi token ko'chirilmaydi.

## 9. Xavfsizlik va xatolar

- Spam: yashirin maydon to'ldirilsa, forma jimgina rad etiladi. Bitta IP'dan 10 daqiqada 5 tadan ortiq yuborish cheklanadi.
- `.env` git'ga kirmaydi, `DEBUG` production'da o'chiq, HTTPS va xavfsiz cookie sozlamalari yoqilgan, CSRF himoyasi ishlaydi.
- Admin uchun kuchli parol, admin manzili `/boshqaruv/`.
- Yuklanadigan fayllar faqat rasm formatida qabul qilinadi.
- 404 va 500 uchun sayt uslubidagi sahifalar.
- YouTube videolar faqat bosilganda yuklanadi, sahifa sekinlashmaydi.

## 10. SEO

Har sahifa uchun title, description va Open Graph. `hreflang` uz va ru uchun, `sitemap.xml`, `robots.txt`, eski manzillardan 301. Rasmlarda `alt` matni: panel kodi va naqsh nomi.

## 11. Sinov

Avtomatik testlar (Django test runner):
- Namuna dump bilan import: panel va aksessuarlar soni, kodni ajratish, `G3-01` holati, tarjima ajratish, qayta ishga tushirish nusxa bermasligi, foydalanuvchilar ko'chirilmasligi.
- Filtr: naqsh, rang, ikkalasi birga, faqat `is_published` yozuvlar.
- Forma: to'g'ri va xato ma'lumot, yashirin maydon, cheklov, Telegram muvaffaqiyatli va xatoli holatlar (Telegram so'rovi soxtalashtiriladi).
- Eski manzillar 301 berishi, ikkala til sahifalari ochilishi.

Haqiqiy dump bilan import bir marta qo'lda ishga tushirilib, 67 va 15 sonlari tekshiriladi. Sahifalar 1280 va 375 piksel kenglikda brauzerda ko'rib chiqiladi. Test guruhga bitta haqiqiy xabar yuboriladi.

## 12. Ishga tushirish tartibi

1. Sayt kompyuterda to'liq ishlaydi va boshqaruvchiga ko'rsatiladi.
2. U rozi bo'lsa, hosting tanlanadi va vaqtinchalik manzilda sinab ko'riladi.
3. `.env`da Telegram boshqaruvchining bot va guruhiga o'tkaziladi.
4. Boshqaruvchining ruxsati bilan domen yangi saytga ulanadi.
5. Eski WordPress va uning zaxirasi o'chirilmaydi, muammo bo'lsa domen qaytariladi.

## 13. Boshqaruvchidan bilinadigan narsalar

Bular saytni ko'rsatishga to'sqinlik qilmaydi, keyin admin'dan kiritiladi:
- Naqsh va rang nomlarini tasdiqlash, `G3-01` ning to'g'ri kodi.
- Panel uzunligi va eni.
- Loyihalarning nomi va shahri, mis fasad fotosi o'zining ishimi.
- Kompaniya haqida matn, agar kerak bo'lsa.
- Hamkorlar logotiplari, agar bu bo'lim kerak bo'lsa.
