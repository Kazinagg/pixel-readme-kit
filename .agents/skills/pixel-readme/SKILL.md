---
name: pixel-readme
description: "Use this skill whenever the user asks to create, format, style, or upgrade a GitHub README, profile README, or repository documentation in the retro-cyberpunk / pixel-HUD aesthetic (Kazinagg signature style). Covers 3 Global Styles (Cyberpunk, Tactical Military, Minimal Glass), SVG generator CLI, markdown compiler with directives, multi-mode theming (auto, dark, light, transparent, gh, picture), 100% full-width table wrappers, quote headers, and Camo-proxy compatibility."
---

# Pixel Readme Kit v3.0 — Signature HUD Design System & Generator

Этот навык используется AI-агентом для проектирования, стилизации и автоматической сборки GitHub README и профилей в фирменной эстетике **Kazinagg Cyberpunk / Pixel HUD**.

---

## 🏛️ Фундаментальные принципы архитектуры

1. **Разделение Геометрии и Цвета**:
   - Существует ровно **3 глобальных стиля геометрии**: `cyberpunk`, `tactical`, `minimal`.
   - **Цветовая палитра (`primary` + `accent`)** полностью независима от формы: пользователь может выбрать тактический стиль и покрасить его в бирюзовый или фиолетовый.
2. **Адаптивная мульти-режимность (Multi-Mode Theming)**:
   - `mode="auto"` (**по умолчанию**): единый автономный SVG с нативными CSS-переменными и медиа-запросом `@media (prefers-color-scheme: dark)`. Переключается мгновенно вместе с системной темой ОС или браузера, без дублирования файлов.
   - `mode="dark"`: всегда тёмная контрастная тема.
   - `mode="light"`: всегда светлая высококонтрастная тема.
   - `mode="transparent"`: тёмные элементы на полностью прозрачном фоне (без подложки).
   - `mode="gh"`: официальный синтаксис GitHub с генерацией пары файлов (`-dark.svg` и `-light.svg`) и атрибутами `#gh-dark-mode-only` / `#gh-light-mode-only`.
   - `mode="picture"`: тег HTML5 `<picture>` с источниками `(prefers-color-scheme: dark)` и `(prefers-color-scheme: light)`.
3. **Anti-Collision Engine (Защита от наложения текста)**:
   - Интеллектуальный расчет раскладки шрифта: длинные заголовки плавно уменьшают размер пикселя (`px=6 ➔ 5 ➔ 4 ➔ 3`) и аккуратно переносятся на 2 строки по границам слов.
   - Плашка подзаголовка рассчитывается динамически по ширине текста.
   - Тег статуса привязан к правому краю (`text-anchor="end"`), исключая столкновение с кнопками управления окна `[ _ ] [ □ ] [ × ]`.
4. **100% Живой Markdown-текст**:
   - Текст внутри окон, цитат и терминалов остаётся копируемым Markdown, формулы — KaTeX/LaTeX, ссылки кликабельны.

---

## 📐 3 Глобальных стиля

| Характеристика | 🟢 Cyberpunk Terminal | 🟡 Tactical Military HUD | 🟣 Minimal Glass |
| :--- | :--- | :--- | :--- |
| **Геометрия формы** | Прямые углы, открытые скобы (Brackets), угловые пиксели `3×3` | 45° срезанные фаски (Chamfers), тактический октагон, шевроны `▲` | Ультратонкая волосяная рамка 1px (Hairline), зацепы `┌ ┐ └ ┘` |
| **Стиль распада (Decay)** | **Матричный пиксельный дизеринг** (`3×3 ➔ 2×2 ➔ 1×1`) | **Диагональные полосы фасок `///`** (убывающие по высоте и alpha) | **Микроточечное рассеивание** (микро-stipple точки и тающая шина) |
| **Интеграция таблицы** | Прямое накрытие 1-ячеечной таблицы зубцами `x=1..849` | Прямое накрытие таблицы фасками без адаптеров | Монолитная 3-строчная таблица без двойных рамок (`table_minimal`) |
| **Анимация** | 360° радар, CRT-сканлайн, бегущий по плате PCB-пакет | Пульсирующий прицельный лазер, маркеры целей | Спектральный частотный эквалайзер, точечные маяки |
| **Канонический цвет** | Cyan (`#00C8D7`) + Purple (`#A855F7`) | Amber (`#F59E0B`) + Orange (`#EA580C`) | Tokyo Blue (`#4F8BFF`) + Magenta (`#A855F7`) |

