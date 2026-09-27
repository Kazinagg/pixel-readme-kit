---
name: pixel-readme
description: "Use this skill whenever the user asks to create, format, style, or upgrade a GitHub README, profile README, or repository documentation in the retro-cyberpunk / pixel-HUD aesthetic (Kazinagg signature style). Covers 3 Global Styles (Cyberpunk, Tactical Military, Minimal Glass), SVG generator CLI, markdown compiler with directives, translucent dark glass, 100% full-width table wrappers, quote headers, and Camo-proxy compatibility."
---

# Pixel Readme Kit v2.2 — Signature HUD Design System & Generator

Этот навык используется AI-агентом для проектирования, стилизации и автоматической сборки GitHub README и профилей в фирменной эстетике **Kazinagg Cyberpunk / Pixel HUD**.

---

## 🏛️ Фундаментальные принципы архитектуры

1. **Разделение Геометрии и Цвета**:
   - Существует ровно **3 глобальных стиля геометрии**: `cyberpunk`, `tactical`, `minimal`.
   - **Цветовая палитра (`primary` + `accent`)** полностью независима от формы: пользователь может выбрать тактический стиль и покрасить его в бирюзовый или фиолетовый.
2. **True Alpha Blending (Контрастность на темной и светлой темах)**:
   - Все компоненты имеют темную полупрозрачную подложку `rgba(10, 14, 23, 0.85)` / `0.88` / `0.82`.
   - Гарантирует контрастность выше 7:1 как на темном фоне GitHub (`#0d1117`), так и на белом (`#ffffff`).
3. **100% Живой Markdown-текст**:
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

## 🛠️ Способ 1: Компилятор Markdown (Рекомендуемый агентский рабочий процесс)

Агент создает шаблонный файл `README.template.md` с декларативными директивами `<!-- pixel-kit:... -->` и запускает компилятор.

> [!TIP]
> **Как запустить CLI в любом проекте**:
> Модуль `generator/` поставляется прямо внутри директории этого скила (там же, где находится данный `SKILL.md`).
> - **В стороннем проекте**: вызывайте CLI через абсолютный/относительный путь к `generator/cli.py` скила:
>   ```bash
>   python "<путь_к_папке_скила>/generator/cli.py" compile --input README.template.md --output README.md --assets-dir assets/generated
>   ```
> - **Внутри репозитория `pixel-readme-kit`**:
>   ```bash
>   python -m generator.cli compile --input README.template.md --output README.md --assets-dir assets/generated
>   ```

### Синтаксис директив в Markdown:

#### 1. Заглавная шапка (Header)
```markdown
<!-- pixel-kit:header style="cyberpunk" title="PROJECT NAME" subtitle="SYSTEM SPECIFICATION" tag="v2.2" spec1="HUD ARCHITECTURE: TRANSLUCENT GLASS" spec2="TEXT INTEGRATION: 100% COPYABLE MARKDOWN" spec3="ANIMATION SUITE: RADAR // SCANLINE" out="assets/header.svg" -->
```
> [!NOTE]
> Теги 3-го уровня телеметрии (`spec1`, `spec2`, `spec3` или `specs="A: 1 | B: 2 | C: 3"`) опциональны (максимум 3 штуки). Если их не указать, область под подзаголовком остаётся чистой во всех трёх стилях (`cyberpunk`, `tactical`, `minimal`).

#### 2. Окно с контентом (Window Container)
```markdown
<!-- pixel-kit:window style="tactical" title="TACTICAL CONSOLE" tag="HUD" out_top="assets/top.svg" out_bottom="assets/bottom.svg" -->
#### Живой Markdown контент внутри окна
- Окно накрывает таблицу на 100% ширины.
- Для Minimal Glass компилятор автоматически генерирует 3-строчную единую монолитную таблицу.
<!-- /pixel-kit:window -->
```

#### 3. Интерактивный терминал (Collapsible Details/Summary)
```markdown
<!-- pixel-kit:terminal style="cyberpunk" title="HUD.TERMINAL" state="open" -->
```bash
git clone https://github.com/Kazinagg/pixel-readme-kit.git
```
<!-- /pixel-kit:terminal -->
```

