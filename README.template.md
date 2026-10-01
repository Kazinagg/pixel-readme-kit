# 📦 PIXEL README KIT — RETRO-CYBERPUNK & TACTICAL HUD DESIGN SYSTEM

<div id="top"></div>

<div align="center">

<!-- pixel-kit:header style="cyberpunk" primary="#00C8D7" accent="#A855F7" title="PIXEL README KIT" subtitle="RETRO-CYBERPUNK & TACTICAL HUD DESIGN SYSTEM FOR GITHUB" spec1="HUD ARCHITECTURE: TRANSLUCENT GLASS & DUAL-THEME" spec2="TEXT INTEGRATION: 100% COPYABLE MARKDOWN & MATH" spec3="DATA VISUALS: METRICS // PROGRESS // TECHSTACK" tag="RELEASE_v4.0" out="assets/generated/header-readme.svg" -->

<br/><br/>

<!-- pixel-kit:chip style="cyberpunk" type="closed" text="📚 КАТАЛОГ БЛОКОВ" href="CATALOG.md" out="assets/generated/chip-readme-catalog.svg" -->
&nbsp;&nbsp;
<!-- pixel-kit:chip style="tactical" type="decay" text="💡 ПРИМЕРЫ И РАЗБОР" href="EXAMPLES.md" out="assets/generated/chip-readme-examples.svg" -->
&nbsp;&nbsp;
<!-- pixel-kit:chip style="minimal" type="pulse" text="● v4.0.0 STABLE" href="#top" out="assets/generated/chip-readme-version.svg" -->
&nbsp;&nbsp;
<!-- pixel-kit:chip style="cyberpunk" type="closed" github="stars" repo="Kazinagg/pixel-readme-kit" out="assets/generated/chip-readme-stars.svg" -->
&nbsp;&nbsp;
<!-- pixel-kit:chip style="tactical" type="decay" github="forks" repo="Kazinagg/pixel-readme-kit" out="assets/generated/chip-readme-forks.svg" -->
&nbsp;&nbsp;
<!-- pixel-kit:chip style="minimal" type="pulse" github="license" repo="Kazinagg/pixel-readme-kit" out="assets/generated/chip-readme-license.svg" -->

<br/><br/>

<!-- pixel-kit:divider style="cyberpunk" primary="#00C8D7" out="assets/generated/divider-readme.svg" -->

</div>

<br/>

## 📊 Ключевые показатели v4.0 (System Telemetry)

<!-- pixel-kit:metrics style="cyberpunk" out="assets/generated/metrics-readme.svg" -->
- label="CACHE ACCELERATION" value="0.02s" delta="98% faster builds" trend="up"
- label="TEST COVERAGE" value="52 / 52" status="100% PASS"
- label="COMPONENTS SUITE" value="12 BLOCKS" delta="+5 new in v4.0" trend="up"
- label="RUNTIME DEPS" value="0 EXT" status="STD-LIB ONLY"
<!-- /pixel-kit:metrics -->

<br/>

<!-- pixel-kit:progress style="cyberpunk" value="100" label="V4.0 EVOLUTION PROGRESS (5/5 SPRINTS)" sub="ALL ARCHITECTURAL PHASES VALIDATED AND OPERATIONAL" out="assets/generated/progress-readme.svg" -->

<br/>

## 📌 О проекте (Project Overview)

**Pixel Readme Kit** — модульная дизайн-система и автономный генератор для оформления репозиториев и профилей GitHub в бескомпромиссной эстетике **ретро-киберпанка**, **тактических военных HUD** и **неонового стекла**.

Комплект создан для решения фундаментальных проблем стандартного оформления GitHub:
1. 🌗 **Адаптивная мульти-режимность (Multi-Mode Theming)**:
   - `mode="auto"` (**по умолчанию**): единый автономный SVG с нативными CSS-переменными и медиа-запросом `@media (prefers-color-scheme: dark)`. Переключается мгновенно вместе с системной темой ОС или браузера, без дублирования файлов.
   - Также поддерживаются: `mode="dark"`, `mode="light"`, `mode="transparent"` (прозрачный фон), `mode="gh"` (`#gh-*-mode-only`) и `mode="picture"` (`<picture>`).
