<div id="top"></div>

<div align="center">

<!-- MAIN 3D CYBERPUNK TERMINAL HEADER (Radar 360° + CRT Scanline + Equalizer) -->
<img src="assets/headers/header-terminal-cyberpunk.svg" width="100%" alt="PIXEL-KIT TRANSLUCENT HUD" />

<br/>

<!-- NAVIGATION PILLS -->
<a href="#suite-1-cyberpunk-terminal-workstation"><img src="assets/chips/nav-brackets.svg" alt="Suite 1: Terminal" /></a>
<a href="#suite-2-tactical-military-hud"><img src="assets/chips/nav-enclosure.svg" alt="Suite 2: Tactical" /></a>
<a href="#suite-3-cyber-gutter-terminal"><img src="assets/chips/nav-chips.svg" alt="Suite 3: Gutter" /></a>
<a href="CATALOG.md"><img src="assets/chips/nav-catalog.svg" alt="Полный каталог" /></a>
<a href="TEST_SUITE.md"><img src="assets/chips/chip-chamfer-spec.svg" alt="Лаборатория тестов" /></a>
<a href="#quick-start--cli-generator"><img src="assets/chips/nav-guide.svg" alt="Guide" /></a>

<br/><br/>

<!-- ANIMATED PCB DIVIDER (Traveling Data Packet) -->
<img src="assets/divider-pcb-cyan.svg" width="100%" alt="PCB Divider" />

</div>

## 📌 OVERVIEW // О ПРОЕКТЕ

**Pixel Readme Kit v2.2** — модульная дизайн-система в эстетике ретро-киберпанка, тактических HUD-терминалов и полупрозрачного стекла.

Создана для оформления GitHub профилей и репозиториев без недостатков статических картинок:
- <img src="assets/bullets/bullet-diamond-cyan.svg" align="center" /> 🧊 **True Alpha Blending (Контрастность на темной и светлой темах)**: `rgba(10, 14, 23, 0.82)` гарантирует глубокую темную подложку как на черном фоне GitHub Dark (`#0d1117`), так и на белом фоне GitHub Light (`#ffffff`). Текст и границы не выгорают и сохраняют контрастность выше 7:1.
- <img src="assets/bullets/bullet-arrow-pink.svg" align="center" /> 📋 **100% Живой Markdown-текст**: Документация, команды консоли, списки и LaTeX-формулы остаются копируемыми и индексируемыми.
- <img src="assets/bullets/bullet-check-cyan.svg" align="center" /> 📐 **3 Полноценных тематических сюиты**: Cyberpunk Terminal, Tactical Military HUD, Cyber Gutter Terminal.
- <img src="assets/bullets/bullet-marker-cyan.svg" align="center" /> 💫 **Живые SVG CSS-анимации**: Вращающийся луч радара 360°, бегущая CRT-строка сканирования, прицельный лазер, бегущий пакет данных по плате, каскадный импульс лестниц и пульсирующие светодиоды.
- <img src="assets/bullets/bullet-diamond-cyan.svg" align="center" /> 📦 **100+ SVG-компонентов**: Полный визуальный справочник доступен в **[Каталоге компонентов (CATALOG.md)](CATALOG.md)**.

<br/>

<img src="assets/callouts/callout-note-cyan.svg" width="100%" alt="Architecture Note" />

> **АРХИТЕКТУРНЫЙ ПРИНЦИП**: Все элементы используют прозрачность стекла `rgba(...)` и нативные SVG-примитивы с отрисовкой `crispEdges`. Они никогда не замыливаются и одинаково безупречно выглядят на Retina-экранах и мобильных устройствах.

---

<div id="suite-1-cyberpunk-terminal-workstation"></div>

### 🟢 1. SUITE 1: CYBERPUNK TERMINAL WORKSTATION

Флагманский стиль открытого терминала. Верхний и нижний фреймы снабжены направляющими зубцами (`│` и `│`), смотрящими строго в сторону контента. Внутри продемонстрировано **горизонтальное расщепление текста** через Т-образный соединитель подмодулей:

<!-- TOP FRAME (MATRIX GREEN) -->
<img src="assets/frames/frame-top-brackets-green.svg" width="100%" alt="Matrix Top Bracket" />

