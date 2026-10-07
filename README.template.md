# README KIT — UNIVERSAL DESIGN SYSTEM FOR GITHUB REPOSITORIES & DEVELOPER PROFILES

<div id="top"></div>

<div align="center">

<!-- pixel-kit:header style="cyberpunk" primary="#00C8D7" accent="#A855F7" title="README KIT" subtitle="DESIGN SYSTEM FOR GITHUB REPOSITORIES & DEVELOPER PROFILES" spec1="DUAL TARGET: REPOSITORIES // DEVELOPER PROFILES" spec2="MULTI-STYLE: RETRO-PIXEL // MODERN VECTOR // CORPORATE" spec3="DATA VISUALS: STARS CHART // METRICS // TECHSTACK" tag="RELEASE_v5.0" out="assets/generated/header-readme.svg" -->

<br/><br/>

<!-- pixel-kit:chip style="cyberpunk" type="closed" text="[DOCS] КАТАЛОГ БЛОКОВ" href="CATALOG.md" out="assets/generated/chip-readme-catalog.svg" -->
&nbsp;&nbsp;
<!-- pixel-kit:chip style="tactical" type="closed" text="[SPEC] ПРИМЕРЫ И РАЗБОР" href="EXAMPLES.md" out="assets/generated/chip-readme-examples.svg" -->
&nbsp;&nbsp;
<!-- pixel-kit:chip style="minimal" type="pulse" text="● v5.0.0 STABLE" href="#top" out="assets/generated/chip-readme-version.svg" -->
&nbsp;&nbsp;
<!-- pixel-kit:chip style="cyberpunk" type="closed" github="stars" repo="Kazinagg/pixel-readme-kit" out="assets/generated/chip-readme-stars.svg" -->
&nbsp;&nbsp;
<!-- pixel-kit:chip style="tactical" type="closed" github="forks" repo="Kazinagg/pixel-readme-kit" out="assets/generated/chip-readme-forks.svg" -->
&nbsp;&nbsp;
<!-- pixel-kit:chip style="minimal" type="pulse" github="license" repo="Kazinagg/pixel-readme-kit" out="assets/generated/chip-readme-license.svg" -->

<br/><br/>

<!-- pixel-kit:divider style="cyberpunk" primary="#00C8D7" out="assets/generated/divider-readme.svg" -->

</div>

<br/>

## 01 // Телеметрия системы (System Telemetry)

<!-- pixel-kit:metrics style="cyberpunk" out="assets/generated/metrics-readme.svg" -->
- label="CACHE ACCELERATION" value="0.02s" delta="98% faster builds" trend="up"
- label="TEST COVERAGE" value="99 / 99" status="100% PASS"
- label="COMPONENTS SUITE" value="14 BLOCKS" delta="+2 new in v5.0" trend="up"
- label="RUNTIME DEPS" value="0 EXT" status="STD-LIB ONLY"
<!-- /pixel-kit:metrics -->

<br/>

<!-- pixel-kit:progress style="cyberpunk" value="100" label="V5.0 REPO & PROFILE EVOLUTION COMPLETE" sub="MULTI-STYLE ARCHITECTURE // STAR CHART // PROFILE DOSSIER" out="assets/generated/progress-readme.svg" -->

<br/>

## 02 // Концепция проекта (Project Overview)

**Readme Kit** — универсальная дизайн-система, генератор ассетов и интерактивная визуальная студия для оформления **Репозиториев (Repositories)** и **Профилей разработчиков (Developer Profiles `username/username`)** на GitHub.

Комплект предоставляет гибкие инструменты для двух ключевых сценариев:
1. **Оформление репозиториев (Repositories Showcase)**:
   - Библиотеки, CLI-утилиты, веб-сервисы, монорепозитории и исследовательские отчеты.
   - Модульные окна контента, интерактивные терминалы, матрицы стека, плашки алертов и футеры.
