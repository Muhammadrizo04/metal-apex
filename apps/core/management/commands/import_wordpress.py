import re
from pathlib import Path
from urllib.parse import quote

from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.catalog.models import Accessory, Color, Panel, Pattern
from apps.core.models import AboutPage, Advantage, HomeContent, Layer, MontageStep, SiteSettings, Stat
from apps.core.wordpress import seed
from apps.core.wordpress.parser import (
    clean_title,
    parse_inserts,
    parse_panel_code,
    php_id_list,
    split_translations,
)
from apps.projects.models import Project, Video

POST_HOME, POST_ABOUT, POST_CONTACT, POST_WORKS, POST_PRODUCTS = 8, 10, 12, 14, 16
_BLOCK = re.compile(r"<(p|ul|ol|h[1-6]|div|table|blockquote)\b", re.I)
_STYLE = re.compile(r"\sstyle=\"[^\"]*\"", re.I)


def _wrap_block(block: str) -> str:
    match = _BLOCK.search(block)
    if not match:
        return "<p>" + block.replace("\n", "<br>") + "</p>"
    before = block[: match.start()].strip()
    return (f"<p>{before}</p>\n" if before else "") + block[match.start() :]


def autop(text: str) -> str:
    """WordPress `the_content` kabi xatboshilarni <p> ga o'raydi."""
    text = _STYLE.sub("", text.replace("\r\n", "\n")).strip()
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text)]
    return "\n".join(_wrap_block(b) for b in blocks if b and b != "&nbsp;")


