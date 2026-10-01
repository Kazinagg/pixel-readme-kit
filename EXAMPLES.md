# 💡 PIXEL README KIT v4.0 — ПРИМЕРЫ И РАБОЧИЙ ПРОЦЕСС (WORKFLOW)

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
> Вы пишете обычный декларативный Markdown-шаблон с директивами `<!-- pixel-kit:... -->`, а компилятор превращает его в профессиональный README с живой анимацией и адаптивной темой.

---

## 📑 Оглавление руководства

1. [Как устроен рабочий процесс (Workflow)](#1-как-устроен-рабочий-процесс-workflow)
2. [Часть 1: Шаблон БЕЗ генерации (Исходный текст)](#2-часть-1-шаблон-без-генерации-исходный-текст)
3. [Часть 2: Команда сборки и новые флаги v4.0](#3-часть-2-команда-сборки-и-новые-флаги-v40)
4. [Часть 3: Сгенерированный результат (Live Render)](#4-часть-3-сгенерированный-результат-live-render)
5. [Часть 4: Интерактивный Live Preview и HUD Studio](#5-часть-4-интерактивный-live-preview-и-hud-studio)
6. [Часть 5: MCP Сервер для AI-агентов (Model Context Protocol)](#6-часть-5-mcp-сервер-для-ai-агентов-model-context-protocol)
7. [Часть 6: Автоматизация через GitHub Actions](#7-часть-6-автоматизация-через-github-actions)

---

## 1. Как устроен рабочий процесс (Workflow)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. ИСХОДНЫЙ ШАБЛОН: EXAMPLE_TEMPLATE.md                    │
│    - Декларативные директивы <!-- pixel-kit:... -->         │
│    - Живой Markdown-текст, списки, таблицы и KaTeX          │
│    - Инфографика v4.0: metrics, progress, techstack, timeline│
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. СБОРКА: python -m generator.cli compile                  │
│    - Инкрементальный кэш SHA-256 (сборка за ~10-40 мс)      │
│    - GC мусорных файлов: --clean-assets                     │
│    - Camo Cache-Buster для GitHub: --bust-cache             │
│    - Безопасные мобильные шрифты >= 11px                    │
│    - Оборачивает контент в 100% таблицы без боковых щелей   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. ГОТОВЫЙ РЕЗУЛЬТАТ: EXAMPLE.md (или README.md)            │
│    - 100% валидный GitHub Flavored Markdown                 │
│    - Идеальный контраст на тёмной и светлой темах (APCA Lc) │
│    - Живая CSS-анимация: радар 360°, лазеры, эквалайзеры   │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Часть 1: Шаблон БЕЗ генерации (Исходный текст)

Ниже представлен **реальный исходный код файла шаблона** ([EXAMPLE_TEMPLATE.md](EXAMPLE_TEMPLATE.md)) в сыром текстовом виде, каким его пишет разработчик:

````markdown
<div id="top"></div>

<div align="center">

<!-- pixel-kit:header style="cyberpunk" primary="#00C8D7" accent="#A855F7" title="NEO-CORE" subtitle="CYBER-HUD AUTOMATION & KERNEL RUNTIME" spec1="HUD ARCHITECTURE: TRANSLUCENT GLASS & CYBER BRACKETS" spec2="TEXT INTEGRATION: 100% COPYABLE MARKDOWN & MATH" spec3="ANIMATION SUITE: RADAR // SCANLINE // LADDER CASCADE" tag="SYS_v4.0_ONLINE" out="assets/example/neo-header.svg" -->

<br/><br/>

<!-- pixel-kit:chip style="cyberpunk" type="closed" text="⚡ v4.0.0" out="assets/example/chip-version.svg" -->
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
| **Adaptive Theme** | `SVG_CSS_VARS` | `● DUAL_THEME` | `0.00 ms` |
| **Live Radar HUD** | `360_DEG_SWEEP` | `● SCANNING` | `16.6 ms (60 FPS)` |

```bash
# Инициализация демо-проекта
npm install neo-kernel-core
neo-kernel init --profile=cyberpunk
```
<!-- /pixel-kit:window -->

<br/>

<!-- 4. КАРТОЧКИ МЕТРИК И KPI (METRICS) -->
<!-- pixel-kit:metrics style="cyberpunk" primary="#00C8D7" accent="#A855F7" out="assets/example/neo-metrics.svg" -->
- label="THROUGHPUT" value="48.2 GB/s" delta="+18.4% PEAK" trend="up"
- label="FRAME LATENCY" value="0.14 ms" delta="p99 < 0.2ms" trend="up"
- label="ACTIVE NODES" value="1,024" delta="+64 CLUSTERS" trend="up"
- label="KERNEL HEALTH" value="99.98%" status="NOMINAL"
<!-- /pixel-kit:metrics -->

<br/>

<!-- 5. ИНДИКАТОР ПРОГРЕССА И СТАТУСА (PROGRESS) -->
<!-- pixel-kit:progress style="cyberpunk" value="88" label="NEO-CORE v4.0 DEPLOYMENT PROGRESS" sub="STAGE 04/04 // STABLE RUNTIME VERIFIED" primary="#00C8D7" accent="#A855F7" out="assets/example/neo-progress.svg" -->

<br/>

<!-- 6. СПЛИТТЕР ПОДМОДУЛЕЙ (SPLITTER) -->
<!-- pixel-kit:splitter style="tactical" primary="#F59E0B" label="[TACTICAL: SECURITY_AND_FAILSAFE]" out="assets/example/splitter-tactical.svg" -->

<br/>

<!-- 7. ТАКТИЧЕСКОЕ ОКНО С ФАСКАМИ 45° (TACTICAL WINDOW) -->
<!-- pixel-kit:window style="tactical" primary="#F59E0B" title="╔═ SEC.DEFENSE // SECTOR_LOCK_ALPHA.EXE" tag="[TACTICAL]" out_top="assets/example/frame-top-tactical.svg" out_bottom="assets/example/frame-bottom-tactical.svg" -->
### ⚡ Тактический модуль мониторинга

- Скосы под 45° с прижимными зубцами на `x=1` и `x=849`.
- Исключены любые внешние разделители и прокладки.
- Полная совместимость со светлой и тёмной темами GitHub.
<!-- /pixel-kit:window -->

<br/>

<!-- 8. МАТРИЦА СТЕКА ТЕХНОЛОГИЙ (TECHSTACK) -->
<!-- pixel-kit:techstack style="tactical" primary="#F59E0B" accent="#EA580C" items="python,rust,cpp,docker,git,linux" columns="6" out="assets/example/neo-techstack.svg" -->

<br/>

<!-- 9. ТАКТИЧЕСКИЙ ТАЙМЛАЙН / ДОРОЖНАЯ КАРТА (TIMELINE) -->
<!-- pixel-kit:timeline style="cyberpunk" primary="#00C8D7" accent="#A855F7" out="assets/example/neo-timeline.svg" -->
- stage="01" title="CORE ENGINE" date="2026-Q1" status="COMPLETED" desc="Vector pixel rendering pipeline"
- stage="02" title="LIVE METRICS" date="2026-Q2" status="COMPLETED" desc="Realtime HUD KPI & progress widgets"
- stage="03" title="STUDIO & MCP" date="2026-Q3" status="ACTIVE" desc="Zero-dep web studio & AI model protocol"
- stage="04" title="GLOBAL CDN" date="2026-Q4" status="PLANNED" desc="Dynamic edge badge synthesis"
<!-- /pixel-kit:timeline -->

<br/>

<!-- 10. ИНТЕРАКТИВНЫЙ ДРОУЭР / ТЕРМИНАЛ (DETAILS / SUMMARY) -->
<!-- pixel-kit:terminal style="minimal" primary="#4F8BFF" title="SYSTEM.CONFIG.YAML" state="open" out_top="assets/example/terminal-top.svg" out_bottom="assets/example/terminal-bottom.svg" -->
```yaml
# neo-kernel.config.yaml
runtime:
  engine: "pixel-readme-kit-v4.0"
  style: "cyberpunk"
  theme:
    mode: "auto"
    primary: "#00C8D7"
    accent: "#A855F7"
telemetry:
  radar_sweep: true
  scanline: true
  equalizer: "44.1kHz"
```
<!-- /pixel-kit:terminal -->

<br/>

<div align="center">

<!-- 11. ЗАКРЫВАЮЩАЯ ПЛАСТИНА ФУТЕРА (FOOTER) -->
<!-- pixel-kit:footer style="cyberpunk" primary="#00C8D7" status="SYSTEM_ONLINE // ALL_CHANNELS_CLEAR" nav="НАВЕРХ К ШАПКЕ" out="assets/example/footer.svg" -->

<br/><br/>

<sub>NEO-CORE v4.0 &bull; PIXEL README DESIGN SYSTEM &bull; 2026</sub>

</div>
````

---

## 3. Часть 2: Команда сборки и новые флаги v4.0

Чтобы превратить шаблон выше в готовый Markdown и сгенерировать все необходимые SVG-ассеты, выполняется команда компиляции:

```bash
python -m generator.cli compile --input EXAMPLE_TEMPLATE.md --output EXAMPLE.md --assets-dir assets/example
```

### Продвинутые флаги компилятора:

| Флаг | Назначение |
| :--- | :--- |
| `--clean-assets` | **Garbage Collector**: сканирует папку `--assets-dir` и автоматически удаляет старые сиротские SVG, на которые больше нет ссылок в шаблоне. |
| `--dry-run-clean` | Выводит список файлов-сирот без их фактического удаления. |
| `--no-cache` | Принудительно отключает инкрементальный кэш и пересобирает все ассеты с нуля. |
| `--bust-cache` | **GitHub Camo Cache-Buster**: добавляет хэш контента `?v=<hash>` к путям изображений, пробивая жесткое прокси-кэширование GitHub при обновлении SVG. |

---

## 4. Часть 3: Сгенерированный результат (Live Render)

Ниже в реальном времени отображается результат работы компилятора из файла [EXAMPLE.md](EXAMPLE.md):

---

<div id="top"></div>

<div align="center">

<img src="assets/example/neo-header.svg" width="100%" alt="NEO-CORE" />

<br/><br/>

<img src="assets/example/chip-version.svg" alt="⚡ v4.0.0" />
&nbsp;&nbsp;
<img src="assets/example/chip-status.svg" alt="● LIVE_NODE" />
&nbsp;&nbsp;
<img src="assets/example/chip-license.svg" alt="LICENSE // MIT" />
&nbsp;&nbsp;
<img src="assets/example/chip-security.svg" alt="SEC: CLEAR" />

<br/><br/>

<img src="assets/example/divider-top.svg" width="100%" alt="Divider cyberpunk" />

</div>

<br/>

<!-- 1. АВТОНОМНЫЙ АЛЕРТ (CALLOUT) -->
<img src="assets/example/callout-arch.svg" width="100%" alt="RUNTIME ARCHITECTURE // ZERO CAMO PROXY OVERFLOW" />

<br/>

<!-- 2. БЛОК ЦИТАТЫ С ХЕДЕРОМ (QUOTE) -->
> <img src="assets/example/callout-quote-warn.svg" width="100%" alt="CRITICAL CONSTRAINT // FULL-WIDTH COMPLIANCE" />
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
| **Adaptive Theme** | `SVG_CSS_VARS` | `● DUAL_THEME` | `0.00 ms` |
| **Live Radar HUD** | `360_DEG_SWEEP` | `● SCANNING` | `16.6 ms (60 FPS)` |

```bash
# Инициализация демо-проекта
npm install neo-kernel-core
neo-kernel init --profile=cyberpunk
```

</td>
</tr>
</table>

<img src="assets/example/frame-bottom-cyber.svg" width="100%" />

<br/>

<!-- 4. КАРТОЧКИ МЕТРИК И KPI (METRICS) -->
<img src="assets/example/neo-metrics.svg" width="100%" alt="Metrics" />

<br/>

<!-- 5. ИНДИКАТОР ПРОГРЕССА И СТАТУСА (PROGRESS) -->
<img src="assets/example/neo-progress.svg" width="100%" alt="NEO-CORE v4.0 DEPLOYMENT PROGRESS" />

<br/>

<!-- 6. СПЛИТТЕР ПОДМОДУЛЕЙ (SPLITTER) -->
<img src="assets/example/splitter-tactical.svg" width="100%" alt="[TACTICAL: SECURITY_AND_FAILSAFE]" />

<br/>

<!-- 7. ТАКТИЧЕСКОЕ ОКНО С ФАСКАМИ 45° (TACTICAL WINDOW) -->
<img src="assets/example/frame-top-tactical.svg" width="100%" />

<table width="100%">
<tr>
<td width="2000">

### ⚡ Тактический модуль мониторинга

- Скосы под 45° с прижимными зубцами на `x=1` и `x=849`.
- Исключены любые внешние разделители и прокладки.
- Полная совместимость со светлой и тёмной темами GitHub.

</td>
</tr>
</table>

<img src="assets/example/frame-bottom-tactical.svg" width="100%" />

<br/>

<!-- 8. МАТРИЦА СТЕКА ТЕХНОЛОГИЙ (TECHSTACK) -->
<img src="assets/example/neo-techstack.svg" width="100%" alt="Tech Stack" />

<br/>

<!-- 9. ТАКТИЧЕСКИЙ ТАЙМЛАЙН / ДОРОЖНАЯ КАРТА (TIMELINE) -->
<img src="assets/example/neo-timeline.svg" width="100%" alt="Timeline" />

<br/>

<!-- 10. ИНТЕРАКТИВНЫЙ ДРОУЭР / ТЕРМИНАЛ (DETAILS / SUMMARY) -->
<details open>
<summary><kbd>▶ SYSTEM.CONFIG.YAML</kbd> <b>[ НАЖМИТЕ ДЛЯ СВОРАЧИВАНИЯ / РАЗВОРАЧИВАНИЯ ]</b> <code>[STATE: EXPANDED]</code></summary>

<br/>

<img src="assets/example/terminal-top.svg" width="100%" />

<table width="100%">
<tr>
<td width="2000">

```yaml
# neo-kernel.config.yaml
runtime:
  engine: "pixel-readme-kit-v4.0"
  style: "cyberpunk"
  theme:
    mode: "auto"
    primary: "#00C8D7"
    accent: "#A855F7"
telemetry:
  radar_sweep: true
  scanline: true
  equalizer: "44.1kHz"
```

</td>
</tr>
</table>

<img src="assets/example/terminal-bottom.svg" width="100%" />

</details>

<br/>

<div align="center">

<!-- 11. ЗАКРЫВАЮЩАЯ ПЛАСТИНА ФУТЕРА (FOOTER) -->
<a href="#top"><img src="assets/example/footer.svg" width="100%" alt="НАВЕРХ К ШАПКЕ" /></a>

<br/><br/>

<sub>NEO-CORE v4.0 &bull; PIXEL README DESIGN SYSTEM &bull; 2026</sub>

</div>

---

## 5. Часть 4: Интерактивный Live Preview и HUD Studio

В версию 4.0 встроен локальный веб-сервер и графическая студия, работающая **без единой внешней зависимости (Zero Dependencies)**:

```bash
# Запуск интерактивной студии с авто-открытием браузера:
python -m generator.cli studio --open

# Или запуск сервера Live Preview для файла:
python -m generator.cli serve --template README.template.md --port 8080 --open
```

### Возможности HUD Studio:
1. **Мгновенный рендеринг SVG (< 50 мс)**: изменения любых параметров (цвета, стиль, текст заголовка, бейджи) отображаются на лету через API `/api/render`.
2. **SSE Live-Reload**: при редактировании `README.template.md` в любой IDE страница браузера обновляется автоматически за 300 мс без перезагрузки.
3. **HUD Debug Mode**: наложение 20px сетки выравнивания и живой мониторинг бюджета символов (Character Budget Warning Badges) прямо на холсте.
4. **Конструктор директив**: кнопки «Копировать директиву» и «Вставить в шаблон» для мгновенного переноса готового блока в ваш проект.

---

## 6. Часть 5: MCP Сервер для AI-агентов (Model Context Protocol)

Для AI-ассистентов (Antigravity, Claude Desktop, Cursor, Roo-Code) комплект поставляется с нативным stdio MCP сервером:

```bash
# Запуск сервера:
python -m generator.mcp_server
```

### Конфигурация Claude Desktop (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "pixel-readme": {
      "command": "python",
      "args": ["-m", "generator.mcp_server"],
      "cwd": "/path/to/pixel-readme-kit"
    }
  }
}
```

Сервер предоставляет 12 специализированных инструментов:
- `pixel_compile_template` — полная сборка шаблона с кэшированием и очисткой.
- `pixel_generate_header` — шапки с поддержкой 3 стилей и компактного режима.
- `pixel_generate_metrics` — карточки KPI и метрик производительности.
- `pixel_generate_progress` — многосегментные полосы прогресса.
- `pixel_generate_techstack` — сетка технологий с пиксельными иконками.
- `pixel_generate_timeline` — таймлайн и дорожная карта.
- `pixel_generate_social` — баннер 1280x640 OpenGraph Social Preview.
- `pixel_generate_callout`, `pixel_generate_frame`, `pixel_generate_chip`, `pixel_generate_divider`, `pixel_generate_splitter`.

---

## 7. Часть 6: Автоматизация через GitHub Actions

В репозиторий уже включён готовый пайплайн [.github/workflows/pixel-compile.yml](.github/workflows/pixel-compile.yml), который:
1. Прогоняет полный юнит-тест сьют на Python 3.11 и 3.12.
2. При push в `main` автоматически компилирует все `*.template.md` файлы.
3. Валидирует 100% полученных SVG через `xml.etree.ElementTree`.
4. Делает коммит и пуш с меткой `[skip ci]`.

```yaml
name: Pixel Kit Test & Auto-Compiler

on:
  push:
    branches: [main]
    paths:
      - '*.template.md'
      - 'generator/**'
      - 'presets/**'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: python -m unittest discover tests -v

  compile:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: |
          python -m generator.cli compile --input README.template.md --output README.md --assets-dir assets/generated
      - uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "chore: auto-compile pixel-readme-kit templates [skip ci]"
```

---

<div align="center">

<a href="README.md"><img src="assets/generated/chip-cat-home.svg" alt="Главная" /></a>
&nbsp;&nbsp;
<a href="CATALOG.md"><img src="assets/generated/chip-cat-examples.svg" alt="Каталог блоков" /></a>
&nbsp;&nbsp;
<a href="#top"><img src="assets/generated/chip-cat-top.svg" alt="Наверх" /></a>

</div>
