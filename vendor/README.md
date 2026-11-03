# vendor

Сторонние файлы, которые раньше грузились с `cdn.jsdelivr.net`. Приложение —
PWA, которой нужно работать в зале без сети, а недоступность CDN делала
страницу пустой. Теперь эти файлы лежат здесь и попадают в кэш service worker
вместе с остальным приложением.

| Файл | Что это | Версия | Лицензия |
|---|---|---|---|
| `supabase.js` | UMD-сборка `@supabase/supabase-js` (`dist/umd/supabase.js`) | 2.118.0 | MIT, `supabase-js-LICENSE` |
| `tabler-icons-subset.woff2` | подмножество Tabler Icons: только используемые иконки | 3.19.0 | MIT, `tabler-icons-LICENSE` |
| `tabler-icons-subset.css` | `@font-face` и правила для них | 3.19.0 | MIT, `tabler-icons-LICENSE` |

Шрифт и CSS сгенерированы: полный webfont — 864 КБ woff2 плюс 237 КБ CSS ради
~5800 иконок, из которых приложению нужны десятки. Подмножество — 8.5 КБ.

Добавили в разметку новую иконку `ti-...`? Перегенерируйте:

```bash
pip install "fonttools[woff]"
python3 tools/build-icon-font.py
```

Скрипт сам находит используемые иконки в `index.html`, забирает апстрим-пакет из
npm и переписывает оба файла. `supabase.js` обновляется вручную:
`npm pack @supabase/supabase-js@2` и копирование `dist/umd/supabase.js`.
При смене версии поднимите `CACHE` в `sw.js`.