---

## 📏 Safe Text Budgets (Безопасные лимиты текста для AI-моделей)

Чтобы сгенерированные блоки выглядели идеально и не ломали композицию:

| Элемент | Рекомендуемый бюджет | Поведение Anti-Collision Engine |
| :--- | :--- | :--- |
| **Header Title** | **8–16 символов** (1 строка)<br/>**17–32 символов** (2 строки) | При длине до 14 симв. — `px_size=6`. При 15–20 симв. — даунскейлинг до `px=5/4`. При > 20 симв. — перенос на 2 строки по пробелам с автоматическим смещением подзаголовка вниз. При экстремальной длине (> 36 симв.) — обрезка с `...`. |
| **Header Subtitle** | **20–45 символов** | Ширина рамки подзаголовка рассчитывается строго по ширине текста (`sub_w`). |
| **Header Tag** | **6–16 символов** | Заякорен справа с отступом `x=755` (`text-anchor="end"`), защищен от наложения на кнопки окна `[ _ ] [ □ ] [ × ]`. |
| **Specs (L3)** | **до 3 строк по 20–35 симв.** | Формат: `spec1="LABEL: VALUE"`. Размещается строго под подзаголовком. |
| **Window Title** | **15–30 символов** | Префикс `╔═ ` добавляется автоматически. |
| **Callout Subtitle** | **25–60 символов** | Безопасно размещается правее бейджа типа (`NOTE`, `WARNING` и т.д.). |
| **Chip Text** | **6–20 символов** | Ширина чипа рассчитывается автоматически с учётом пиксельных эмодзи и отступов. |

---

## 🛠️ Способ 1: Компилятор Markdown (Рекомендуемый воркфлоу)

Агент создает шаблонный файл `README.template.md` с декларативными директивами `<!-- pixel-kit:... -->` и запускает компилятор.

> [!TIP]
> **Как запустить CLI в любом проекте**:
> - **В стороннем проекте**:
>   ```bash
>   python "<путь_к_папке_скила>/generator/cli.py" compile --input README.template.md --output README.md --assets-dir assets/generated
>   ```
> - **Внутри репозитория `pixel-readme-kit`**:
>   ```bash
>   python -m generator.cli compile --input README.template.md --output README.md --assets-dir assets/generated
>   ```

### Синтаксис директив в Markdown:

Все директивы поддерживают атрибут `mode="auto|dark|light|transparent|gh|picture"` (по умолчанию `auto`).

#### 1. Заглавная шапка (Header)
```markdown
<!-- pixel-kit:header style="cyberpunk" title="PROJECT NAME" subtitle="SYSTEM SPECIFICATION" tag="RELEASE_v3.0" spec1="HUD ARCHITECTURE: TRANSLUCENT GLASS" spec2="THEMING: ADAPTIVE DUAL-THEME SVG" spec3="ANIMATION SUITE: RADAR // SCANLINE" mode="auto" out="assets/header.svg" -->
```

#### 2. Окно с контентом (Window Container)
```markdown
<!-- pixel-kit:window style="tactical" title="TACTICAL CONSOLE" tag="HUD" mode="auto" out_top="assets/top.svg" out_bottom="assets/bottom.svg" -->
#### Живой Markdown контент внутри окна
- Окно накрывает таблицу на 100% ширины.
- Для Minimal Glass компилятор автоматически генерирует 3-строчную единую монолитную таблицу.
<!-- /pixel-kit:window -->
```

#### 3. Интерактивный терминал (Collapsible Details/Summary)
```markdown
<!-- pixel-kit:terminal style="cyberpunk" title="HUD.TERMINAL" state="open" mode="auto" -->
```bash
git clone https://github.com/Kazinagg/pixel-readme-kit.git
```
<!-- /pixel-kit:terminal -->
```

#### 4. Плашка для цитаты (Quote Header Container)
```markdown
<!-- pixel-kit:quote style="cyberpunk" badge="NOTE" title="SPECIFICATION NOTICE" subtitle="Flows into live text" mode="auto" -->
**Живой текст цитаты**: плашка бесшовно открыта слева к серой полосе цитаты `border-left`, а пунктирная нижняя линия направляет внимание в текст.
<!-- /pixel-kit:quote -->
```