#### 4. Плашка для цитаты (Quote Header Container)
```markdown
<!-- pixel-kit:quote style="cyberpunk" badge="NOTE" title="SPECIFICATION NOTICE" subtitle="Flows into live text" -->
**Живой текст цитаты**: плашка бесшовно открыта слева к серой полосе цитаты `border-left`, а пунктирная нижняя линия направляет внимание в текст.
<!-- /pixel-kit:quote -->
```

#### 5. Закрывающая пластина (Footer)
```markdown
<!-- pixel-kit:footer style="cyberpunk" status="SYSTEM_ONLINE // STANDBY" nav="RETURN TO TOP" -->
```

#### 6. Автономная закрытая плашка (Callout)
```markdown
<!-- pixel-kit:callout style="tactical" type="warning" title="WARNING" subtitle="Important operational parameter" -->
```

#### 7. Разделители и сплиттеры
```markdown
<!-- pixel-kit:divider style="minimal" -->
<!-- pixel-kit:splitter style="tactical" label="[MODULE: AUTH]" -->
```

#### 8. Голографические чипы
```markdown
<!-- pixel-kit:chip style="cyberpunk" type="closed" text="CORE_SYS" -->
<!-- pixel-kit:chip style="tactical" type="decay" text="DEF_ALERT" -->
<!-- pixel-kit:chip style="minimal" type="pulse" text="SYNC_IDLE" -->
```

---

## ⚡ Способ 2: Генерация одиночных SVG через CLI
 
Для генерации конкретного SVG-файла по параметрам (в сторонних проектах замените `python -m generator.cli` на `python "<путь_к_папке_скила>/generator/cli.py"`):

```bash
# Флагманский хедер
python -m generator.cli header --style tactical --title "TACTICAL COMMAND" --subtitle "SECURITY LAYER" -o assets/header.svg

# Закрывающий футер
python -m generator.cli footer --style minimal --status "SESSION_ACTIVE" -o assets/footer.svg

# Плашка алерта или цитаты (--quote)
python -m generator.cli callout --style cyberpunk --type note --title "SYS NOTICE" --quote -o assets/quote-note.svg

# Рамка окна (top или bottom)
python -m generator.cli frame --style minimal --type top --title "╔═ MINIMAL.SYS" -o assets/frame-top.svg

# Чип (closed, decay, pulse)
python -m generator.cli chip --style tactical --type decay --text "SECTOR_01" -o assets/chip-tactical.svg

# Разделитель глав
python -m generator.cli divider --style minimal -o assets/divider-spectrum.svg

# Сплиттер подмодулей
python -m generator.cli splitter --style cyberpunk --label "[MODULE: AUTH]" -o assets/splitter.svg
```

> [!TIP]
> Запустите `python -m generator.cli <subcommand> --help` (например, `callout --help` или `chip --help`), чтобы увидеть полный список параметров для каждого блока.

---

## ⚠️ Критические ограничения GitHub Markdown и Camo Proxy

1. **Запрет `<img>` внутри `<summary>`**:
   - На GitHub веб-клиент вешает обработчик Lightbox на все изображения `<img>`. Если в `<summary>` поместить картинку, клик по ней **открывает SVG в браузере, а не раскрывает блок**.
   - **Правило**: Внутри `<summary>` всегда использовать текстовые теги: `<summary><kbd>▶ TITLE</kbd> <b>[...]</b> <code>[...]</code></summary>`.
2. **Таблицы на 100% ширины**:
   - GitHub сжимает таблицы по содержимому текста.
   - **Правило**: Всегда указывать `<table width="100%"><tr><td width="100%">`.
3. **XML-экранирование**:
   - Неэкранированные символы `&`, `<`, `>` внутри SVG ломают GitHub Camo Proxy.
   - Всегда валидировать SVG через `xml.etree.ElementTree.fromstring()`.