class Command(BaseCommand):
    help = "Eski WordPress dumpidan matn, panel va rasmlarni import qiladi."

    def add_arguments(self, parser):
        parser.add_argument("--sql", required=True)
        parser.add_argument("--uploads", required=True)

    @transaction.atomic
    def handle(self, *args, **options):
        tables = parse_inserts(Path(options["sql"]).read_text(encoding="utf-8"), {"mx_posts", "mx_postmeta"})
        self.uploads = Path(options["uploads"])
        self.skipped: list[str] = []
        self.posts = {row["ID"]: row for row in tables["mx_posts"]}
        self.meta: dict[int, dict[str, str]] = {}
        for row in tables["mx_postmeta"]:
            self.meta.setdefault(row["post_id"], {})[row["meta_key"]] = row["meta_value"] or ""
        self.files = {pid: m["_wp_attached_file"] for pid, m in self.meta.items() if "_wp_attached_file" in m}

        self._seed_catalog_refs()
        self._import_catalog()
        self._import_projects()
        self._import_videos()
        self._import_home()
        self._import_settings()
        self._import_about()
        self._report()

    def _attach(self, field, wp_id: int) -> bool:
        rel = self.files.get(wp_id, "")
        path = self.uploads / rel
        if not rel or not path.is_file():
            self.skipped.append(rel or f"id={wp_id}")
            return False
        with path.open("rb") as handle:
            field.save(path.name, File(handle), save=False)
        return True

    def _tr(self, post_id: int, key: str) -> tuple[str, str]:
        return split_translations(self.meta.get(post_id, {}).get(key, ""))

    def _plain(self, post_id: int, key: str) -> str:
        return self._tr(post_id, key)[0].strip()

    def _seed_catalog_refs(self):
        for series, (uz, ru) in seed.PATTERNS.items():
            Pattern.objects.get_or_create(series=series, defaults={"name_uz": uz, "name_ru": ru, "order": series})
        for order, (letter, (uz, ru, hex_value)) in enumerate(seed.COLORS.items()):
            Color.objects.get_or_create(
                letter=letter, defaults={"name_uz": uz, "name_ru": ru, "hex": hex_value, "order": order}
            )

    def _import_catalog(self):
        for order, wp_id in enumerate(php_id_list(self.meta[POST_PRODUCTS]["products"])):
            title = str(self.posts.get(wp_id, {}).get("post_title", ""))
            parsed = parse_panel_code(title)
            if parsed:
                self._import_panel(wp_id, order, *parsed)
            else:
                self._import_accessory(wp_id, order, title)

    def _import_panel(self, wp_id, order, letter, series, code):
        if Panel.objects.filter(wp_id=wp_id).exists():
            return
        final_code, published = code, True
        if Panel.objects.filter(code=code).exists():
            final_code, published = f"{code}-2", False
        color, _ = Color.objects.get_or_create(letter=letter, defaults={"name_uz": letter, "name_ru": letter})
        panel = Panel(
            wp_id=wp_id, code=final_code, pattern=Pattern.objects.get(series=series),
            color=color, is_published=published, order=order,
        )
        if self._attach(panel.image, wp_id):
            panel.save()

    def _import_accessory(self, wp_id, order, title):
        if Accessory.objects.filter(wp_id=wp_id).exists():
            return
        uz, ru = split_translations(title)
        item = Accessory(wp_id=wp_id, name_uz=uz.strip(" ,."), name_ru=ru.strip(" ,."), order=order)
        if self._attach(item.image, wp_id):
            item.save()

    def _project_ids(self) -> list[int]:
        ids = php_id_list(self.meta.get(POST_HOME, {}).get("slider_images", ""))
        ids += php_id_list(self.meta.get(POST_WORKS, {}).get("works", ""))
        return list(dict.fromkeys(ids))

    def _import_projects(self):
        seen_files = set()
        for order, wp_id in enumerate(self._project_ids()):
            rel = self.files.get(wp_id, "")
            if rel in seen_files or Project.objects.filter(wp_id=wp_id).exists():
                continue
            seen_files.add(rel)
            project = Project(wp_id=wp_id, order=order, is_published=not rel.endswith(seed.HIDDEN_PROJECT_SUFFIXES))
            if self._attach(project.image, wp_id):
                project.save()

    def _import_videos(self):
        n = 0
        while url := self._plain(POST_HOME, f"works_video_{n}_url"):
            Video.objects.get_or_create(url=url, defaults={"order": n})
            n += 1

    def _hero_source(self) -> int | None:
        ids = self._project_ids()
        for wp_id in ids:
            if self.files.get(wp_id, "").endswith("/1.jpg"):
                return wp_id
        for wp_id in ids:
            if not self.files.get(wp_id, "").endswith(seed.HIDDEN_PROJECT_SUFFIXES):
                return wp_id
        return None

    def _import_home(self):
        home = HomeContent.load()
        if home.hero_title_uz:
            return
        for field, (uz, ru) in seed.HOME_COPY.items():
            setattr(home, f"{field}_uz", uz)
            setattr(home, f"{field}_ru", ru)
        for key, field in seed.HOME_FROM_WP.items():
            uz, ru = self._tr(POST_HOME, key)
            if uz:
                setattr(home, f"{field}_uz", uz)
                setattr(home, f"{field}_ru", ru)
        hero = self._hero_source()
        if hero:
            self._attach(home.hero_image, hero)
        montage = self._plain(POST_HOME, "montage_img")
        if montage.isdigit():
            self._attach(home.montage_image, int(montage))
        home.save()

        for order, item in enumerate(seed.STATS):
            Stat.objects.create(
                home=home, value_uz=item["value"][0], value_ru=item["value"][1], title_uz=item["title"][0],
                title_ru=item["title"][1], auto_panel_count=item.get("auto", False), order=order,
            )
        self._import_children(home, Layer, "what_components_{}_text_{}")
        self._import_children(home, Advantage, "offer_offers_{}_text_{}")
        self._import_children(home, MontageStep, "montage_components_{}_text_{}")

    def _import_children(self, home, model, pattern):
        n = 0
        while True:
            title_uz, title_ru = self._tr(POST_HOME, pattern.format(n, 1))
            if not title_uz:
                return
            text_uz, text_ru = self._tr(POST_HOME, pattern.format(n, 2))
            model.objects.create(
                home=home, title_uz=title_uz, title_ru=title_ru, text_uz=text_uz, text_ru=text_ru, order=n
            )
            n += 1

    def _import_settings(self):
        site = SiteSettings.load()
        if site.phone_1:
            return
        site.address_uz, site.address_ru = self._tr(POST_CONTACT, "contact_address")
        for field in ("phone_1", "phone_2", "email_1", "email_2"):
            setattr(site, field, self._plain(POST_CONTACT, f"contact_{field}"))
        for field in ("facebook", "instagram", "youtube", "telegram", "x"):
            setattr(site, field, self._plain(POST_HOME, f"header_{field}"))
        site.map_url = seed.MAP_BASE + quote(site.address_uz) if site.address_uz else ""
        for field, value in seed.PANEL_SPECS.items():
            setattr(site, field, value)
        site.save()

    def _import_about(self):
        about = AboutPage.load()
        if about.body_uz or POST_ABOUT not in self.posts:
            return
        post = self.posts[POST_ABOUT]
        about.title_uz, about.title_ru = split_translations(str(post["post_title"]))
        uz, ru = split_translations(str(post["post_content"]))
        about.body_uz, about.body_ru = autop(uz), autop(ru)
        about.save()

    def _report(self):
        self.stdout.write(f"Panel: {Panel.objects.count()}")
        self.stdout.write(f"Aksessuar: {Accessory.objects.count()}")
        self.stdout.write(f"Loyiha: {Project.objects.count()}")
        self.stdout.write(f"Video: {Video.objects.count()}")
        self.stdout.write(f"O'tkazib yuborilgan fayl: {len(self.skipped)}")
        for rel in self.skipped:
            self.stdout.write(f"  {rel}")