2. **Оформление профилей разработчиков (Developer Profiles)**:
   - Флагманские карточки профиля (`<!-- pixel-kit:profile -->`) со стилизованным аватаром, LED-индикатором статуса, 3D-типографикой и био.
   - График динамики звёзд и активности (`<!-- pixel-kit:starchart -->`) с координатной сеткой и градиентной заливкой.
   - Витрины ключевых проектов и социальные чипы.

<br/>

## 03 // Флагманские компоненты v5.0 (Showcase)

### Карточка профиля разработчика (Developer Dossier Card)

<!-- pixel-kit:profile style="cyberpunk" name="ALEX DEVELOPER" role="FULLSTACK & SYSTEMS ARCHITECT" bio="Building high-performance runtimes and resilient developer tooling." status="AVAILABLE FOR HIRE" location="REMOTE // UTC+3" badge="LEVEL_99" out="assets/generated/profile-readme-demo.svg" -->

<br/>

### График динамики звёзд (Star Growth Trajectory)

<!-- pixel-kit:starchart style="cyberpunk" repo="Kazinagg/pixel-readme-kit" points="15,65,190,480,950,1650" current="1,650" delta="+78% past 6m" title="OPEN SOURCE STARS TRAJECTORY" out="assets/generated/starchart-readme-demo.svg" -->

<br/>

<!-- pixel-kit:callout style="cyberpunk" type="note" title="АРХИТЕКТУРНЫЙ ПРИНЦИП" subtitle="Разделение геометрии (3 парадигмы) и цветовой палитры (primary + accent + preset)" out="assets/generated/callout-readme-arch.svg" -->

---

## 04 // Мульти-стилевая архитектура (3 Дизайн-парадигмы)

Дизайн-система предлагает 3 глобальные визуальные парадигмы с ортогональным разделением **Геометрии (`style`)** и **Цветовых палитр (`theme`)**:

| Парадигма (Стиль `style`) | Канонические темы (`theme`) | Основная палитра | Особенности геометрии | Статус готовности |
| :--- | :--- | :--- | :--- | :--- |
| **Pixel / Retro-Tech** (`pixel`) | `cyberpunk`, `tactical`, `tokyo` | Cyan / Magenta, Phosphor Amber, Tokyo Neon | 3D пиксельный шрифт, радары 360°, CRT-сканлайн, скобы 45°, дизеринг | ● **READY (v5.0-CORE)** |
| **Clean / Modern Vector** (`modern`) | `slate-dark`, `nordic-frost`, `linear-violet` | Matte Graphite, Nordic Frost, Linear Violet | Четкие векторные контуры 1px, сглаженные радиусы, чистый фон | ○ IN DEV (Roadmap v5.1+) |
| **Minimalist / Corporate** (`corporate`) | `academic-paper`, `enterprise-navy`, `swiss-mono` | Academic Paper, Enterprise Navy, Swiss Monochrome | Сдержанная академическая типографика, 1px строгая геометрия | ○ IN DEV (Roadmap v5.2+) |

> [!NOTE]
> **Каноническая триада тем Pixel-стиля**:
> 1. `cyberpunk` — неоновый киберпанк (Electric Cyan `#00C8D7` / Laser Magenta `#FF0055` / Purple `#A855F7`).
> 2. `tactical` — тактический HUD (Phosphor Amber `#F59E0B` / Signal Orange `#EA580C`).
> 3. `tokyo` — ночной токийский ретро-вейв (Tokyo Neon Blue `#7AA2F7` / Vaporwave Purple `#BB9AF7`).
> 
> *Темы `nordic-frost` и `academic-paper` сохранены в ядре генератора как исходники и фундамент для грядущих стилей Modern и Corporate.*

<br/>

## 05 // Стек технологий и поддерживаемое окружение

<!-- pixel-kit:techstack style="cyberpunk" items="python,docker,git,linux,github" columns="5" out="assets/generated/techstack-readme.svg" -->

<br/>

## 06 // Дорожная карта развития (Roadmap)