> #### 🧬 MODULE 01 // RUNTIME KERNEL SPEC
>
> Живой Markdown-контент находится строго по центру между направляющими зубцами:
>
> ```bash
> # Клонирование и сборка терминального комплекта
> git clone https://github.com/Kazinagg/pixel-readme-kit.git
> python generator/cli.py --theme matrix --style terminal --title "CYBER-CORE"
> ```
>
> - <img src="assets/bullets/bullet-check-cyan.svg" align="center" /> <img src="assets/chips/chip-pulse-online.svg" align="center" /> ➔ **Ядро системы активно** (живой мерцающий маяк)
> - <img src="assets/bullets/bullet-diamond-cyan.svg" align="center" /> <img src="assets/chips/chip-chamfer-matrix.svg" align="center" /> ➔ Модуль RLE-сжатия 3D пиксельных шрифтов

<!-- SUB-BLOCK SPLITTER (TERMINAL T-JUNCTION) -->
<img src="assets/splitters/splitter-terminal-cyberpunk.svg" width="100%" alt="Terminal Splitter" />

> #### ⚡ MODULE 02 // TELEMETRY & HARDWARE BUS
>
> Второй расщепленный блок с параметрами окружения:
> - <img src="assets/bullets/bullet-marker-cyan.svg" align="center" /> <img src="assets/chips/chip-closed-core.svg" align="center" /> ➔ Архитектура True Alpha Blending (`rgba(10, 14, 23, 0.82)`)
> - <img src="assets/bullets/bullet-check-cyan.svg" align="center" /> <img src="assets/chips/chip-closed-cli.svg" align="center" /> ➔ Чистый Python 3.8+ без внешних библиотек

<!-- BOTTOM FRAME (MATRIX GREEN) -->
<img src="assets/frames/frame-bottom-brackets-green.svg" width="100%" alt="Matrix Bottom Bracket" />

---

<div id="suite-2-tactical-military-hud"></div>

### 🟡 2. SUITE 2: TACTICAL MILITARY HUD // TRANSITIONAL SHOULDERS

Боевой интерфейс со скошенными углами 45°. Для идеального визуального сопряжения между фреймами и таблицей GitHub используются **переходные адаптеры плеч (Transitional Shoulders)**, расширяющие контур под поля таблицы и плавно замыкающие его внизу:

<!-- TOP FRAME (AMBER CHAMFER 45°) -->
<img src="assets/frames/frame-top-chamfer-amber.svg" width="100%" alt="Amber Chamfer Top" />

<!-- TRANSITIONAL SHOULDER ADAPTER (TOP: EXPAND BUS) -->
<img src="assets/adapters/transition-shoulder-top-amber.svg" width="100%" alt="Transition Shoulder Top" />

<table border="0" cellpadding="0" cellspacing="0" width="100%">
  <tr>
    <td width="40" valign="top" align="center" style="line-height: 0; padding: 0;">
      <img src="assets/rails/rail-left-ladder-amber.svg" height="250" width="14" />
    </td>
    <td style="padding: 10px 24px;">

#### 🛰️ TACTICAL TELEMETRY STREAM
Внутри замкнутого бокса данные защищены боковыми шинами.

<img src="assets/callouts/callout-warning-amber.svg" width="100%" alt="Tactical Warning" />

> **ПРАВИЛО РАЗМЕТКИ**: Для внешних рельсов используйте ширину ячеек `width="40"` или `width="54"`, чтобы предотвратить сплющивание картинок из-за правила GitHub table padding.

| Подсистема | Режим | Анимация | Статус |
| :--- | :--- | :--- | :--- |
| `Radar 360°` | Full Sweep | `<animateTransform>` | <img src="assets/chips/chip-pulse-live.svg" align="center" /> |
| `Target Laser` | 4s Traverse | `@keyframes targetScan` | <img src="assets/chips/chip-chamfer-spec.svg" align="center" /> |
| `Ladder Bus` | Cascade Glow | `@keyframes rungGlow` | `ACTIVE` |

    </td>
    <td width="40" valign="top" align="center" style="line-height: 0; padding: 0;">
      <img src="assets/rails/rail-right-ladder-amber.svg" height="250" width="14" />
    </td>
  </tr>