2. ⚡ **Инкрементальный SHA-256 кэш и сборщик мусора (GC)**:
   - Хэширует свойства директив, компилируя только изменившиеся ассеты за доли секунды.
   - Флаг `--clean-assets` автоматически удаляет файлы-сироты из `assets/generated/`.
   - Флаг `--bust-cache` автоматически снабжает ссылки версионными хэшами `?v=<hash>` для обхода кэша Camo Proxy.
3. 🖥️ **Live Preview и HUD Studio Web UI**:
   - Локальный HTTP-сервер на стандартной библиотеке Python с SSE Live Reload (`python -m generator.cli studio`).
   - Интерактивный генератор блоков с предпросмотром за <50мс, копированием директив и сеткой HUD Debug.
4. 🤖 **Нативный MCP-сервер (Model Context Protocol)**:
   - Встроенный сервер для AI-агентов (Claude, Cursor, Antigravity, Copilot) с 5 структурированными инструментами.
5. 📱 **Безопасная мобильная типографика и Compact Header**:
   - Гарантированный порог читаемости текста $\ge 11$px на экранах смартфонов.
   - Компактный флагманский баннер (`compact="true"`, 84px) для мобильных и минималистичных репозиториев.
   - Генератор OpenGraph карточек 1280×640 (`pixel-kit:social`).

<br/>

<!-- pixel-kit:callout style="cyberpunk" type="note" title="АРХИТЕКТУРНЫЙ ПРИНЦИП" subtitle="Разделение формы (3 глобальных стиля) и цветовой палитры (primary + accent)" out="assets/generated/callout-readme-arch.svg" -->

---

## 🛠️ Стек технологий и поддерживаемое окружение

<!-- pixel-kit:techstack style="cyberpunk" items="python,docker,git,linux,github" columns="5" out="assets/generated/techstack-readme.svg" -->

<br/>

## 🏛️ 3 Глобальных стиля геометрии

Дизайн-система строго разделяет **геометрию (форму блоков)** и **цветовую палитру**:

| Стиль | Канонические цвета | Геометрия и силуэт | Механика распада (Decay) | Накрытие таблиц | Живая анимация |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 **Cyberpunk** | Cyan `#00C8D7`<br/>Purple `#A855F7` | Прямые углы, открытые кронштейны, пиксели `3×3` | Матричный пиксельный дизеринг (`3×3 ➔ 2×2 ➔ 1×1`) | Накрытие таблицы зубцами `x=1..849` | Радар 360°, CRT Scanline, PCB-пакет |
| 🟡 **Tactical Military** | Amber `#F59E0B`<br/>Orange `#EA580C` | 45° срезанные фаски (Chamfers), шевроны `▲` | Диагональные штрихи фасок `///` с затуханием | Накрытие фасками `45°` без зазоров | Пульсирующий прицел, маркеры захвата |
| 🟣 **Minimal Glass** | Tokyo Blue `#4F8BFF`<br/>Magenta `#A855F7` | Ультратонкая волосяная рамка 1px, зацепы `┌ ┐` | Микроточечное рассеивание (Micro-stipple) | Монолитная 3-строчная таблица | Спектральный 5-полосный эквалайзер |

---

## 🗺️ Дорожная карта развития (Roadmap)

<!-- pixel-kit:timeline style="cyberpunk" out="assets/generated/timeline-readme.svg" -->
- title="v1.0 - SVG HUD BANNER FOUNDATION" sub="Флагманские адаптивные шапки, 3D пиксельные шрифты, радары 360°" status="COMPLETED"
- title="v2.0 - MODULAR WINDOW CHASSIS" sub="Оконные рамки, чипы со статистикой GitHub, инлайн-алерты, разделители" status="COMPLETED"
- title="v3.0 - MULTI-THEMING & ANTI-COLLISION" sub="Автоматическая смена dark/light тем через CSS, безопасные зоны" status="COMPLETED"
- title="v4.0 - DATA VIZ, LIVE STUDIO & MCP" sub="Метрики, прогресс, стек, таймлайн, веб-студия, MCP сервер, кэш" status="COMPLETED"
- title="v4.1 - GITHUB ACTION & COMMUNITY PACKS" sub="Автоматическая компиляция в CI/CD, внешние палитры и плагины" status="IN_PROGRESS"
<!-- /pixel-kit:timeline -->

<br/>

## 🚀 Быстрый старт (Quick Start)