<!-- pixel-kit:timeline style="cyberpunk" out="assets/generated/timeline-readme.svg" -->
- title="v1.0 - SVG HUD BANNER FOUNDATION" sub="Флагманские адаптивные шапки, 3D пиксельные шрифты, радары 360°" status="COMPLETED"
- title="v2.0 - MODULAR WINDOW CHASSIS" sub="Оконные рамки, чипы со статистикой GitHub, инлайн-алерты, разделители" status="COMPLETED"
- title="v3.0 - MULTI-THEMING & ANTI-COLLISION" sub="Автоматическая смена dark/light тем через CSS, безопасные зоны" status="COMPLETED"
- title="v4.0 - DATA VIZ, LIVE STUDIO & MCP" sub="Метрики, прогресс, стек, таймлайн, веб-студия, MCP сервер, кэш" status="COMPLETED"
- title="v5.0 - REPOSITORIES & DEVELOPER PROFILES" sub="Мульти-стили, график звезд, карточки профилей, шаблоны repo/ и profile/" status="COMPLETED"
<!-- /pixel-kit:timeline -->

<br/>

## 07 // Руководство по началу работы (Quick Start Guide)

### 1. Мгновенный запуск Студии в браузере (Zero-Install)
```bash
# Запуск через pipx без предварительного клонирования (рекомендуется):
pipx run pixel-readme-kit studio --open

# Или классическая установка пакета через pip:
pip install pixel-readme-kit
pixel-kit studio --open
```

### 2. Инициализация шаблона с помощью Scaffolder
```bash
# Оформление репозитория (библиотека, CLI, исследование):
pixel-kit init --category repo --type library --title "MY-AWESOME-LIB"

# Оформление профиля разработчика (dossier, минимализм, киберпанк):
pixel-kit init --category profile --type developer --title "ALEX DEVELOPER"
```

### 3. Компиляция и синхронизация (с автоподхватом данных GitHub)
```bash
# Полная сборка с актуализацией звезд, очисткой сирот и сбросом кэша Camo:
pixel-kit sync

# Или ручная компиляция шаблона:
pixel-kit compile --fetch-github --clean-assets --bust-cache
```

### 4. Автоматическое обновление по расписанию в GitHub Actions
Чтобы график звезд, бейджи и метрики всегда оставались актуальными, добавьте workflow `.github/workflows/update-readme.yml`:
```yaml
name: Sync Readme
on:
  schedule:
    - cron: '0 0 * * *' # Ежедневное обновление в полночь
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - uses: Kazinagg/pixel-readme-kit@v5
        with:
          fetch-github: 'true'
          bust-cache: 'true'
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      - uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "chore: auto-update readme stats and starchart [skip ci]"
```

### 5. Подключение через MCP (Claude Desktop, Cursor, Antigravity)
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

## 08 // Интерактивный пример окна контента

<!-- pixel-kit:window style="cyberpunk" primary="#00C8D7" title="╔═ RUNTIME.SYS // MODULE_INTERFACE" tag="[ONLINE]" out_top="assets/generated/frame-readme-top.svg" out_bottom="assets/generated/frame-readme-bottom.svg" -->
### [SPEC] Спецификация подсистем ядра v5.0

Контент внутри окон остаётся полноценным Markdown:

| Подсистема | Протокол | Статус | Задержка |
| :--- | :--- | :--- | :--- |
| **Multi-Style Engine** | `PIXEL + VECTOR + CORPORATE` | `● TRI-PARADIGM` | `0.00 ms` |
| **Theme Engine** | `CSS_VARS_MEDIA_QUERY` | `● AUTO_ADAPTIVE` | `0.00 ms` |
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
python -m generator.cli init --help      # Скаффолдер шаблонов (repo/* и profile/*)
python -m generator.cli header --help    # Заглавные шапки (включая --compact)
python -m generator.cli starchart --help # График динамики звезд и роста
python -m generator.cli profile --help   # Карточка профиля разработчика
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
