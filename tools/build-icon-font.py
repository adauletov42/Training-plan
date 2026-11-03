#!/usr/bin/env python3
"""Собрать подмножество шрифта Tabler Icons из иконок, которые реально
использует index.html.

Полный @tabler/icons-webfont — это woff2 на 864 КБ и CSS на 237 КБ ради
~5800 иконок, из которых приложению нужны несколько десятков. Скрипт берёт
апстрим-пакет из npm, вытаскивает коды только используемых иконок и пишет
vendor/tabler-icons-subset.woff2 и vendor/tabler-icons-subset.css.

Запускать после того, как в разметке появилась новая иконка `ti-...`:

    pip install "fonttools[woff]"
    python3 tools/build-icon-font.py

Результат коммитится в репозиторий: самому приложению сборка не нужна,
оно остаётся набором статических файлов.
"""
import json
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

VERSION = "3.19.0"
ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "index.html"
OUT_DIR = ROOT / "vendor"
OUT_WOFF2 = OUT_DIR / "tabler-icons-subset.woff2"
OUT_CSS = OUT_DIR / "tabler-icons-subset.css"


def used_icons(html: str) -> list[str]:
    names = {m for m in re.findall(r"\bti-[a-z0-9-]+", html)}
    return sorted(names)


def fetch_upstream(tmp: Path) -> Path:
    subprocess.run(
        ["npm", "pack", f"@tabler/icons-webfont@{VERSION}"],
        cwd=tmp, check=True, stdout=subprocess.DEVNULL,
    )
    tgz = next(tmp.glob("*.tgz"))
    with tarfile.open(tgz) as tf:
        tf.extractall(tmp / "pkg", filter="data")
    return tmp / "pkg" / "package" / "dist"


def main() -> int:
    if not HTML.exists():
        sys.exit(f"не найден {HTML}")
    icons = used_icons(HTML.read_text(encoding="utf-8"))
    if not icons:
        sys.exit("в index.html не найдено ни одной иконки ti-*")

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        dist = fetch_upstream(tmp)
        css = (dist / "tabler-icons.min.css").read_text(encoding="utf-8")

        codes: dict[str, str] = {}
        for name in icons:
            m = re.search(r"\.%s:before\{content:\"\\([0-9a-fA-F]+)\"\}" % re.escape(name), css)
            if m:
                codes[name] = m.group(1)

        missing = [n for n in icons if n not in codes]
        if missing:
            sys.exit("нет таких иконок в Tabler %s: %s" % (VERSION, ", ".join(missing)))

        OUT_DIR.mkdir(exist_ok=True)
        unicodes = ",".join("U+" + c for c in sorted(set(codes.values())))

        # Апстрим-шрифт несёт таблицу лигатур (ti + имя иконки), на которой
        # fontTools падает с AssertionError в разборе GSUB, и --drop-tables
        # не помогает: разбор происходит при загрузке. Приложение адресует
        # иконки кодами, лигатуры ему не нужны, поэтому таблицы раскладки
        # снимаются до сабсеттинга.
        from fontTools.ttLib import TTFont

        stripped = tmp / "stripped.ttf"
        font = TTFont(dist / "fonts" / "tabler-icons.ttf", lazy=True)
        for table in ("GSUB", "GPOS", "DSIG"):
            if table in font:
                del font[table]
        font.save(stripped)

        subprocess.run([
            sys.executable, "-m", "fontTools.subset", str(stripped),
            f"--unicodes={unicodes}",
            "--flavor=woff2",
            "--no-hinting",
            "--desubroutinize",
            f"--output-file={OUT_WOFF2}",
        ], check=True)

        shutil.copyfile(dist.parent / "LICENSE", OUT_DIR / "tabler-icons-LICENSE")

    rules = "\n".join(
        '.%s:before { content: "\\%s"; }' % (name, codes[name])
        for name in sorted(codes)
    )
    OUT_CSS.write_text(
        f"""/* Подмножество Tabler Icons {VERSION} — {len(codes)} иконок,
   собрано tools/build-icon-font.py из иконок, используемых в index.html.
   Лицензия апстрима: MIT, см. vendor/tabler-icons-LICENSE.
   Файл сгенерирован: править руками не нужно, перегенерируйте скриптом. */
@font-face {{
  font-family: "tabler-icons";
  font-style: normal;
  font-weight: 400;
  font-display: block;
  src: url("tabler-icons-subset.woff2") format("woff2");
}}
.ti {{
  font-family: "tabler-icons" !important;
  speak: none;
  font-style: normal;
  font-weight: normal;
  font-variant: normal;
  text-transform: none;
  line-height: 1;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}}
{rules}
""",
        encoding="utf-8",
    )
    print(f"иконок: {len(codes)}")
    print(f"{OUT_WOFF2.relative_to(ROOT)}: {OUT_WOFF2.stat().st_size} байт")
    print(f"{OUT_CSS.relative_to(ROOT)}: {OUT_CSS.stat().st_size} байт")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
