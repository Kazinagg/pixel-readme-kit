# 💡 PIXEL README KIT — ПРИМЕРЫ И РАБОЧИЙ ПРОЦЕСС (WORKFLOW)

<div id="top"></div>

<div align="center">

<img src="assets/generated/header-tactical-amber.svg" width="100%" alt="Examples & Workflow Header" />

<br/><br/>

<a href="README.md"><img src="assets/generated/chip-cat-home.svg" alt="Главная" /></a>
&nbsp;&nbsp;
<a href="CATALOG.md"><img src="assets/generated/chip-cat-examples.svg" alt="Каталог блоков" /></a>
&nbsp;&nbsp;
<a href="#top"><img src="assets/generated/chip-cat-top.svg" alt="Наверх" /></a>

<br/><br/>

<img src="assets/generated/divider-laser-amber.svg" width="100%" alt="Divider" />

</div>

> [!TIP]
> 🎯 **ГЛАВНАЯ ЦЕЛЬ ДИЗАЙН-СИСТЕМЫ**:
> Избавить разработчика от ручного рисования SVG, выравнивания пикселей и подгонки таблиц под рендерер GitHub.
> Вы пишете обычный декларативный Markdown-шаблон с директивами `<!-- pixel-kit:... -->`, а компилятор превращает его в профессиональный README.

---

## 📑 Оглавление руководства

