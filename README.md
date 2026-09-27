# 📦 PIXEL README KIT — RETRO-CYBERPUNK & TACTICAL HUD DESIGN SYSTEM

<div id="top"></div>

<div align="center">

<img src="assets/generated/header-readme.svg" width="100%" alt="PIXEL README KIT" />

<br/><br/>

<a href="CATALOG.md"><img src="assets/generated/chip-readme-catalog.svg" alt="📚 КАТАЛОГ БЛОКОВ" /></a>
&nbsp;&nbsp;
<a href="EXAMPLES.md"><img src="assets/generated/chip-readme-examples.svg" alt="💡 ПРИМЕРЫ И РАЗБОР" /></a>
&nbsp;&nbsp;
<a href="#top"><img src="assets/generated/chip-readme-version.svg" alt="● v2.2.0 STABLE" /></a>
&nbsp;&nbsp;
<a href="LICENSE"><img src="assets/generated/chip-readme-license.svg" alt="MIT LICENSE" /></a>

<br/><br/>

<img src="assets/generated/divider-readme.svg" width="100%" alt="Divider cyberpunk" />

</div>

<br/>

## 📌 О проекте (Project Overview)

**Pixel Readme Kit** — модульная дизайн-система и генератор для оформления репозиториев и профилей GitHub в бескомпромиссной эстетике **ретро-киберпанка**, **тактических военных HUD** и **неонового стекла**.

Комплект создан для решения фундаментальных проблем стандартного оформления GitHub:
1. 🧊 **True Alpha Blending (Идеальный контраст на тёмной и светлой темах)**:
   Все элементы используют фирменную полупрозрачную подложку `rgba(10, 14, 23, 0.82)`. Текст и контуры не выгорают и сохраняют контрастность выше 7:1 как на тёмном фоне GitHub (`#0d1117`), так и на чистом белом (`#ffffff`).
2. 📋 **100% Живой копируемый Markdown-текст**:
   Документация, списки, ссылки, консольные команды и математика KaTeX внутри окон остаются полноценным текстом — их можно выделять, копировать и индексировать поиском.
3. 📐 **Прямое накрытие таблиц БЕЗ боковых зазоров (`x=1..849`)**:
   Оконные рамки ложатся вровень со стандартными таблицами GitHub (`<table width="100%">`) без адаптеров и лишних прокладок.
4. 💫 **Нативная SVG CSS-анимация**:
   Вращающийся луч радара 360°, бегущая CRT-сканлайн, прицельные лазеры, частотные эквалайзеры и светодиодные маяки работают на чистом SVG без внешних скриптов.

<br/>

<img src="assets/generated/callout-readme-arch.svg" width="100%" />

---

## 🏛️ 3 Глобальных стиля геометрии

Дизайн-система строго разделяет **геометрию (форму блоков)** и **цветовую палитру**:

| Стиль | Канонические цвета | Геометрия и силуэт | Механика распада (Decay) | Накрытие таблиц | Живая анимация |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 **Cyberpunk** | Cyan `#00C8D7`<br/>Purple `#A855F7` | Прямые углы, открытые кронштейны, пиксели `3×3` | Матричный пиксельный дизеринг (`3×3 ➔ 2×2 ➔ 1×1`) | Накрытие таблицы зубцами `x=1..849` | Радар 360°, CRT Scanline, PCB-пакет |
| 🟡 **Tactical Military** | Amber `#F59E0B`<br/>Orange `#EA580C` | 45° срезанные фаски (Chamfers), шевроны `▲` | Диагональные штрихи фасок `///` с затуханием | Накрытие фасками `45°` без зазоров | Пульсирующий прицел, маркеры захвата |
| 🟣 **Minimal Glass** | Tokyo Blue `#4F8BFF`<br/>Magenta `#A855F7` | Ультратонкая волосяная рамка 1px, зацепы `┌ ┐` | Микроточечное рассеивание (Micro-stipple) | Монолитная 3-строчная таблица | Спектральный 5-полосный эквалайзер |

> 🎨 **Свобода цвета**: Пользователь может использовать любой стиль с любыми hex-цветами: например, тактический стиль в цветах Matrix Green (`#00FF66`) или киберпанк в тёмно-красном Alert Red (`#FF0055`).

---

## 🚀 Быстрый старт (Quick Start)

Комплект предоставляет два независимых режима работы: **автоматический компилятор Markdown** и **автономный генератор CLI**.

