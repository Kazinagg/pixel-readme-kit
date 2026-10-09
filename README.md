<img src="assets/generated/metrics-modern-clean-1.svg?v=b065ba33" width="100%" alt="Metrics" />

<br/>

<img src="assets/generated/progress-readme.svg?v=a62d0fcd" width="100%" alt="UNIVERSAL CUSTOMIZATION SYSTEM &amp; DESIGN ENGINE COMPLETE" />

<br/>

## 02 // Концепция проекта (Project Overview)

**ReadmeKit** — универсальная модульная **система кастомизации**, генератор динамических SVG-ассетов и интерактивная дизайн-студия для оформления **Репозиториев (Repositories Showcase)** и **Профилей разработчиков (Developer Profiles `username/username`)** на GitHub.

Проект вырос из моно-темы в **полноценный дизайн-движок кастомизации**:
- **Ортогональная архитектура**: визуальная форма (геометрия стиля) полностью отделена от цветовой палитры (темы и пресеты). Вы вольны комбинировать любой стиль с любой палитрой.
- **Zero-Flicker адаптивный SVG (`mode="auto"`)**: единый автономный SVG-файл использует нативные CSS-переменные и медиа-запрос `@media (prefers-color-scheme: dark)`. Переключается мгновенно вместе с системной темой браузера без дублирования файлов и мерцания.
- **Два ключевых сценария кастомизации**:
  1. **Оформление репозиториев (Repositories Showcase & Documentation)**:
     - Оформление библиотек, CLI-утилит, веб-сервисов, монорепозиториев и аналитических отчетов.
     - Модульные окна контента с копируемым Markdown внутри, сворачиваемые интерактивные терминалы, матрицы стека технологий, плашки алертов, KPI-метрики и футеры.
  2. **Оформление профилей разработчиков (Developer Profiles & Portfolios)**:
     - Флагманские досье-карточки профиля (`&lt;!-- readme-kit:profile ... --&gt;`) с аватаром, LED-индикатором статуса, специализацией, локацией и био.
     - График динамики звёзд и активности (`&lt;!-- readme-kit:starchart ... --&gt;`) с гладкими кривыми Безье, координатной сеткой и градиентной заливкой.
     - Витрины ключевых проектов, OpenGraph превью-карточки (1280x640) и социальные чипы.

<br/>

## 03 // Флагманские компоненты v5.1 (Showcase)

### Карточка профиля разработчика (Developer Dossier Card)

<img src="assets/generated/profile-readme-demo.svg?v=a96de362" width="100%" alt="ALEX DEVELOPER" />

<br/>

### График динамики звёзд (Star Growth Trajectory)

<img src="assets/generated/starchart-readme-demo.svg?v=ade7acad" width="100%" alt="OPEN SOURCE STARS TRAJECTORY" />

<br/>

<img src="assets/generated/callout-readme-arch.svg?v=16977a67" width="100%" alt="АРХИТЕКТУРНЫЙ ПРИНЦИП" />

---

## 04 // Мульти-стилевая архитектура (4 Дизайн-парадигмы)

Дизайн-система предлагает 4 глобальные визуальные парадигмы с ортогональным разделением **Геометрии (`style`)** и **Цветовых палитр (`theme`)**:

| Парадигма (Стиль `style`) | Канонические темы (`theme`) | Основная палитра | Особенности геометрии | Статус готовности |
| :--- | :--- | :--- | :--- | :--- |
| **Clean / Modern Vector** (`modern`) | `slate-dark`, `nordic-frost`, `linear-violet`, `emerald-clean` | Matte Graphite, Nordic Frost, Linear Violet, Emerald Clean | Четкие векторные контуры 1px, сглаженные скругления, pill-бейджи, кривые Безье | ● **READY (CORE)** |
| **Pixel / Retro-Tech** (`pixel`) | `cyberpunk`, `tactical`, `tokyo`, `matrix`, `amber` | Cyan / Magenta, Phosphor Amber, Tokyo Neon, Matrix Green | 3D пиксельный шрифт, радары 360°, CRT-сканлайн, скобы 45°, дизеринг | ● **READY (CORE)** |
| **Hand-Drawn / Sketch** (`sketch`) | `excali-dark`, `whiteboard`, `notebook-graph`, `blueprint-sketch` | Excali Dark, Clean Whiteboard, Graph Paper, Blueprint Blue | Живой штрих руки (Jitter), двойные контуры, карандашная штриховка, шрифт заметок | ● **READY (CORE)** |
| **Minimalist / Corporate** (`corporate`) | `academic-paper`, `enterprise-navy`, `swiss-mono` | Academic Paper, Enterprise Navy, Swiss Monochrome | Сдержанная типографика, 1px строгая геометрия, швейцарский модернизм | ● **READY (CORE)** |

