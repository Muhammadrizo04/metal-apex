# Metal Apex Django sayti — amalga oshirish rejasi

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `metal-apex.uz` saytini Django'da, tasdiqlangan maketlar bo'yicha, kompyuterda to'liq ishlaydigan holatda qayta yaratish.

**Architecture:** Serverda tayyorlanadigan Django sayti, to'rtta ilova (`core`, `catalog`, `projects`, `leads`). Kontent Django admin orqali boshqariladi, boshlang'ich ma'lumot bitta buyruq bilan eski WordPress dumpidan olinadi. Fon jarayonlari va tashqi xizmatlar yo'q, faqat Telegram Bot API.

**Tech Stack:** Python 3.12, Django 5.2, django-modeltranslation, django-imagekit, Pillow, WhiteNoise, requests, django-environ, oddiy CSS va JavaScript.

**Spec:** `docs/superpowers/specs/2026-11-09-metal-apex-django-design.md`

## Global Constraints

- Loyiha ildizi: `D:\claude\metal-apex-sayt`. `D:\claude\metal-apex` faqat o'qiladi.
- Tillar: `uz` (standart), `ru`. Barcha sahifa manzillari `/uz/` yoki `/ru/` prefiksli.
- Ranglar: fon `#f4f1ec`, matn `#1c1c1c`, xira matn `#5d564f`, chiziq `#ddd6cc`, mis `#c46a26`, to'q mis `#a8561a`. Kichik yozuv va tugma foni faqat to'q mis.
- Shriftlar: sarlavha Oswald 700 katta harflar, matn Inter 400/600, sayt ichidan yuklanadi. Oddiy matn 14px dan kichik emas.
- Telefon chegarasi: 760px dan past kenglikda ustunlar ustma-ust. Gorizontal aylantirish yo'q.
- Maxfiy qiymatlar faqat `.env` da. `.env`, `db.sqlite3`, `media/`, `*.sql`, `.superpowers/`, `.venv/` git'ga kirmaydi.
- Barcha foydalanuvchiga ko'rinadigan matn o'zbek va rus tilida. Kompaniya haqida ma'lumot to'qilmaydi.
- `gettext` ishlatilmaydi (Windows va cPanel'da `msgfmt` kerak bo'lmasin). Interfeys matnlari `apps/core/ui.py` da.
- Testlar: `.venv/Scripts/python manage.py test`. Telegram testlarda doim soxtalashtiriladi.
- Commit xabari oxirida: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. Hech qachon `git push` qilinmaydi.

## Review Focus

1. Telefon turli yozuvda (`+998 90 123-45-67`, `901234567`) qabul qilinishi, harfli qiymat rad etilishi kerak. Task 6 da test bor.
2. Bo'sh baza yoki to'ldirilmagan kontent bilan har bir sahifa 200 qaytarishi, bo'sh bo'limlar yashirilishi kerak (500 emas). Task 4 da test bor.
3. Filtrda noma'lum yoki xavfli qiymat (`?naqsh=abc&rang=<script>`) 500 bermasligi, e'tiborsiz qoldirilishi kerak. Panel manzili katta-kichik harfga bog'liq bo'lmasligi kerak. Task 5 da test bor.
4. Telegram xatosida saqlanadigan matnda bot tokeni bo'lmasligi kerak (`requests` xatolari manzilni o'z ichiga oladi). Task 6 da test bor.
5. Dumpda ko'rsatilgan rasm fayli diskda yo'q bo'lsa, import to'xtamasligi, o'sha yozuvni o'tkazib hisobotda aytishi kerak. Task 3 da test bor.

---

## Fayl tuzilishi

```
manage.py, requirements.txt, .env.example, .gitignore, README.md
config/        settings.py, urls.py, wsgi.py
apps/core/     models.py, translation.py, admin.py, views.py, ui.py, context_processors.py,
               templatetags/site_tags.py, wordpress/parser.py, wordpress/seed.py,
               management/commands/import_wordpress.py, tests/
apps/catalog/  models.py, translation.py, admin.py, views.py, urls.py, filters.py, tests/
apps/projects/ models.py, translation.py, admin.py, views.py, urls.py, tests/
apps/leads/    models.py, admin.py, forms.py, views.py, urls.py, telegram.py, throttle.py, tests/
templates/     base.html, 404.html, 500.html, core/, catalog/, projects/, leads/, includes/
static/        css/site.css, js/site.js, js/catalog.js, fonts/
```

---

### Task 1: Loyiha poydevori va umumiy shablon

**Files:**
- Create: `requirements.txt`, `.env.example`, `.gitignore`, `manage.py`, `config/*`, `apps/*/__init__.py`, `apps/*/apps.py`, `apps/core/ui.py`, `apps/core/templatetags/site_tags.py`, `templates/base.html`, `templates/includes/{header,footer}.html`, `static/css/site.css`, `static/js/site.js`, `static/fonts/*`
- Test: `apps/core/tests/test_foundation.py`