</table>

<!-- SUB-BLOCK SPLITTER (TACTICAL CHEVRON 45°) -->
<img src="assets/splitters/splitter-tactical-amber.svg" width="100%" alt="Tactical Splitter" />

<!-- TRANSITIONAL SHOULDER ADAPTER (BOTTOM: CONTRACT BUS) -->
<img src="assets/adapters/transition-shoulder-bottom-amber.svg" width="100%" alt="Transition Shoulder Bottom" />

<!-- BOTTOM FRAME (AMBER CHAMFER 45°) -->
<img src="assets/frames/frame-bottom-chamfer-amber.svg" width="100%" alt="Amber Chamfer Bottom" />

<br/>

<!-- ANIMATED LASER DIVIDER -->
<img src="assets/divider-laser-amber.svg" width="100%" alt="Laser Divider" />

---

<div id="suite-3-cyber-gutter-terminal"></div>

### 🔵 3. SUITE 3: CYBER GUTTER TERMINAL // 54PX DITHER RAILS

Так как GitHub автоматически накладывает рамки на ячейки таблиц, этот режим **обыгрывает рамки как намеренную структуру интерфейса**:
- Боковые ячейки увеличены до **54px**, благодаря чему графические элементы (`gutter-left-cyberpunk.svg`) **никогда не сжимаются и не съезжают**.
- Внутри: **шахматный дизеринг ("шашкой")**, **рассеянная пиксельная пыль**, прерывистые направляющие шины данных и контрольные метки `0x...`.
- Внутри блока показано **вертикальное расщепление контента на 2 колонки**:

<!-- TOP FRAME (CYBERPUNK CYAN ENCLOSURE) -->
<img src="assets/frames/frame-top-enclosure-cyan.svg" width="100%" alt="Cyberpunk Top Frame" />

<table border="0" cellpadding="0" cellspacing="0" width="100%">
  <tr>
    <td width="54" align="center" valign="top" style="padding: 0;">
      <img src="assets/rails/gutter-left-cyberpunk.svg" width="54" height="210" />
    </td>
    <td style="padding: 10px 24px;">

#### ⚡ RETRO CYBER-GUTTER // 2-COLUMN DECOMPOSITION
Границы таблицы GitHub становятся естественными разделителями между экраном и боковыми шинами:

<!-- 2-COLUMN SPLIT INSIDE TEXT -->
<table width="100%">
  <tr>
    <td width="50%" valign="top">
      <b>[ 📊 COLUMN A: TELEMETRY ]</b><br/><br/>
      <img src="assets/bullets/bullet-square-green.svg" align="center" /> <img src="assets/chips/chip-decay-right-src.svg" align="center" /> ➔ <code>generator/builder.py</code><br/>
      <img src="assets/bullets/bullet-square-green.svg" align="center" /> <img src="assets/chips/chip-decay-right-tag.svg" align="center" /> ➔ Релиз v2.2 Dual-Theme<br/>
      <img src="assets/bullets/bullet-check-cyan.svg" align="center" /> <img src="assets/chips/chip-decay-right-done.svg" align="center" /> ➔ 100% валидация XML
    </td>
    <td width="50%" valign="top">
      <b>[ 🛠️ COLUMN B: COMMANDS ]</b><br/><br/>
      <img src="assets/bullets/bullet-prompt-green.svg" align="center" /> <code>python cli.py --theme cyberpunk</code><br/>
      <img src="assets/bullets/bullet-prompt-green.svg" align="center" /> <code>python cli.py --theme amber</code><br/>
      <img src="assets/bullets/bullet-prompt-green.svg" align="center" /> <code>python cli.py --theme tokyo</code>
    </td>
  </tr>
</table>

    </td>
    <td width="54" align="center" valign="top" style="padding: 0;">
      <img src="assets/rails/gutter-right-cyberpunk.svg" width="54" height="210" />
    </td>
  </tr>
</table>

<!-- SUB-BLOCK SPLITTER (DECAY DITHER) -->
<img src="assets/splitters/splitter-decay-tokyo.svg" width="100%" alt="Decay Splitter" />

