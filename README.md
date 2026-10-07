# README KIT — UNIVERSAL DESIGN SYSTEM FOR GITHUB REPOSITORIES & DEVELOPER PROFILES

<div id="top"></div>

<div align="center">

<img src="assets/generated/header-readme.svg?v=94362f22" width="100%" alt="README KIT" />

<br/><br/>

<a href="CATALOG.md"><img src="assets/generated/chip-readme-catalog.svg?v=ac70a4b4" alt="[DOCS] КАТАЛОГ БЛОКОВ" /></a>
&nbsp;&nbsp;
<a href="EXAMPLES.md"><img src="assets/generated/chip-readme-examples.svg?v=9f2ea60b" alt="[SPEC] ПРИМЕРЫ И РАЗБОР" /></a>
&nbsp;&nbsp;
<a href="#top"><img src="assets/generated/chip-readme-version.svg?v=4762e507" alt="● v5.0.0 STABLE" /></a>
&nbsp;&nbsp;
<a href="https://github.com/Kazinagg/pixel-readme-kit/stargazers"><img src="assets/generated/chip-readme-stars.svg?v=7f5510c1" alt="★ 2" /></a>
&nbsp;&nbsp;
<a href="https://github.com/Kazinagg/pixel-readme-kit/network/members"><img src="assets/generated/chip-readme-forks.svg?v=fc322181" alt="FORKS: 0" /></a>
&nbsp;&nbsp;
<a href="https://github.com/Kazinagg/pixel-readme-kit"><img src="assets/generated/chip-readme-license.svg?v=d551d52e" alt="LICENSE: MIT" /></a>

<br/><br/>

<img src="assets/generated/divider-readme.svg?v=82716312" width="100%" alt="Divider cyberpunk" />

</div>

<br/>

## 01 // Телеметрия системы (System Telemetry)

<img src="assets/generated/metrics-readme.svg?v=fa1ee0fc" width="100%" alt="Metrics" />

<br/>

<img src="assets/generated/progress-readme.svg?v=61f74cbc" width="100%" alt="V5.0 REPO &amp; PROFILE EVOLUTION COMPLETE" />

<br/>

## 02 // Концепция проекта (Project Overview)

**Readme Kit** — универсальная дизайн-система, генератор ассетов и интерактивная визуальная студия для оформления **Репозиториев (Repositories)** и **Профилей разработчиков (Developer Profiles `username/username`)** на GitHub.

Комплект предоставляет гибкие инструменты для двух ключевых сценариев:
1. **Оформление репозиториев (Repositories Showcase)**:
   - Библиотеки, CLI-утилиты, веб-сервисы, монорепозитории и исследовательские отчеты.
   - Модульные окна контента, интерактивные терминалы, матрицы стека, плашки алертов и футеры.
2. **Оформление профилей разработчиков (Developer Profiles)**:
   - Флагманские карточки профиля (`<img src="assets/generated/profile-cyberpunk-1.svg?v=f70c16ef" width="100%" alt="ALEX DEVELOPER" />`) со стилизованным аватаром, LED-индикатором статуса, 3D-типографикой и био.
   - График динамики звёзд и активности (`<img src="assets/generated/starchart-cyberpunk-1.svg?v=bd2f3a79" width="100%" alt="STAR GROWTH TRAJECTORY" />`) с координатной сеткой и градиентной заливкой.
   - Витрины ключевых проектов и социальные чипы.

<br/>

## 03 // Флагманские компоненты v5.0 (Showcase)

### Карточка профиля разработчика (Developer Dossier Card)

<img src="assets/generated/profile-readme-demo.svg?v=f70c16ef" width="100%" alt="ALEX DEVELOPER" />

<br/>

### График динамики звёзд (Star Growth Trajectory)

<img src="assets/generated/starchart-readme-demo.svg?v=05566a8c" width="100%" alt="OPEN SOURCE STARS TRAJECTORY" />

<br/>

<img src="assets/generated/callout-readme-arch.svg?v=1b8f8525" width="100%" alt="АРХИТЕКТУРНЫЙ ПРИНЦИП" />

---

## 04 // Мульти-стилевая архитектура (3 Дизайн-парадигмы)

Дизайн-система предлагает 3 глобальные визуальные парадигмы:

| Парадигма | Стиль | Палитры по умолчанию | Особенности геометрии | Назначение |
| :--- | :--- | :--- | :--- | :--- |
| **Pixel / Retro-Tech** | `cyberpunk`, `tactical`, `matrix`, `tokyo` | Cyan / Purple, Amber / Orange, Phosphor Green | Пиксельный дизеринг, радары 360°, CRT-сканлайн, скобы | Игровые, хакерские и CLI проекты, яркие профили |
| **Clean / Modern Vector** | `clean-mono`, `modern-slate` | Monochrome, Matte Graphite, Accent Slate | Четкие векторные контуры 1px, сглаженные радиусы, чистый фон | Системный софт, DevOps, облачные утилиты |
| **Minimalist / Corporate** | `corporate-blue`, `academic-paper` | Deep Navy / Azure, Paper Monochrome | Сдержанная корпоративная типографика, 1px геометрия | Enterprise-библиотеки, научные статьи, исследования |

<br/>

## 05 // Стек технологий и поддерживаемое окружение

<img src="assets/generated/techstack-readme.svg?v=507e6c25" width="100%" alt="Tech Stack" />

<br/>

## 06 // Дорожная карта развития (Roadmap)

<img src="assets/generated/timeline-readme.svg?v=afff989d" width="100%" alt="Timeline" />

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

<img src="assets/generated/frame-readme-top.svg?v=59cdd27f" width="100%" />

<table width="100%">
<tr>
<td width="2000">

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

</td>
</tr>
</table>

<img src="assets/generated/frame-readme-bottom.svg?v=cd366dc0" width="100%" />

<br/>

> <img src="assets/generated/callout-quote-readme.svg?v=881fadc8" width="100%" alt="РУКОВОДСТВО ПО СТИЛЮ" />
>
> > **Навигация по документации**:
> > - Полный каталог всех компонентов во всех стилях доступен в **[CATALOG.md](CATALOG.md)**.
> > - Детальный разбор «сырой шаблон $\rightarrow$ скомпилированный результат» приведён в **[EXAMPLES.md](EXAMPLES.md)**.
> > - Лицензия проекта: [LICENSE](LICENSE) (MIT).

<br/>

<details >
<summary><kbd>▶ CLI_COMMANDS.LIST</kbd> <b>[ НАЖМИТЕ ДЛЯ СВОРАЧИВАНИЯ / РАЗВОРАЧИВАНИЯ ]</b> <code>[CLICK TO EXPAND]</code></summary>

<br/>

<img src="assets/generated/term-top-readme.svg?v=8c1b3913" width="100%" />

<table width="100%">
<tr>
<td width="2000">

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

</td>
</tr>
</table>

<img src="assets/generated/term-bottom-readme.svg?v=715dbd2d" width="100%" />

</details>

<br/><br/>

<a href="#top"><img src="assets/generated/footer-readme.svg?v=5390a594" width="100%" alt="▲ НАВЕРХ" /></a>