#### 5. Закрывающая пластина (Footer)
```markdown
<!-- pixel-kit:footer style="cyberpunk" status="SYSTEM_ONLINE // STANDBY" nav="RETURN TO TOP" mode="auto" -->
```

#### 6. Автономная закрытая плашка (Callout)
```markdown
<!-- pixel-kit:callout style="tactical" type="warning" title="WARNING" subtitle="Important operational parameter" mode="auto" -->
```

#### 7. Разделители и сплиттеры
```markdown
<!-- pixel-kit:divider style="minimal" mode="auto" -->
<!-- pixel-kit:splitter style="tactical" label="[MODULE: AUTH]" mode="auto" -->
```

#### 8. Голографические чипы
```markdown
<!-- pixel-kit:chip style="cyberpunk" type="closed" text="CORE_SYS" href="https://github.com" mode="auto" -->
<!-- pixel-kit:chip style="tactical" type="decay" text="DEF_ALERT" mode="auto" -->
<!-- pixel-kit:chip style="minimal" type="pulse" text="SYNC_IDLE" mode="auto" -->
```

---

## ⚡ Способ 2: Генерация одиночных SVG через CLI

```bash
# Флагманский адаптивный хедер (авто-тема):
python -m generator.cli header --style tactical --title "TACTICAL COMMAND" --subtitle "SECURITY LAYER" --mode auto -o assets/header.svg

# Генерация пары файлов для GitHub (#gh-dark-mode-only):
python -m generator.cli header --style cyberpunk --title "DUAL MODE" --mode gh -o assets/header.svg

# Закрывающий футер:
python -m generator.cli footer --style minimal --status "SESSION_ACTIVE" -o assets/footer.svg

# Плашка алерта или цитаты (--quote):
python -m generator.cli callout --style cyberpunk --type note --title "SYS NOTICE" --quote -o assets/quote-note.svg

# Рамка окна (top или bottom):
python -m generator.cli frame --style minimal --type top --title "╔═ MINIMAL.SYS" -o assets/frame-top.svg

# Чип (closed, decay, pulse):
python -m generator.cli chip --style tactical --type decay --text "SECTOR_01" -o assets/chip-tactical.svg

# Разделитель глав:
python -m generator.cli divider --style minimal -o assets/divider-spectrum.svg

# Сплиттер подмодулей:
python -m generator.cli splitter --style cyberpunk --label "[MODULE: AUTH]" -o assets/splitter.svg
```

---

## ⚠️ Критические правила вёрстки

1. **Запрет `<img>` внутри `<summary>`**:
   - На GitHub веб-клиент вешает обработчик Lightbox на все изображения `<img>`. Если в `<summary>` поместить картинку, клик по ней **открывает SVG в браузере, а не раскрывает блок**.
   - **Правило**: Внутри `<summary>` всегда использовать текстовые теги: `<summary><kbd>▶ TITLE</kbd> <b>[...]</b> <code>[...]</code></summary>`.
2. **Таблицы на 100% ширины**:
   - GitHub сжимает таблицы по содержимому текста (`width: max-content`).
   - **Правило**: Всегда указывать `<table width="100%"><tr><td width="2000">`. Значение `width="2000"` на ячейке `<td>` сообщает браузеру предпочтительную ширину, благодаря чему таблица гарантированно растягивается на все 100% доступной ширины контейнера (`max-width: 100%`), а зубцы крышек садятся ровно на серые рамки.
3. **XML-экранирование**:
   - Неэкранированные символы `&`, `<`, `>` внутри SVG ломают GitHub Camo Proxy.
   - Всегда валидировать SVG через `xml.etree.ElementTree.fromstring()`.
4. **Адаптивный вертикальный поток (DOM-like Flow Layout)**:
   - Высота шапок (`generate_header`) автоматически рассчитывается динамически: при 2-строчных заголовках или наличии спецификаций все нижние блоки плавно съезжают вниз (как `div` в браузере), а сам SVG динамически увеличивает высоту (`viewBox` и шасси), гарантируя запас отступа (clearance $\ge 18-26$px) до нижних линий и скосов.