**Interfaces:**
- Produces: `{% load site_tags %}{% t 'key' %}` joriy tilda matn qaytaradi. `apps.core.ui.UI: dict[str, dict[str, str]]`. `base.html` bloklari: `title`, `description`, `content`, `extra_js`. CSS klasslari: `.sec`, `.lbl`, `.t`, `.mut`, `.btn`, `.btn-o`, `.chips`.

- [ ] **Step 1: Git va virtual muhit**

Run: `git init`, `python -m venv .venv`. `requirements.txt`:
`Django>=5.2,<5.3`, `django-modeltranslation>=0.19,<0.20`, `django-imagekit>=5.0,<6`, `Pillow>=11`, `whitenoise>=6.7,<7`, `requests>=2.32,<3`, `django-environ>=0.12,<0.13`.
Run: `.venv/Scripts/python -m pip install -r requirements.txt`. Expected: xatosiz tugaydi.

- [ ] **Step 2: Shriftlarni yuklash**

`static/fonts/` ga `https://cdn.jsdelivr.net/npm/@fontsource/oswald@5.1.0/files/` dan `oswald-{latin,cyrillic}-700-normal.woff2` va `https://cdn.jsdelivr.net/npm/@fontsource/inter@5.1.0/files/` dan `inter-{latin,cyrillic}-{400,600}-normal.woff2`. Expected: 6 fayl, har biri 5 KB dan katta.

- [ ] **Step 3: Failing test**

```python
class FoundationTests(TestCase):
    def test_root_redirects_to_language(self):
        r = self.client.get("/", HTTP_ACCEPT_LANGUAGE="ru")
        self.assertEqual(r.status_code, 302); self.assertEqual(r["Location"], "/ru/")
    def test_root_default_is_uz(self):
        self.assertEqual(self.client.get("/", HTTP_ACCEPT_LANGUAGE="en")["Location"], "/uz/")
    def test_home_renders_nav_in_language(self):
        self.assertContains(self.client.get("/uz/"), "Mahsulotlar")
        self.assertContains(self.client.get("/ru/"), "Продукция")
    def test_ui_has_both_languages(self):
        for key, v in UI.items(): self.assertEqual(set(v), {"uz", "ru"}, key)
```

- [ ] **Step 4: Testni ishga tushirish**

Run: `.venv/Scripts/python manage.py test apps.core.tests.test_foundation`. Expected: FAIL (hali sozlanmagan).

- [ ] **Step 5: Sozlamalar va shablonni yozish**

`config/settings.py` `.env` dan o'qiydi: `SECRET_KEY`, `DEBUG` (standart False), `PRODUCTION` (standart False), `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `DATABASE_URL` (standart `sqlite:///db.sqlite3`), `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `TRUST_PROXY` (standart False), `SERVE_MEDIA` (standart False). `INSTALLED_APPS` da `modeltranslation` `django.contrib.admin` dan oldin, `imagekit`, `django.contrib.sitemaps` va to'rt ilova. `LANGUAGE_CODE="uz"`, `LANGUAGES=[("uz",…),("ru",…)]`, `MODELTRANSLATION_FALLBACK_LANGUAGES=("uz","ru")`, `LocaleMiddleware`, WhiteNoise middleware, `CACHES` `DatabaseCache` (`django_cache`). `PRODUCTION=True` bo'lsa: `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_HSTS_SECONDS=3600`, `CompressedManifestStaticFilesStorage`. `urls.py`: `i18n_patterns(prefix_default_language=True)`, admin `boshqaruv/`. `SERVE_MEDIA` yoki `DEBUG` bo'lsa media `django.views.static.serve` orqali. Vaqtinchalik bosh sahifa view `base.html` ni chizadi (`core:home` nomi bilan).

`base.html`: maket bo'yicha sarlavha (logo, menyu: Mahsulotlar, Loyihalar, Mahsulot haqida, Aloqa, UZ / RU almashtirgich joriy sahifani saqlab), telefonda `<details>` asosidagi menyu, footer. `site.css`: Global Constraints tokenlari `:root` da, `@font-face`, maket `bosh-sahifa-v3.html` dagi umumiy klasslar. `.gitignore` Global Constraints ro'yxati bo'yicha.

- [ ] **Step 6: Testni tekshirish**

Run: `.venv/Scripts/python manage.py test apps.core.tests.test_foundation`. Expected: 4 ta test PASS.

- [ ] **Step 7: Commit** — `feat: loyiha poydevori, ikki til va umumiy shablon`

---

### Task 2: Modellar va admin panel