### Вариант 1: Компилятор Markdown (Рекомендуемый воркфлоу)

1. Создайте шаблон документа (например, `README.template.md`) с декларативными директивами `<!-- pixel-kit:... -->`.
2. Запустите компилятор одной командой:
   ```bash
   python -m generator.cli compile --input README.template.md --output README.md --assets-dir assets/generated
   ```
3. Компилятор автоматически сгенерирует все SVG-ассеты, создаст 100% табличные обертки и сформирует готовый `README.md`.

### Вариант 2: Автономный генератор CLI

Генерация отдельных SVG-файлов по запросу:

```bash
# Флагманская шапка (с кастомными тегами 3 уровня):
python -m generator.cli header --style cyberpunk --title "MY-PROJECT" --subtitle "SYSTEM RUNTIME" --spec1 "ARCH: TRANSLUCENT" --spec2 "TEXT: LIVE MARKDOWN" -o assets/header.svg

# Оконная рамка:
python -m generator.cli frame --style tactical --type top --title "MODULE_SPEC" -o assets/frame-top.svg
python -m generator.cli frame --style tactical --type bottom -o assets/frame-bottom.svg

# Адаптивный чип-ссылка:
python -m generator.cli chip --style cyberpunk --type closed --text "⚡ v2.2.0" -o assets/chip.svg

# Инлайн-алерт:
python -m generator.cli callout --style minimal --type note --title "NOTICE" --subtitle "High performance" -o assets/callout.svg
```

### Вариант 3: Использование в качестве Agent Skill (Antigravity, Claude Code, Cursor, Cline)

Pixel Readme Kit полностью упакован как официальный навык для AI-агентов. Вы можете установить его одной командой:

```bash
# Установка глобально для всех агентов в системе:
npx skills add Kazinagg/pixel-readme-kit -g -y

# Или установка локально в текущий проект:
npx skills add Kazinagg/pixel-readme-kit -y
```

После установки любой поддерживаемый AI-агент сразу поймет синтаксис директив `<!-- pixel-kit:... -->` и сможет автоматически собирать HUD README для ваших проектов.

---

## 🪟 Интерактивный пример окна контента

<img src="assets/generated/frame-readme-top.svg" width="100%" />

<table width="100%">
<tr>
<td width="2000">

### 🧬 Спецификация подсистем ядра

Контент внутри окон остаётся полноценным Markdown:

| Подсистема | Протокол | Статус | Задержка |
| :--- | :--- | :--- | :--- |
| **Render Engine** | `SVG_NATIVE_XML` | `● ACTIVE` | `0.00 ms` |
| **Alpha Blending** | `RGBA_0.82` | `● DUAL_THEME_PASS` | `0.12 ms` |
| **Matrix Radar** | `360_DEG_SWEEP` | `● SCANNING` | `16.6 ms (60 FPS)` |

```bash
# Клонирование и быстрый запуск
git clone https://github.com/Kazinagg/pixel-readme-kit.git
cd pixel-readme-kit
python -m generator.cli --help
```

</td>
</tr>
</table>

<img src="assets/generated/frame-readme-bottom.svg" width="100%" />

<br/>

> <img src="assets/generated/callout-quote-readme.svg" width="100%" />
>
> > **Навигация по документации**:
> > - Полный каталог всех 8 типов компонентов во всех стилях доступен в **[CATALOG.md](CATALOG.md)**.
> > - Детальный разбор «сырой шаблон без генерации $\rightarrow$ сгенерированный результат» с GitHub Actions приведён в **[EXAMPLES.md](EXAMPLES.md)**.
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
python -m generator.cli header --help    # Заглавные шапки
python -m generator.cli footer --help    # Закрывающие пластины
python -m generator.cli callout --help   # Инлайн-алерты и плашки
python -m generator.cli frame --help     # Рамки окон (top/bottom)
python -m generator.cli chip --help      # Чипы и пилюли
python -m generator.cli divider --help   # Разделители глав
python -m generator.cli splitter --help  # Сплиттеры подмодулей
python -m generator.cli compile --help   # Компилятор Markdown
```

</td>
</tr>
</table>

<img src="assets/generated/term-bottom-readme.svg" width="100%" />

</details>

<br/><br/>

<a href="#top"><img src="assets/generated/footer-readme.svg" width="100%" alt="▲ НАВЕРХ" /></a>