### 1. Интерактивная Web-студия (Live Preview & Studio)
```bash
# Запуск веб-редактора с мгновенным Live Reload (SSE):
python -m generator.cli studio --open
```

### 2. Инициализация шаблона с помощью Scaffolder
```bash
# Быстрое создание README.template.md из готовых пресетов:
python -m generator.cli init --type library --title "MY-AWESOME-LIB"
```

### 3. Компиляция шаблона в Markdown
```bash
# Полная сборка с инкрементальным кэшем, очисткой сирот и Camo-хэшированием:
python -m generator.cli compile --clean-assets --bust-cache
```

### 4. Подключение через MCP (Claude Desktop, Cursor, Antigravity)
Добавьте сервер в ваш `mcp_config.json`:
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

---

## 🪟 Интерактивный пример окна контента

<!-- pixel-kit:window style="cyberpunk" primary="#00C8D7" title="╔═ RUNTIME.SYS // MODULE_INTERFACE" tag="[ONLINE]" out_top="assets/generated/frame-readme-top.svg" out_bottom="assets/generated/frame-readme-bottom.svg" -->
### 🧬 Спецификация подсистем ядра v4.0

Контент внутри окон остаётся полноценным Markdown:

| Подсистема | Протокол | Статус | Задержка |
| :--- | :--- | :--- | :--- |
| **Theme Engine** | `CSS_VARS_MEDIA_QUERY` | `● AUTO_ADAPTIVE` | `0.00 ms` |
| **Anti-Collision** | `WORD_WRAP_DOWNSCALE` | `● ZERO_OVERLAP` | `0.05 ms` |
| **Incremental Cache** | `SHA-256 DIGEST` | `● 98% HIT_RATE` | `0.02 s` |
| **Live Studio** | `SSE REALTIME SYNC` | `● 300ms INTERVAL` | `< 50 ms` |

```bash
# Клонирование и запуск студии
git clone https://github.com/Kazinagg/pixel-readme-kit.git
cd pixel-readme-kit
python -m generator.cli studio
```
<!-- /pixel-kit:window -->

<br/>

<!-- pixel-kit:quote style="tactical" badge="NOTE" title="РУКОВОДСТВО ПО СТИЛЮ" subtitle="Где найти полные справочники и примеры" out="assets/generated/callout-quote-readme.svg" -->
> **Навигация по документации**:
> - Полный каталог всех компонентов во всех стилях доступен в **[CATALOG.md](CATALOG.md)**.
> - Детальный разбор «сырой шаблон $\rightarrow$ скомпилированный результат» приведён в **[EXAMPLES.md](EXAMPLES.md)**.
> - Лицензия проекта: [LICENSE](LICENSE) (MIT).
<!-- /pixel-kit:quote -->

<br/>

<!-- pixel-kit:terminal style="cyberpunk" title="CLI_COMMANDS.LIST" state="closed" out_top="assets/generated/term-top-readme.svg" out_bottom="assets/generated/term-bottom-readme.svg" -->
```bash
# Список всех доступных команд генератора:
python -m generator.cli studio --help    # Запуск HUD Studio с Live Reload
python -m generator.cli serve --help     # Запуск HTTP сервера предпросмотра
python -m generator.cli compile --help   # Компилятор шаблонов Markdown
python -m generator.cli init --help      # Скаффолдер шаблонов (study, library, cli)
python -m generator.cli header --help    # Заглавные шапки (включая --compact)
python -m generator.cli social --help    # OpenGraph социальные карточки 1280x640
python -m generator.cli metrics --help   # KPI метрики
python -m generator.cli progress --help  # Индикаторы прогресса
python -m generator.cli techstack --help # Матрицы технологий
python -m generator.cli timeline --help  # PCB таймлайны
python -m generator.cli footer --help    # Закрывающие пластины
python -m generator.cli callout --help   # Инлайн-алерты и плашки
python -m generator.cli frame --help     # Рамки окон (top/bottom)
python -m generator.cli chip --help      # Чипы и пилюли
python -m generator.cli divider --help   # Разделители глав
python -m generator.cli splitter --help  # Сплиттеры подмодулей
```
<!-- /pixel-kit:terminal -->

<br/><br/>

<!-- pixel-kit:footer style="cyberpunk" status="SESSION_ONLINE // READY" nav="▲ НАВЕРХ" out="assets/generated/footer-readme.svg" -->