**Files:**
- Create: `apps/{core,catalog,projects,leads}/{models,translation,admin}.py` (leads uchun translation yo'q), migratsiyalar, `apps/core/context_processors.py`
- Test: `apps/core/tests/test_models.py`, `apps/catalog/tests/test_models.py`, `apps/projects/tests/test_models.py`, `apps/core/tests/test_admin.py`

**Interfaces:**
- Produces (spec 5-bo'limi bo'yicha, qo'shimchalar bilan):
  - `core.models.SingletonModel.load() -> Self` (`pk=1`, `get_or_create`). Merosxo'rlar: `SiteSettings`, `HomeContent`, `AboutPage`.
  - `HomeContent` maydonlari, `[t]`: `hero_kicker`, `hero_title`, `hero_text`, `layers_kicker`, `layers_title`, `adv_kicker`, `adv_title`, `catalog_kicker`, `catalog_title`, `projects_kicker`, `projects_title`, `videos_kicker`, `videos_title`, `montage_kicker`, `montage_title`, `partners_title`, `form_kicker`, `form_title`. Rasm: `hero_image`, `montage_image`.
  - `Stat(home, value[t], title[t], auto_panel_count: bool, order)`, `Layer|Advantage|MontageStep(home, title[t], text[t], order)`. Barchasida `related_name` ko'plikda: `stats`, `layers`, `advantages`, `montage_steps`.
  - `catalog.models.Pattern(series: int unique, name[t], order)`, `Color(letter unique, name[t], hex, order)`, `Panel(wp_id null unique editable=False, code unique, pattern FK, color FK null, image, description[t], length_mm null, width_mm null, is_published=True, order)`, `Accessory(wp_id, name[t], image, order, is_published=True)`.
  - `Panel.objects.published()`, `Panel.get_absolute_url()` (kod kichik harfda), `Panel.image_card` (600px WebP), `Panel.image_large` (1400px WebP) `ImageSpecField`. `Accessory.image_card` xuddi shunday.
  - `projects.models.Project(wp_id, title[t] blank, city[t] blank, image, order, is_published)`, `image_card`, `image_large`. `Video(url unique, title[t] blank, order)`, `Video.youtube_id -> str`. `Partner(name, logo, order)`.
  - `leads.models.Lead` spec bo'yicha, `Status` TextChoices: `new`, `contacted`, `closed`.
  - Context processor `site` → `SiteSettings.load()`.

- [ ] **Step 1: Failing testlar**

```python
def test_singleton_load_is_single(self):
    a = SiteSettings.load(); b = SiteSettings.load(); self.assertEqual(a.pk, b.pk); self.assertEqual(SiteSettings.objects.count(), 1)
def test_singleton_save_forces_pk_one(self):
    SiteSettings(phone_1="1").save(); SiteSettings(phone_1="2").save(); self.assertEqual(SiteSettings.objects.get().phone_1, "2")
def test_panel_url_is_lowercase(self): # code="E5-01"
    self.assertEqual(panel.get_absolute_url(), "/uz/katalog/e5-01/")
def test_published_excludes_hidden(self): ...  # is_published=False yozuv ro'yxatda yo'q
def test_youtube_id_variants(self):
    for url, vid in [("https://www.youtube.com/watch?v=XuN47W_qGYk","XuN47W_qGYk"),
                     ("https://youtu.be/r1NFnKlrsvk?si=Q7pMxSBZhnZEHBcC","r1NFnKlrsvk"),
                     ("https://youtube.com/shorts/YIUAgnRsXHA?feature=share","YIUAgnRsXHA")]:
        self.assertEqual(Video(url=url).youtube_id, vid)
def test_translation_falls_back_to_uz(self): # name_uz to'la, name_ru bo'sh: ru tilida uz chiqadi
def test_admin_singleton_add_forbidden_when_exists(self): # staff bilan /boshqaruv/core/sitesettings/add/ 403
def test_admin_pages_open(self): # har bir ro'yxatdan o'tgan model changelist 200
```

- [ ] **Step 2: Test FAIL ekanini tekshirish** — Run: `.venv/Scripts/python manage.py test apps`. Expected: FAIL/ImportError.

- [ ] **Step 3: Modellar, tarjima va admin**

Admin: `TranslationAdmin` va `TranslationTabularInline`, o'zbekcha `verbose_name`. Singleton admin `has_add_permission` faqat yozuv yo'q bo'lsa, `has_delete_permission=False`. `PanelAdmin`: `list_display` kichik rasm, kod, naqsh, rang, `is_published`; `list_filter` naqsh, rang, `is_published`; `search_fields=["code"]`. `LeadAdmin`: `list_display` sana, ism, telefon, panel kodi, holat, `telegram_sent`; `list_filter` holat va `telegram_sent`; maydonlar holatdan boshqasi faqat o'qish uchun; `resend_telegram` amali Task 6 da qo'shiladi. Rasm maydonlari `ImageField`, shuning uchun SVG va rasm bo'lmagan fayl rad etiladi.

Run: `.venv/Scripts/python manage.py makemigrations`, keyin `migrate`, keyin `createcachetable`.

- [ ] **Step 4: Testlarni tekshirish** — Run: `.venv/Scripts/python manage.py test apps`. Expected: hammasi PASS.

- [ ] **Step 5: Commit** — `feat: ma'lumot modellari va admin panel`

---

### Task 3: WordPress'dan import

**Files:**
- Create: `apps/core/wordpress/parser.py`, `apps/core/wordpress/seed.py`, `apps/core/management/commands/import_wordpress.py`
- Test: `apps/core/tests/test_import.py`, `apps/core/tests/fixtures/sample_dump.sql`

**Interfaces:**
- Produces:
  - `parse_inserts(sql: str, tables: set[str]) -> dict[str, list[dict[str, object]]]`: faqat `tables` dagi `INSERT INTO` qatorlari, ustun nomlari INSERT ro'yxatidan.
  - `split_translations(text: str) -> tuple[str, str]`: `[:uz]a[:ru]b[:]` → `("a","b")`. Belgisiz matn → `(text, text)`.
  - `php_id_list(value: str) -> list[int]`: `a:2:{i:0;s:2:"97";i:1;s:2:"60";}` → `[97, 60]`.
  - `parse_panel_code(title: str) -> tuple[str, int, str] | None`: oxiridagi bo'shliq, `,` va `.` tozalanadi, `[:uz]` belgilari olib tashlanadi, `"G3-01 ."` → `("G", 3, "G3-01")`. Naqsh `^([A-Z]+)(\d)-(\d+)$`, moslashmasa `None`.
  - Buyruq: `import_wordpress --sql PATH --uploads PATH`, oxirida hisobot: panel, aksessuar, loyiha, video soni va o'tkazib yuborilgan fayllar.

- [ ] **Step 1: Sinov dumpi**

`sample_dump.sql`: phpMyAdmin ko'rinishida `INSERT INTO \`mx_posts\` (\`ID\`, \`post_content\`, \`post_title\`, \`post_status\`, \`post_type\`) VALUES …`, `mx_postmeta`, shuningdek `mx_users` (`user_pass` bilan) va `mx_options` (`wpcf7_telegram_tkn` bilan). Ichida: `A1-02`, `Q3-101`, `CH5-01`, ikkita `G3-01` (biri `G3-01 .`), `[:uz]T4-04[:ru]T4-04[:]`, ikkita aksessuar (`наружный угол`, `наружный угол ,`), `O\'zbek` va `''` qochirilgan matn, 8-sahifa uchun `what_components_0_text_1`, `offer_offers_0_text_1`, `montage_components_0_text_1`, `works_video_0_url`, `slider_images`, 14-sahifa `works`, `2024/07/11.jpg`, va diskda yo'q fayl.

- [ ] **Step 2: Failing testlar**

```python
def test_parse_only_requested_tables(self):
    r = parse_inserts(SQL, {"mx_posts"}); self.assertEqual(set(r), {"mx_posts"}); self.assertNotIn("hash-qiymat", str(r))
def test_parse_unescapes(self): # \' va '' to'g'ri, qiymat ichidagi "), (" qatorni bo'lmaydi
def test_split_translations(self): self.assertEqual(split_translations("[:uz]a[:ru]b[:]"), ("a","b"))
def test_split_plain(self): self.assertEqual(split_translations("a"), ("a","a"))
def test_php_id_list(self): ...
def test_panel_code(self):
    self.assertEqual(parse_panel_code("CH5-01"), ("CH",5,"CH5-01")); self.assertEqual(parse_panel_code("Q3-101"), ("Q",3,"Q3-101"))
    self.assertEqual(parse_panel_code("G3-01 ."), ("G",3,"G3-01")); self.assertIsNone(parse_panel_code("наружный угол"))
def test_import_counts_and_duplicate(self): # panellar soni to'g'ri; G3-01 ochiq; G3-01-2 is_published=False
def test_import_translations_and_inlines(self): # Advantage, Layer, MontageStep uz va ru bilan
def test_import_idempotent(self): # 2 marta: sonlar o'zgarmaydi
def test_reimport_keeps_admin_edits(self): # panel description o'zgartirildi, qayta import o'zgartirmaydi
def test_copper_photo_hidden(self): # 11.jpg Project is_published=False
def test_missing_file_skipped_and_reported(self): # xatosiz tugaydi, stdout da fayl nomi bor
def test_no_users_imported(self): self.assertEqual(User.objects.count(), 0)
```

Rasmlarni test vaqtinchalik papkada Pillow bilan yaratadi, `MEDIA_ROOT` vaqtinchalik papkaga almashtiriladi.

- [ ] **Step 3: Test FAIL ekanini tekshirish** — Run: `.venv/Scripts/python manage.py test apps.core.tests.test_import`. Expected: ImportError.

- [ ] **Step 4: Parser, seed va buyruqni yozish**

`parser.py`: holat mashinasi bilan belgi-belgi o'qiydi (satr ichida `\\` va `''` qochiriladi, `NULL` → `None`, raqamlar son). Regex bilan qator bo'lish taqiqlanadi, chunki matnlarda `),(` uchrashi mumkin. Fayl `utf-8` da o'qiladi.

`seed.py`: `PATTERNS` (1 Mayda g'isht/Мелкий кирпич, 2 Ingichka g'isht/Тонкий кирпич, 3 Tekis tekstura/Гладкая текстура, 4 Keng panel/Широкая панель, 5 Yirik tosh/Крупный камень, 6 Chiziqli/Линейная), `COLORS` (spec 7-bo'limi jadvali, ru nomlari tarjima bilan). `HOME_COPY`: `hero_kicker` "01 — FASAD PANELLARI"/"01 — ФАСАДНЫЕ ПАНЕЛИ", `hero_title` "Uyingizning yuzi o'zgarsin"/"Новый облик вашего дома", `hero_text` "Po'lat, poliuretan va folga — bir panelda chiroy va issiqlik."/"Сталь, пенополиуретан и фольга — красота и тепло в одной панели.", `layers_title` "Uch qatlam — bitta panel", `adv_title` "To'qqiz sabab", `catalog_title` "Naqshingizni tanlang", `projects_title` "Bizning panellar binolarda", `videos_title` "O'z ko'zingiz bilan ko'ring", `montage_title` "Uch qadamda", `form_title` "Narxini bilib oling" va ularning ruscha tarjimasi. Kichik sarlavhalar eski ACF `*_title` dan. `STATS`: `3,8 kg/m²` "yengil — poydevorga yuk yo'q", `16 mm` "poliuretan issiqlik qatlami", `auto_panel_count=True` "panel", `50 yil` "xizmat muddati".

Buyruq xaritasi: panellar va aksessuarlar 16-post `products` tartibida; `_wp_attached_file` orqali fayl; kontaktlar 12-post `contact_*`; ijtimoiy tarmoqlar 8-post `header_*`; matnlar 8-post `what_*`, `offer_offers_N_*`, `montage_components_N_*`; 10-post `post_content` → `AboutPage`; loyihalar 8-post `slider_images`, keyin 14-post `works`, `wp_id` takrorlanmaydi; `montage_img` va `slider` birinchi rasmi `hero_image`. Mavjud yozuvlar `get_or_create` bilan himoyalanadi. Singletonlar faqat `hero_title_uz` bo'sh bo'lsa to'ldiriladi. `Color`, `Pattern` kod bo'yicha yaratiladi. `SiteSettings.map_url` boshlang'ich qiymati: `https://yandex.uz/map-widget/v1/?text=` + manzilning URL-kodlangan shakli. `panel specs`: 0.3, 16, 3.8, 50.

- [ ] **Step 5: Testlarni tekshirish** — Run: `.venv/Scripts/python manage.py test apps.core.tests.test_import`. Expected: hammasi PASS.

- [ ] **Step 6: Haqiqiy dump bilan sinash**

Run: `.venv/Scripts/python manage.py import_wordpress --sql D:/claude/metal-apex/metalap1_site.sql --uploads D:/claude/metal-apex/public_html/wp-content/uploads`.
Expected: `Panel: 67`, `Aksessuar: 15`, `Video: 6`, o'tkazib yuborilgan fayl 0 ta.
Run: `.venv/Scripts/python manage.py shell -c "from apps.catalog.models import Panel; print(Panel.objects.published().count())"`. Expected: `66`.

- [ ] **Step 7: Commit** — `feat: WordPress dumpidan import buyrug'i`

---

### Task 4: Bosh sahifa

**Files:**
- Create: `apps/core/views.py`, `apps/core/urls.py`, `templates/core/home.html`, `templates/includes/{lead_form,panel_card,video_card}.html`
- Modify: `static/css/site.css`, `static/js/site.js`, `config/urls.py`
- Test: `apps/core/tests/test_home.py`

**Interfaces:**
- Consumes: Task 2 modellari. `leads:submit` nomi Task 6 da yaratiladi, shu sababli Task 4 shablonida forma qo'shilmaydi, `includes/lead_form.html` Task 6 da to'ldiriladi va `home.html` ga shu yerda `{% include %}` qilinadi (hozircha bo'sh fayl).
- Produces: `core:home`. `includes/panel_card.html` (kontekst `panel`), `includes/lead_form.html` (kontekst `lead_form`, ixtiyoriy `panel_code`).

- [ ] **Step 1: Failing testlar**

```python
def test_empty_database_renders(self):
    for lang in ("uz","ru"): self.assertEqual(self.client.get(f"/{lang}/").status_code, 200)
def test_empty_sections_hidden(self): self.assertNotContains(self.client.get("/uz/"), 'id="hamkorlar"')
def test_partners_shown_when_present(self): # Partner qo'shilgach id="hamkorlar" bor
def test_auto_stat_counts_published_only(self): # 2 ochiq, 1 yopiq panel: stat qiymati "2"
def test_sample_shows_four_panels_with_total(self): # 5 panel: 4 kartochka va "Barcha 5" matni
def test_russian_content(self): # hero_title_ru /ru/ da chiqadi
def test_video_loads_only_on_click(self): # sahifada <iframe yo'q, data-youtube-id bor
def test_only_published_projects(self): ...
```

- [ ] **Step 2: Test FAIL ekanini tekshirish** — Run: `.venv/Scripts/python manage.py test apps.core.tests.test_home`. Expected: FAIL.

- [ ] **Step 3: View, shablon va uslub**

`home(request)` kontekst: `home`, `stats`, `panels` (birinchi 4 ochiq), `panel_total`, `patterns`, `projects` (birinchi 5 ochiq), `videos`, `partners`, `lead_form`. Tuzilish `bosh-sahifa-v3.html` dan aynan, 2-bo'lim maketdagi 82 o'rniga hisoblangan son. Har bo'lim ma'lumoti bo'lsagina chiziladi, `id` lar: `hamkorlar`, `videolar`, `loyihalar`, `katalog-namuna`. Rasm `image_card`/`image_large.url`, `alt` kod va naqsh nomi. `site.js`: `[data-youtube-id]` bosilganda `youtube-nocookie.com` iframe bilan almashtiriladi, muqova `https://img.youtube.com/vi/<id>/hqdefault.jpg`. Maket izohlari: 4-bo'lim kartochkasiz, sarlavha 21px, matn 14px, raqam 16px; 8-bo'lim rasm eng ko'pi 340px; 9-bo'lim quti `width:50%`, `aspect-ratio:3/2`.

- [ ] **Step 4: Testlarni tekshirish** — Run: `.venv/Scripts/python manage.py test apps.core.tests.test_home`. Expected: PASS.

- [ ] **Step 5: Commit** — `feat: bosh sahifa`

---

### Task 5: Katalog va panel sahifasi

**Files:**
- Create: `apps/catalog/{filters,views,urls}.py`, `templates/catalog/{list,_grid,accessories,detail}.html`, `static/js/catalog.js`
- Modify: `config/urls.py`, `static/css/site.css`
- Test: `apps/catalog/tests/test_views.py`

**Interfaces:**
- Consumes: `Panel.objects.published()`, `includes/panel_card.html`, `includes/lead_form.html`.
- Produces: `catalog:list`, `catalog:accessories`, `catalog:detail` (`code`). `filter_panels(qs, naqsh: str | None, rang: str | None) -> QuerySet`.

- [ ] **Step 1: Failing testlar**

```python
def test_filter_by_pattern_and_color(self): # ?naqsh=5, ?rang=E, ikkalasi: to'g'ri to'plam
def test_filter_ignores_garbage(self):
    r = self.client.get("/uz/katalog/", {"naqsh":"abc","rang":"<script>"}); self.assertEqual(r.status_code,200)
    self.assertEqual(len(r.context["panels"]), PUBLISHED); self.assertNotContains(r, "<script>alert")
def test_hidden_panel_absent_and_404(self): # /uz/katalog/g3-01-2/ 404
def test_detail_case_insensitive(self): # e5-01 va E5-01 ikkalasi 200
def test_detail_two_letter_code(self): # ch5-01 200
def test_detail_shows_specs_and_siblings(self): # "0,3 mm", "16 mm", "3,8 kg/m²"; bir naqshdagi panellar, eng ko'pi 6, joriy panel birinchi
def test_optional_dimensions_hidden_when_empty(self): # length_mm bo'sh: "Uzunligi" yo'q
def test_ajax_returns_grid_only(self): # X-Requested-With: fetch bilan <html yo'q
def test_only_used_colors_listed(self): ...
def test_accessories_page(self): # faqat ochiq aksessuarlar
```

- [ ] **Step 2: Test FAIL ekanini tekshirish** — Run: `.venv/Scripts/python manage.py test apps.catalog.tests.test_views`. Expected: FAIL.

- [ ] **Step 3: View, shablon va JavaScript**

Tuzilish `katalog.html` dan. `filter_panels`: `naqsh` raqam bo'lmasa e'tiborsiz, `rang` mavjud `Color.letter` bo'lmasa e'tiborsiz. Filtr chiplari oddiy `<a>`, joriy tanlov saqlanadi. `catalog.js`: chip bosilganda `fetch` (`X-Requested-With: fetch`), `#grid` almashtiriladi, `history.pushState`. Sonlar va ko'rsatkichlar `SiteSettings` dan, o'nli vergul bilan. Detail: `code__iexact`, `get_object_or_404(published)`. Boshqa ranglar joriy panel bilan bitta `pattern`da. "Narxini so'rash" sahifadagi `#buyurtma` formaga olib boradi, forma `panel_code` bilan.

- [ ] **Step 4: Testlarni tekshirish** — Run: `.venv/Scripts/python manage.py test apps.catalog.tests.test_views`. Expected: PASS.

- [ ] **Step 5: Commit** — `feat: katalog, filtr va panel sahifasi`

---

### Task 6: Buyurtma formasi va Telegram

**Files:**
- Create: `apps/leads/{forms,views,urls,telegram,throttle}.py`, `templates/leads/{form_page,thanks}.html`
- Modify: `templates/includes/lead_form.html`, `apps/leads/admin.py`, `config/urls.py`, `apps/core/views.py`, `apps/catalog/views.py`
- Test: `apps/leads/tests/test_leads.py`

**Interfaces:**
- Consumes: `Lead`, `Panel`.
- Produces: `leads:submit`, `leads:thanks`. `LeadForm` (`name`, `phone`, `company`, `panel_code` yashirin, `website` yashirin spam tuzog'i). `send_lead(lead: Lead) -> tuple[bool, str]` (xato matnida token bo'lmaydi). `is_throttled(ip: str) -> bool` (10 daqiqada 5 tadan ortiq). `client_ip(request) -> str` (`TRUST_PROXY` yoqilganda `X-Forwarded-For` ning oxirgi qiymati, aks holda `REMOTE_ADDR`).

- [ ] **Step 1: Failing testlar**

```python
@override_settings(TELEGRAM_BOT_TOKEN="123:SECRET", TELEGRAM_CHAT_ID="-100")
class LeadTests(TestCase):
    def test_valid_saves_sends_and_redirects(self): # requests.post soxta; 302 /uz/buyurtma/qabul/; Lead.telegram_sent True
    def test_message_text(self): # json["text"] da "Yangi buyurtma", "Ism: Ali", "Telefon: ...", "Panel: E5-01", "Til: uz"; parse_mode yo'q; timeout=5
    def test_phone_formats(self):
        for ok in ("+998 90 123-45-67","901234567","(90) 123 45 67"): self.assertTrue(form(ok).is_valid(), ok)
        for bad in ("salom","123","+998abc4567"): self.assertFalse(form(bad).is_valid(), bad)
    def test_invalid_keeps_values_and_shows_error(self): # 200, kiritilgan ism sahifada, Lead yo'q
    def test_honeypot_silent(self): # website to'ldirilgan: 302 qabul sahifasi, Lead yo'q, post chaqirilmadi
    def test_throttle(self): # 6-yuborish 429, xato matni bor, Lead 5 ta
    def test_telegram_failure_still_succeeds(self): # post ConnectionError: 302; telegram_sent False; telegram_error to'la
    def test_error_never_contains_token(self): # ConnectionError(".../bot123:SECRET/...") : "SECRET" telegram_error da yo'q
    def test_unconfigured_telegram(self): # token bo'sh: 302, Lead saqlanadi, post chaqirilmaydi
    def test_unknown_panel_code(self): # panel None, xato yo'q
    def test_panel_code_snapshot_survives_delete(self): # panel o'chirildi: panel_code qoladi
    def test_admin_resend_action(self): # telegram_sent False yozuv uchun amal ishlaydi va True bo'ladi
    def test_csrf_enforced(self): # Client(enforce_csrf_checks=True) 403
```

- [ ] **Step 2: Test FAIL ekanini tekshirish** — Run: `.venv/Scripts/python manage.py test apps.leads`. Expected: FAIL.

- [ ] **Step 3: Forma, view va Telegram**

Telefon qoidasi: `^\+?[\d\s()\-]{7,20}$` va kamida 9 raqam. Oqim spec 8-bo'limi bo'yicha: bazaga yozish, keyin yuborish. `send_lead` `requests.post(url, json={"chat_id":…,"text":…}, timeout=5)`. Xatolikda faqat xato sinfi nomi va HTTP holati saqlanadi, manzil saqlanmaydi. Xato bo'lsa `form_page.html` bog'langan forma bilan. Forma maketdagi qora blok. `source_url` `HTTP_REFERER` ning 500 belgisi. `language` joriy til. Bosh sahifa, panel sahifasi va aloqa kontekstiga `lead_form` qo'shiladi.

- [ ] **Step 4: Testlarni tekshirish** — Run: `.venv/Scripts/python manage.py test apps.leads`. Expected: PASS.

- [ ] **Step 5: Commit** — `feat: buyurtma formasi va Telegram`

---

### Task 7: Qolgan sahifalar, yo'naltirishlar va SEO

**Files:**
- Create: `apps/projects/{views,urls}.py`, `templates/projects/list.html`, `templates/core/{about,contact}.html`, `templates/404.html`, `templates/500.html`, `apps/core/sitemaps.py`
- Modify: `apps/core/views.py`, `apps/core/urls.py`, `config/urls.py`, `templates/base.html`, `static/js/site.js`, `static/css/site.css`
- Test: `apps/core/tests/test_pages.py`

**Interfaces:**
- Consumes: Oldingi tasklardagi view nomlari va `lead_form`.
- Produces: `projects:list`, `core:about`, `core:contact`.

- [ ] **Step 1: Failing testlar**

```python
def test_old_urls_redirect_permanently(self):
    for old, new in [("/products/","/uz/katalog/"),("/works/","/uz/loyihalar/"),("/about/","/uz/mahsulot-haqida/"),("/contact/","/uz/aloqa/"),
                     ("/glavnaya/","/uz/"),("/ru/products/","/ru/katalog/"),("/ru/works/","/ru/loyihalar/"),("/ru/about/","/ru/mahsulot-haqida/"),("/ru/contact/","/ru/aloqa/"),("/ru/glavnaya/","/ru/")]:
        r = self.client.get(old); self.assertEqual((r.status_code, r["Location"]), (301, new))
def test_pages_open_on_empty_db(self): # /uz va /ru: loyihalar, mahsulot-haqida, aloqa 200
def test_project_caption_only_when_set(self): ...
def test_contact_shows_details_and_map(self): # telefon, email, map_url iframe; map_url bo'sh: iframe yo'q
def test_404_styled(self): # mavjud bo'lmagan sahifa: 404, "METAL APEX" bor
def test_seo_tags(self): # hreflang uz va ru, og:title, meta description
def test_sitemap_and_robots(self): # sitemap ichida ochiq panel bor, yopiq yo'q; robots /boshqaruv/ ni taqiqlaydi
```

- [ ] **Step 2: Test FAIL ekanini tekshirish** — Run: `.venv/Scripts/python manage.py test apps.core.tests.test_pages`. Expected: FAIL.

- [ ] **Step 3: Sahifalar, yo'naltirish va SEO**

Yo'naltirishlar `i18n_patterns` dan oldin `RedirectView(permanent=True)`. Loyihalar: setka, `<dialog>` bilan to'liq ekran (`site.js`). Aloqa: manzil, 2 telefon, 2 email, forma, `map_url` iframe. Mahsulot haqida: `AboutPage.body` `|safe` (faqat admin kiritadi). `base.html`: `hreflang`, `og:*`, `description` bloki. `sitemap.xml` statik sahifalar va ochiq panellar. `robots.txt` `/boshqaruv/` ni taqiqlaydi va sitemap manzilini ko'rsatadi.

- [ ] **Step 4: Testlarni tekshirish** — Run: `.venv/Scripts/python manage.py test`. Expected: barcha testlar PASS.

- [ ] **Step 5: Commit** — `feat: loyihalar, aloqa, yo'naltirishlar va SEO`

---

### Task 8: Yakuniy tekshiruv va hujjat

**Files:**
- Create: `README.md`, `.claude/launch.json`
- Modify: `.env.example`

- [ ] **Step 1: README**

Mahalliy ishga tushirish (`venv`, `pip install`, `.env`, `migrate`, `createcachetable`, `import_wordpress`, `createsuperuser`, `runserver`), test bot va guruhni ulash, spec 12-bo'limidagi ishga tushirish tartibi va `.env` da almashtiriladigan ikkita Telegram qiymati.

- [ ] **Step 2: Dev serverni preview bilan ochish**

`.claude/launch.json` da `.venv/Scripts/python manage.py runserver 8000` (`name: metal-apex`). `preview_start` bilan ochiladi.

- [ ] **Step 3: Brauzerda tekshirish**

Bosh sahifa, katalog, filtr, panel, loyihalar, aloqa, ruscha versiya 1280 va 375 piksel kenglikda. Tekshiriladi: konsolda xato yo'q, buzilgan rasm yo'q, `document.scrollingElement.scrollWidth <= clientWidth`, maketga mosligi. Skrinshot olinadi.

- [ ] **Step 4: Haqiqiy Telegram sinovi**

Foydalanuvchi `.env` ga test bot tokeni va test guruh ID'sini o'zi yozadi. Formadan bitta buyurtma yuboriladi. Expected: xabar test guruhga keladi, adminda `telegram_sent=True`.

- [ ] **Step 5: Admin hisobi**

Foydalanuvchi `createsuperuser` buyrug'ini o'zi ishga tushiradi va parolni o'zi kiritadi. Admin'da panel tahrirlanib saytda o'zgarishi ko'rinadi.

- [ ] **Step 6: Yakuniy testlar**

Run: `.venv/Scripts/python manage.py test` va `.venv/Scripts/python manage.py check --deploy` (`PRODUCTION=True` bilan). Expected: testlar PASS. `check --deploy` da faqat HSTS subdomen va preload ogohlantirishlari (`security.W005`, `security.W021`) qolishi mumkin, chunki ular ataylab yoqilmagan.

- [ ] **Step 7: Commit** — `docs: README va ishga tushirish sozlamalari`