<!-- BOTTOM FRAME (CYBERPUNK CYAN ENCLOSURE) -->
<img src="assets/frames/frame-bottom-enclosure-cyan.svg" width="100%" alt="Cyberpunk Bottom Frame" />

---

<div id="header-styles-gallery"></div>

### 🏛️ HEADER STYLES GALLERY // 3 ВАРИАНТА ШАПОК

В дизайн-системе сохранены все созданные варианты шапок с уникальными эффектами:

#### Вариант 1: Cyberpunk 3D Workstation (Radar 360° + CRT Scanline + Spectrum)
Флагманская рабочая станция с вращающимся лучом радара 360°, бегущей CRT-строкой сканирования, эквалайзером и 3D-шрифтом:
<img src="assets/headers/header-terminal-cyberpunk.svg" width="100%" alt="Terminal Header" />

#### Вариант 2: Tactical Military HUD (Sweeping Laser + Hazard Stripes)
Боевой тактический интерфейс со скошенными углами 45°, бегущим лучом прицела и блокировкой цели:
<img src="assets/headers/header-tactical-amber.svg" width="100%" alt="Tactical Header" />

#### Вариант 3: Minimal Glass & Live Equalizer
Широкий минималистичный неоновый баннер с прыгающими полосами эквалайзера и дышащей каймой:
<img src="assets/headers/header-minimal-tokyo.svg" width="100%" alt="Minimal Header" />

---

### 🎨 ПАЛИТРЫ И КАЛИБРОВКА КОНТРАСТНОСТИ

Все цвета откалиброваны для одинаковой читаемости на темном (`#0D1117`) и белом (`#FFFFFF`) фонах:

| Палитра | Назначение | Основной цвет | Акцент 1 | Акцент 2 |
| :--- | :--- | :--- | :--- | :--- |
| **`cyberpunk`** | Kazinagg Core | `#00C8D7` (Electric Cyan) | `#FF0055` (Laser Pink) | `#A855F7` (Cyber Purple) |
| **`matrix`** | Emerald Terminal | `#00D26A` (Matrix Green) | `#00E5FF` (Teal Link) | `#EAB308` (Cyber Yellow) |
| **`amber`** | Retro CRT Phosphor | `#F59E0B` (CRT Amber) | `#EA580C` (CRT Orange) | `#10B981` (Retro Mint) |
| **`tokyo`** | Tokyo Vaporwave | `#4F8BFF` (Tokyo Blue) | `#A855F7` (Tokyo Violet)| `#06B6D4` (Cyan Accent) |

---

---

<div id="component-catalog"></div>

### 📚 БИБЛИОТЕКА КОМПОНЕНТОВ // COMPONENT CATALOG

<img src="assets/callouts/callout-success-green.svg" width="100%" alt="Component Library Ready" />

> **100+ ГОТОВЫХ SVG-КОМПОНЕНТОВ**: Дизайн-система содержит более сотни калиброванных элементов: 3 стиля шапок, 4 закрывающих футера с навигацией, 16 пиксельных маркеров списков, 19 чипов, рамки окон, адаптеры 45°, боковые шины и разделители.
>
> Чтобы титульный README оставался чистым и сфокусированным, подробный визуальный справочник со всеми файлами, превью и сниппетами вынесен в отдельный документ:

<br/>

<div align="center">

<h3>🔗 <a href="CATALOG.md">👉 [ ПЕРЕЙТИ В ПОЛНЫЙ ВИЗУАЛЬНЫЙ КАТАЛОГ (CATALOG.MD) ] 👈</a></h3>

<br/>

<a href="CATALOG.md"><img src="assets/chips/nav-catalog.svg" alt="Каталог" /></a>
&nbsp;
<a href="CATALOG.md#4-пиксельные-маркеры-списков-pixel-bullet-lists-1414"><img src="assets/chips/chip-closed-core.svg" alt="Маркеры списков" /></a>
&nbsp;
<a href="CATALOG.md#3-инлайн-плашки-и-алерты-inline-callouts--alerts"><img src="assets/chips/chip-chamfer-spec.svg" alt="Плашки и алерты" /></a>
&nbsp;
<a href="CATALOG.md#2-закрывающие-пластины-master-footers"><img src="assets/chips/chip-pulse-online.svg" alt="Футеры" /></a>
&nbsp;
<a href="TEST_SUITE.md"><img src="assets/chips/chip-pulse-live.svg" alt="Тесты" /></a>