1. [Как устроен рабочий процесс (Workflow)](#1-как-устроен-рабочий-процесс-workflow)
2. [Часть 1: Шаблон БЕЗ генерации (Исходный текст)](#2-часть-1-шаблон-без-генерации-исходный-текст)
3. [Часть 2: Команда сборки (CLI Command)](#3-часть-2-команда-сборки-cli-command)
4. [Часть 3: Сгенерированный результат (Live Render)](#4-часть-3-сгенерированный-результат-live-render)
5. [Часть 4: Автоматизация через GitHub Actions](#5-часть-4-автоматизация-через-github-actions)

---

## 1. Как устроен рабочий процесс (Workflow)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. ИСХОДНЫЙ ШАБЛОН: EXAMPLE_TEMPLATE.md                    │
│    - Декларативные директивы <!-- pixel-kit:... -->         │
│    - Живой Markdown-текст, списки, таблицы и KaTeX          │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. СБОРКА: python -m generator.cli compile                  │
│    - Генератор автоматически создаёт все SVG в assets/      │
│    - Подгоняет ширину чипов под длину текста                │
│    - Оборачивает контент в 100% таблицы без боковых щелей   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. ГОТОВЫЙ РЕЗУЛЬТАТ: EXAMPLE.md (или README.md)            │
│    - 100% валидный GitHub Flavored Markdown                 │
│    - Идеальный контраст на тёмной и светлой темах           │
│    - Живая CSS-анимация: радар 360°, лазеры, эквалайзеры   │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Часть 1: Шаблон БЕЗ генерации (Исходный текст)

Ниже представлен **реальный исходный код файла шаблона** ([EXAMPLE_TEMPLATE.md](EXAMPLE_TEMPLATE.md)) в сыром текстовом виде, каким его пишет разработчик:

````markdown
<div id="top"></div>

<div align="center">

<!-- pixel-kit:header style="cyberpunk" primary="#00C8D7" accent="#A855F7" title="NEO-CORE" subtitle="CYBER-HUD AUTOMATION & KERNEL RUNTIME" spec1="HUD ARCHITECTURE: TRANSLUCENT GLASS & CYBER BRACKETS" spec2="TEXT INTEGRATION: 100% COPYABLE MARKDOWN & MATH" spec3="ANIMATION SUITE: RADAR // SCANLINE // LADDER CASCADE" tag="SYS_v2.2_ONLINE" out="assets/example/neo-header.svg" -->

<br/><br/>

<!-- pixel-kit:chip style="cyberpunk" type="closed" text="⚡ v2.2.0" out="assets/example/chip-version.svg" -->
&nbsp;&nbsp;
<!-- pixel-kit:chip style="cyberpunk" type="pulse" text="● LIVE_NODE" out="assets/example/chip-status.svg" -->
&nbsp;&nbsp;
<!-- pixel-kit:chip style="minimal" type="closed" text="LICENSE // MIT" out="assets/example/chip-license.svg" -->
&nbsp;&nbsp;
<!-- pixel-kit:chip style="tactical" type="decay" text="SEC: CLEAR" out="assets/example/chip-security.svg" -->

<br/><br/>

<!-- pixel-kit:divider style="cyberpunk" primary="#00C8D7" out="assets/example/divider-top.svg" -->

</div>

<br/>

<!-- 1. АВТОНОМНЫЙ АЛЕРТ (CALLOUT) -->
<!-- pixel-kit:callout style="cyberpunk" type="note" title="RUNTIME ARCHITECTURE // ZERO CAMO PROXY OVERFLOW" subtitle="Dual-theme contrast > 7:1 // Monospace typography" out="assets/example/callout-arch.svg" -->

<br/>

<!-- 2. БЛОК ЦИТАТЫ С ХЕДЕРОМ (QUOTE) -->
<!-- pixel-kit:quote style="tactical" badge="WARNING" title="CRITICAL CONSTRAINT // FULL-WIDTH COMPLIANCE" subtitle="Quote header with open left edge directly connecting into Markdown quote" out="assets/example/callout-quote-warn.svg" -->
**Внимание оператора**: все контентные окна обязаны использовать 100% табличную обертку (`<table width="100%"><tr><td width="2000">...</td></tr></table>`). 
Это гарантирует, что зубцы крышек на `x=1` и `x=849` ложатся ровно на серые рамки GitHub без боковых зазоров на любых дисплеях.
<!-- /pixel-kit:quote -->

<br/>

<!-- 3. ИНТЕРАКТИВНОЕ ОКНО CYBERPUNK (WINDOW) -->
<!-- pixel-kit:window style="cyberpunk" primary="#00C8D7" title="╔═ NEO.KERNEL // CORE_SPECIFICATION.SYS" tag="[ACTIVE_HUD]" out_top="assets/example/frame-top-cyber.svg" out_bottom="assets/example/frame-bottom-cyber.svg" -->
### 🧬 Спецификация ядра системы

Интерфейс спроектирован по канонам ретро-футуризма с полной адаптацией под рендерер GitHub:

| Подсистема | Протокол | Статус | Задержка |
| :--- | :--- | :--- | :--- |
| **Fiber Pipeline** | `IPC_BUS // DMA` | `● ACTIVE` | `0.12 ms` |
| **Translucent Glass** | `SVG_ALPHA_0.82` | `● STABLE` | `0.00 ms` |
| **Live Radar HUD** | `360_DEG_SWEEP` | `● SCANNING` | `16.6 ms (60 FPS)` |

```bash
# Инициализация демо-проекта
npm install neo-kernel-core
npx neo-core --bootstrap
```
<!-- /pixel-kit:window -->

<br/>

<!-- 4. СВОРАЧИВАЕМЫЙ ТЕРМИНАЛ (DETAILS/SUMMARY) -->
<!-- pixel-kit:terminal style="cyberpunk" title="ENVIRONMENT_CONFIGURATION" state="closed" out_top="assets/example/terminal-top-cyber.svg" out_bottom="assets/example/terminal-bottom-cyber.svg" -->
```ini
[RUNTIME]
NODE_ENV=production
HUD_OPACITY=0.82
ACCENT_COLOR=#00C8D7
SECONDARY_COLOR=#A855F7
SCANLINE_FPS=60
```
<!-- /pixel-kit:terminal -->

<br/><br/>

<!-- pixel-kit:footer style="cyberpunk" status="SESSION_ONLINE // READY" nav="▲ НАВЕРХ" out="assets/example/neo-footer.svg" -->
````

---

## 3. Часть 2: Команда сборки (CLI Command)

Чтобы превратить шаблон выше в готовый Markdown и сгенерировать все необходимые SVG-ассеты, выполняется всего одна команда:

```bash
python -m generator.cli compile --input EXAMPLE_TEMPLATE.md --output EXAMPLE.md --assets-dir assets/example
```

**Что делает компилятор**:
- Парсит каждую директиву `<!-- pixel-kit:... -->`.
- Вызывает генератор и сохраняет SVG с уникальными именами в указанную папку `--assets-dir`.
- Рассчитывает точную адаптивную ширину для каждого чипа по количеству символов текста.
- Оборачивает контент окон в таблицы на 100% ширины.
- Заменяет директивы в Markdown на готовые теги `<img>` и форматированные блоки.

---

## 4. Часть 3: Сгенерированный результат (Live Render)

Ниже в реальном времени отображается результат работы компилятора из файла [EXAMPLE.md](EXAMPLE.md):

---

<div align="center">

<img src="assets/example/neo-header.svg" width="100%" alt="NEO-CORE" />

<br/><br/>

<img src="assets/example/chip-version.svg" alt="⚡ v2.2.0" />
&nbsp;&nbsp;
<img src="assets/example/chip-status.svg" alt="● LIVE_NODE" />
&nbsp;&nbsp;
<img src="assets/example/chip-license.svg" alt="LICENSE // MIT" />
&nbsp;&nbsp;
<img src="assets/example/chip-security.svg" alt="SEC: CLEAR" />

<br/><br/>

<img src="assets/example/divider-top.svg" width="100%" />

</div>

<br/>

<!-- 1. АВТОНОМНЫЙ АЛЕРТ (CALLOUT) -->
<img src="assets/example/callout-arch.svg" width="100%" />

<br/>

<!-- 2. БЛОК ЦИТАТЫ С ХЕДЕРОМ (QUOTE) -->
> <img src="assets/example/callout-quote-warn.svg" width="100%" />
>
> **Внимание оператора**: все контентные окна обязаны использовать 100% табличную обертку (`<table width="100%"><tr><td width="2000">...</td></tr></table>`). 
> Это гарантирует, что зубцы крышек на `x=1` и `x=849` ложатся ровно на серые рамки GitHub без боковых зазоров на любых дисплеях.

<br/>

<!-- 3. ИНТЕРАКТИВНОЕ ОКНО CYBERPUNK (WINDOW) -->
<img src="assets/example/frame-top-cyber.svg" width="100%" />

<table width="100%">
<tr>
<td width="2000">

### 🧬 Спецификация ядра системы

Интерфейс спроектирован по канонам ретро-футуризма с полной адаптацией под рендерер GitHub:

| Подсистема | Протокол | Статус | Задержка |
| :--- | :--- | :--- | :--- |
| **Fiber Pipeline** | `IPC_BUS // DMA` | `● ACTIVE` | `0.12 ms` |
| **Translucent Glass** | `SVG_ALPHA_0.82` | `● STABLE` | `0.00 ms` |
| **Live Radar HUD** | `360_DEG_SWEEP` | `● SCANNING` | `16.6 ms (60 FPS)` |

```bash
# Инициализация демо-проекта
npm install neo-kernel-core
npx neo-core --bootstrap
```

</td>
</tr>
</table>

<img src="assets/example/frame-bottom-cyber.svg" width="100%" />

<br/>

<!-- 4. СВОРАЧИВАЕМЫЙ ТЕРМИНАЛ (DETAILS/SUMMARY) -->
<details >
<summary><kbd>▶ ENVIRONMENT_CONFIGURATION</kbd> <b>[ НАЖМИТЕ ДЛЯ СВОРАЧИВАНИЯ / РАЗВОРАЧИВАНИЯ ]</b> <code>[CLICK TO EXPAND]</code></summary>

<br/>

<img src="assets/example/terminal-top-cyber.svg" width="100%" />

<table width="100%">
<tr>
<td width="2000">

```ini
[RUNTIME]
NODE_ENV=production
HUD_OPACITY=0.82
ACCENT_COLOR=#00C8D7
SECONDARY_COLOR=#A855F7
SCANLINE_FPS=60
```

</td>
</tr>
</table>

<img src="assets/example/terminal-bottom-cyber.svg" width="100%" />

</details>

<br/><br/>

<a href="#top"><img src="assets/example/neo-footer.svg" width="100%" alt="▲ НАВЕРХ" /></a>

---

## 5. Часть 4: Автоматизация через GitHub Actions

Вы можете автоматически пересобирать свой `README.md` при каждом `git push`, добавив следующий файл в `.github/workflows/compile-readme.yml`:

```yaml
name: Compile Pixel README

on:
  push:
    paths:
      - 'README.template.md'
      - 'generator/**'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Compile README from template
        run: |
          python -m generator.cli compile --input README.template.md --output README.md --assets-dir assets/generated

      - name: Commit and push changes
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "docs(readme): automated recompilation from template [skip ci]"
          file_pattern: "README.md assets/generated/*.svg"
```

---

<div align="center">

<a href="README.md"><img src="assets/generated/chip-cat-home.svg" alt="Главная" /></a>
&nbsp;&nbsp;
<a href="CATALOG.md"><img src="assets/generated/chip-cat-examples.svg" alt="Каталог блоков" /></a>
&nbsp;&nbsp;
<a href="#top"><img src="assets/generated/chip-cat-top.svg" alt="Наверх" /></a>

</div>
