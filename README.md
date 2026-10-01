# 📦 PIXEL README KIT — RETRO-CYBERPUNK & TACTICAL HUD DESIGN SYSTEM

<div id="top"></div>

<div align="center">

<img src="assets/generated/header-readme.svg" width="100%" alt="PIXEL README KIT" />

<br/><br/>

<a href="CATALOG.md"><img src="assets/generated/chip-readme-catalog.svg" alt="📚 КАТАЛОГ БЛОКОВ" /></a>
&nbsp;&nbsp;
<a href="EXAMPLES.md"><img src="assets/generated/chip-readme-examples.svg" alt="💡 ПРИМЕРЫ И РАЗБОР" /></a>
&nbsp;&nbsp;
<a href="#top"><img src="assets/generated/chip-readme-version.svg" alt="● v4.0.0 STABLE" /></a>
&nbsp;&nbsp;
<a href="https://github.com/Kazinagg/pixel-readme-kit/stargazers"><img src="assets/generated/chip-readme-stars.svg" alt="★ 1" /></a>
&nbsp;&nbsp;
<a href="https://github.com/Kazinagg/pixel-readme-kit/network/members"><img src="assets/generated/chip-readme-forks.svg" alt="🍴 0" /></a>
&nbsp;&nbsp;
<a href="https://github.com/Kazinagg/pixel-readme-kit"><img src="assets/generated/chip-readme-license.svg" alt="⚖ MIT" /></a>

<br/><br/>

<img src="assets/generated/divider-readme.svg" width="100%" alt="Divider cyberpunk" />

</div>

<br/>

## 📊 Ключевые показатели v4.0 (System Telemetry)

<img src="assets/generated/metrics-readme.svg" width="100%" alt="Metrics" />

<br/>

<img src="assets/generated/progress-readme.svg" width="100%" alt="V4.0 EVOLUTION PROGRESS (5/5 SPRINTS)" />

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

<img src="assets/generated/callout-readme-arch.svg" width="100%" alt="АРХИТЕКТУРНЫЙ ПРИНЦИП" />

---

## 🛠️ Стек технологий и поддерживаемое окружение

<img src="assets/generated/techstack-readme.svg" width="100%" alt="Tech Stack" />

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

<img src="assets/generated/timeline-readme.svg" width="100%" alt="Timeline" />

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

<img src="assets/generated/frame-readme-top.svg" width="100%" />

<table width="100%">
<tr>
<td width="2000">

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

</td>
</tr>
</table>

<img src="assets/generated/term-bottom-readme.svg" width="100%" />

</details>

<br/><br/>

<a href="#top"><img src="assets/generated/footer-readme.svg" width="100%" alt="▲ НАВЕРХ" /></a>