</div>

---

<div id="quick-start--cli-generator"></div>

### 🚀 QUICK START & CLI GENERATOR

Сгенерировать набор под любой проект одной командой (чистый Python, без сторонних библиотек):

```bash
# 1. Сгенерировать флагманский терминал в стиле Cyberpunk
python generator/cli.py --theme cyberpunk --style terminal --title "PROJECT-X"

# 2. Сгенерировать тактический военный HUD в янтарной гамме
python generator/cli.py --theme amber --style tactical --title "SECURITY"

# 3. Сгенерировать минималистичный баннер Tokyo Night
python generator/cli.py --theme tokyo --style minimal --title "AUDIO-SYNTH"
```

#### Структура полной коллекции ассетов (`assets/`):
```
assets/
├── headers/                             # 3 флагманских титульных баннера (850px)
│   ├── header-terminal-cyberpunk.svg    # Радар 360°, scanline и эквалайзер
│   ├── header-tactical-amber.svg        # Тактический прицел и скосы 45°
│   └── header-minimal-tokyo.svg         # Неоновый градиент и эквалайзер
├── footers/                             # 4 закрывающих пластины с навигацией [▲ RETURN TO TOP]
│   ├── footer-terminal-cyberpunk.svg    # Терминальный статус и кластер
│   ├── footer-tactical-amber.svg        # Гриф секретности DEFCON 5
│   ├── footer-minimal-tokyo.svg         # Лицензия и копирайт
│   └── footer-matrix-green.svg          # Консольное завершение сессии
├── callouts/                            # 4 инлайн-плашки для заметок и алертов
│   ├── callout-note-cyan.svg            # Информационный блок [NOTE // 0x01]
│   ├── callout-warning-amber.svg        # Сигнальное предупреждение [WARNING // HAZARD]
│   ├── callout-critical-magenta.svg     # Аварийный блок с пульсирующим маяком [CRITICAL]
│   └── callout-success-green.svg        # Статус развертывания [SUCCESS // OK]
├── bullets/                             # 16 пиксельных маркеров списков (14×14px SVG)
│   ├── bullet-diamond-cyan.svg          # Неоновый ромб Cyberpunk
│   ├── bullet-arrow-pink.svg            # Лазерная стрелка
│   ├── bullet-chevron-amber.svg         # Тактический шеврон ▲
│   ├── bullet-alert-amber.svg           # Сигнал тревоги [!]
│   ├── bullet-square-green.svg          # Пиксельный квадрат ▪
│   ├── bullet-prompt-green.svg          # Терминальный промпт >>
│   └── ... (см. CATALOG.md для полного списка)
├── frames/                              # Верхние и нижние крышки окон (Brackets, Chamfer, Enclosure)
├── splitters/                           # Сплиттеры подмодулей (Terminal, Tactical, Decay)
├── adapters/                            # 45° переходные адаптеры расширения/сужения контура
├── rails/                               # Боковые шины данных 54px и анимированные лестницы 14px
└── chips/                               # 19 голографических чипов (Closed, Chamfer, Decay, Pulse)
```

<br/>

<div align="center">

<!-- MASTER FOOTER (CYBERPUNK WITH RETURN TO TOP) -->
<a href="#top"><img src="assets/footers/footer-terminal-cyberpunk.svg" width="100%" alt="Master Footer" /></a>

<br/><br/>

<a href="https://github.com/Kazinagg"><img src="assets/chips/chip-closed-github.svg" alt="GitHub Profile" /></a>
&nbsp;&nbsp;
<a href="CATALOG.md"><img src="assets/chips/nav-catalog.svg" alt="Catalog" /></a>

<br/><br/>

<sub>PIXEL README KIT v2.2 &bull; CRAFTED FOR TRANSLUCENT DUAL-THEME GITHUB PROFILES &bull; 2026</sub>

</div>