> [!NOTE]
> **Канонические темы по стилям**:
> 1. **Modern Vector Style**: `slate-dark` (графит + циан), `nordic-frost` (арктический лед), `linear-violet` (Linear App космос), `emerald-clean` (Supabase/Vercel изумруд).
> 2. **Pixel Style**: `cyberpunk` (неон), `tactical` (янтарь), `tokyo` (ночной Токио), `matrix` (зеленый монохром), `amber` (янтарь CRT).
> 3. **Sketch Style**: `excali-dark` (тёмный Excalidraw), `whiteboard` (белая доска), `notebook-graph` (тетрадь в клетку), `blueprint-sketch` (чертёж).
> 4. **Corporate Style**: `academic-paper` (академический монохром), `enterprise-navy` (корпоративный синий), `swiss-mono` (швейцарская сетка).

<br/>

## 05 // Стек технологий и поддерживаемое окружение

<img src="assets/generated/techstack-readme.svg?v=63e58b7e" width="100%" alt="Tech Stack" />

<br/>

## 06 // Дорожная карта развития (Roadmap)

<img src="assets/generated/timeline-readme.svg?v=4f7c33c4" width="100%" alt="Timeline" />

<br/>

## 07 // Руководство по началу работы (Quick Start Guide)

### 1. Мгновенный запуск Студии в браузере (Zero-Install)
```bash
# Запуск через pipx без предварительного клонирования (рекомендуется):
pipx run readme-kit studio --open

# Или классическая установка пакета через pip:
pip install readme-kit
readme-kit studio --open

# (Также сохранена обратная совместимость вызова через pixel-kit studio --open)
```

### 2. Инициализация шаблона с помощью Scaffolder
```bash
# Оформление репозитория (Modern Vector, Hand-Drawn Sketch или Retro-Pixel):
readme-kit init --category repo --type modern --title "MY-MODERN-LIB"
readme-kit init --category repo --type sketch --title "MY-SKETCH-PROJECT"
readme-kit init --category repo --type library --title "MY-AWESOME-LIB"

# Оформление профиля разработчика (Clean Vector, Dossier или Sketch):
readme-kit init --category profile --type modern --title "ALEX DEVELOPER"
readme-kit init --category profile --type sketch --title "ALEX DEVELOPER"
readme-kit init --category profile --type developer --title "ALEX DEVELOPER"
```

### 3. Компиляция и синхронизация (с автоподхватом данных GitHub)
```bash
# Полная сборка с актуализацией звезд, очисткой сирот и сбросом кэша Camo:
readme-kit sync

# Или ручная компиляция шаблона Markdown:
readme-kit compile --fetch-github --clean-assets --bust-cache
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
    "readme-kit": {
      "command": "python",
      "args": ["-m", "generator.mcp_server"],
      "cwd": "/path/to/readme-kit"
    }
  }
}
```

---

## 08 // Интерактивный пример окна контента

<table width="100%">
<tr>
<td width="100%" align="center">
<img src="assets/generated/frame-readme-top.svg?v=77197807" width="100%" />
</td>
</tr>
<tr>
<td width="2000">

### [SPEC] Спецификация подсистем ядра ReadmeKit

Контент внутри окон остаётся полноценным копируемым Markdown:

| Подсистема | Протокол | Статус | Задержка |
| :--- | :--- | :--- | :--- |
| **Multi-Style Engine** | `VECTOR + PIXEL + SKETCH + CORP` | `● QUAD-PARADIGM` | `0.00 ms` |
| **Theme Engine** | `CSS_VARS_MEDIA_QUERY` | `● AUTO_ADAPTIVE` | `0.00 ms` |
| **Incremental Cache** | `SHA-256 DIGEST` | `● 98% HIT_RATE` | `0.02 s` |
| **Live Studio** | `SSE REALTIME SYNC` | `● 300ms INTERVAL` | `< 50 ms` |

```bash
# Клонирование и запуск студии кастомизации
git clone https://github.com/Kazinagg/pixel-readme-kit.git
cd pixel-readme-kit
python -m generator.cli studio
```

</td>
</tr>
<tr>
<td width="100%" align="center">
<img src="assets/generated/frame-readme-bottom.svg?v=06f08ce7" width="100%" />
</td>
</tr>
</table>

<br/>

> <img src="assets/generated/callout-quote-readme.svg?v=b45e22ae" width="100%" alt="РУКОВОДСТВО ПО СТИЛЮ" />
>
> > **Навигация по документации**:
> > - Полный каталог всех компонентов во всех стилях доступен в **[CATALOG.md](CATALOG.md)**.
> > - Детальный разбор «сырой шаблон $\rightarrow$ скомпилированный результат» приведён в **[EXAMPLES.md](EXAMPLES.md)**.
> > - Лицензия проекта: [LICENSE](LICENSE) (MIT).

<br/>

<details >
<summary><kbd>▶ CLI_COMMANDS.LIST</kbd> <b>[ НАЖМИТЕ ДЛЯ СВОРАЧИВАНИЯ / РАЗВОРАЧИВАНИЯ ]</b> <code>[CLICK TO EXPAND]</code></summary>

<br/>

<img src="assets/generated/term-top-readme.svg?v=0eb73b9e" width="100%" />

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

<img src="assets/generated/term-bottom-readme.svg?v=4515d6ef" width="100%" />

</details>

<br/><br/>

<a href="#top"><img src="assets/generated/footer-readme.svg?v=d4702d82" width="100%" alt="▲ НАВЕРХ" /></a>
