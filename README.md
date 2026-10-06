# README KIT — UNIVERSAL DESIGN SYSTEM FOR GITHUB REPOSITORIES & DEVELOPER PROFILES

<div id="top"></div>

<div align="center">

<img src="assets/generated/header-readme.svg" width="100%" alt="README KIT" />

<br/><br/>

<a href="CATALOG.md"><img src="assets/generated/chip-readme-catalog.svg" alt="[DOCS] КАТАЛОГ БЛОКОВ" /></a>
&nbsp;&nbsp;
<a href="EXAMPLES.md"><img src="assets/generated/chip-readme-examples.svg" alt="[SPEC] ПРИМЕРЫ И РАЗБОР" /></a>
&nbsp;&nbsp;
<a href="#top"><img src="assets/generated/chip-readme-version.svg" alt="● v5.0.0 STABLE" /></a>
&nbsp;&nbsp;
<a href="https://github.com/Kazinagg/pixel-readme-kit/stargazers"><img src="assets/generated/chip-readme-stars.svg" alt="★ 2" /></a>
&nbsp;&nbsp;
<a href="https://github.com/Kazinagg/pixel-readme-kit/network/members"><img src="assets/generated/chip-readme-forks.svg" alt="FORKS: 0" /></a>
&nbsp;&nbsp;
<a href="https://github.com/Kazinagg/pixel-readme-kit"><img src="assets/generated/chip-readme-license.svg" alt="LICENSE: MIT" /></a>

<br/><br/>

<img src="assets/generated/divider-readme.svg" width="100%" alt="Divider cyberpunk" />

</div>

<br/>

## 01 // Телеметрия системы (System Telemetry)

<img src="assets/generated/metrics-readme.svg" width="100%" alt="Metrics" />

<br/>

<img src="assets/generated/progress-readme.svg" width="100%" alt="V5.0 REPO &amp; PROFILE EVOLUTION COMPLETE" />

<br/>

## 02 // Концепция проекта (Project Overview)

**Readme Kit** — универсальная дизайн-система, генератор ассетов и интерактивная визуальная студия для оформления **Репозиториев (Repositories)** и **Профилей разработчиков (Developer Profiles `username/username`)** на GitHub.

Комплект предоставляет гибкие инструменты для двух ключевых сценариев:
1. **Оформление репозиториев (Repositories Showcase)**:
   - Библиотеки, CLI-утилиты, веб-сервисы, монорепозитории и исследовательские отчеты.
   - Модульные окна контента, интерактивные терминалы, матрицы стека, плашки алертов и футеры.
2. **Оформление профилей разработчиков (Developer Profiles)**:
   - Флагманские карточки профиля (`<img src="assets/generated/profile-cyberpunk-1.svg" width="100%" alt="ALEX DEVELOPER" />`) со стилизованным аватаром, LED-индикатором статуса, 3D-типографикой и био.
   - График динамики звёзд и активности (`<img src="assets/generated/starchart-cyberpunk-1.svg" width="100%" alt="STAR GROWTH TRAJECTORY" />`) с координатной сеткой и градиентной заливкой.
   - Витрины ключевых проектов и социальные чипы.

<br/>

## 03 // Флагманские компоненты v5.0 (Showcase)

### Карточка профиля разработчика (Developer Dossier Card)

<img src="assets/generated/profile-readme-demo.svg" width="100%" alt="ALEX DEVELOPER" />

<br/>

### График динамики звёзд (Star Growth Trajectory)

<img src="assets/generated/starchart-readme-demo.svg" width="100%" alt="OPEN SOURCE STARS TRAJECTORY" />

<br/>

<img src="assets/generated/callout-readme-arch.svg" width="100%" alt="АРХИТЕКТУРНЫЙ ПРИНЦИП" />

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

<img src="assets/generated/techstack-readme.svg" width="100%" alt="Tech Stack" />

<br/>

## 06 // Дорожная карта развития (Roadmap)

<img src="assets/generated/timeline-readme.svg" width="100%" alt="Timeline" />

<br/>

## 07 // Руководство по началу работы (Quick Start Guide)

### 1. Интерактивная Web-студия (Live Preview & Studio)
```bash
# Запуск веб-редактора с мгновенным Live Reload (SSE):
python -m generator.cli studio --open
```

### 2. Инициализация шаблона с помощью Scaffolder
```bash
# Оформление репозитория:
python -m generator.cli init --category repo --type library --title "MY-AWESOME-LIB"

# Оформление профиля разработчика:
python -m generator.cli init --category profile --type developer --title "ALEX DEVELOPER"
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

## 08 // Интерактивный пример окна контента

<img src="assets/generated/frame-readme-top.svg" width="100%" />

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

<img src="assets/generated/frame-readme-bottom.svg" width="100%" />

<br/>

> <img src="assets/generated/callout-quote-readme.svg" width="100%" alt="РУКОВОДСТВО ПО СТИЛЮ" />
>
> > **Навигация по документации**:
> > - Полный каталог всех компонентов во всех стилях доступен в **[CATALOG.md](CATALOG.md)**.
> > - Детальный разбор «сырой шаблон $\rightarrow$ скомпилированный результат» приведён в **[EXAMPLES.md](EXAMPLES.md)**.
> > - Лицензия проекта: [LICENSE](LICENSE) (MIT).

<br/>

<details >
<summary><kbd>▶ CLI_COMMANDS.LIST</kbd> <b>[ НАЖМИТЕ ДЛЯ СВОРАЧИВАНИЯ / РАЗВОРАЧИВАНИЯ ]</b> <code>[CLICK TO EXPAND]</code></summary>

<br/>

<img src="assets/generated/term-top-readme.svg" width="100%" />

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

<img src="assets/generated/term-bottom-readme.svg" width="100%" />

</details>

<br/><br/>

<a href="#top"><img src="assets/generated/footer-readme.svg" width="100%" alt="▲ НАВЕРХ" /></a>
