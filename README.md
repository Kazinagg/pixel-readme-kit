<div align="center">

<!-- MAIN 3D CYBERPUNK TERMINAL HEADER (Radar 360° + CRT Scanline + Equalizer) -->
<img src="assets/headers/header-terminal-cyberpunk.svg" width="100%" alt="PIXEL-KIT TRANSLUCENT HUD" />

<br/>

<!-- NAVIGATION PILLS -->
<a href="#suite-1-cyberpunk-terminal-workstation"><img src="assets/chips/nav-brackets.svg" alt="Suite 1: Terminal" /></a>
<a href="#suite-2-tactical-military-hud"><img src="assets/chips/nav-enclosure.svg" alt="Suite 2: Tactical" /></a>
<a href="#suite-3-cyber-gutter-terminal"><img src="assets/chips/nav-chips.svg" alt="Suite 3: Gutter" /></a>
<a href="#header-styles-gallery"><img src="assets/chips/nav-arch.svg" alt="Header Gallery" /></a>
<a href="#quick-start--cli-generator"><img src="assets/chips/nav-guide.svg" alt="Guide" /></a>

<br/><br/>

<!-- ANIMATED PCB DIVIDER (Traveling Data Packet) -->
<img src="assets/divider-pcb-cyan.svg" width="100%" alt="PCB Divider" />

</div>

## 📌 OVERVIEW // О ПРОЕКТЕ

**Pixel Readme Kit v2.2** — модульная дизайн-система в эстетике ретро-киберпанка, тактических HUD-терминалов и полупрозрачного стекла.

Создана для оформления GitHub профилей и репозиториев без недостатков статических картинок:
- 🧊 **True Alpha Blending (Контрастность на темной и светлой темах)**: `rgba(10, 14, 23, 0.82)` гарантирует глубокую темную подложку как на черном фоне GitHub Dark (`#0d1117`), так и на белом фоне GitHub Light (`#ffffff`). Текст и границы не выгорают и сохраняют контрастность выше 7:1.
- 📋 **100% Живой Markdown-текст**: Документация, команды консоли, списки и LaTeX-формулы остаются копируемыми и индексируемыми.
- 📐 **3 Полноценных тематических сюиты (3 Стиля оформления)**:
  1. *Suite 1: Cyberpunk Terminal* — классический открытый терминал с T-образными сплиттерами блоков.
  2. *Suite 2: Tactical Military HUD* — боевой интерфейс 45° с переходными адаптерами плеч (Transitional Shoulders) и шевронными сплиттерами.
  3. *Suite 3: Cyber Gutter Terminal* — шины данных с шахматным дизерингом 54px и многоколоночным расщеплением текста.
- 💫 **Живые SVG CSS-анимации**: Вращающийся луч радара 360°, бегущая CRT-строка сканирования, прицельный лазер, бегущий пакет данных по плате, каскадный импульс лестниц и пульсирующие светодиоды.
- 💎 **5 типов голографических чипов**: Closed, 45° Chamfer, Decay-Right (растворение в текст), Decay-Left (выход из текста), Pulse (с живым маяком).

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
> - <img src="assets/chips/chip-pulse-online.svg" align="center" /> ➔ **Ядро системы активно** (живой мерцающий маяк)
> - <img src="assets/chips/chip-chamfer-matrix.svg" align="center" /> ➔ Модуль RLE-сжатия 3D пиксельных шрифтов

<!-- SUB-BLOCK SPLITTER (TERMINAL T-JUNCTION) -->
<img src="assets/splitters/splitter-terminal-cyberpunk.svg" width="100%" alt="Terminal Splitter" />

> #### ⚡ MODULE 02 // TELEMETRY & HARDWARE BUS
>
> Второй расщепленный блок с параметрами окружения:
> - <img src="assets/chips/chip-closed-core.svg" align="center" /> ➔ Архитектура True Alpha Blending (`rgba(10, 14, 23, 0.82)`)
> - <img src="assets/chips/chip-closed-cli.svg" align="center" /> ➔ Чистый Python 3.8+ без внешних библиотек

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
      <img src="assets/rails/rail-left-ladder-amber.svg" height="210" width="14" />
    </td>
    <td style="padding: 10px 24px;">

#### 🛰️ TACTICAL TELEMETRY STREAM
Внутри замкнутого бокса данные защищены боковыми шинами. Таблица статуса подсистем:

| Подсистема | Режим | Анимация | Статус |
| :--- | :--- | :--- | :--- |
| `Radar 360°` | Full Sweep | `<animateTransform>` | <img src="assets/chips/chip-pulse-live.svg" align="center" /> |
| `Target Laser` | 4s Traverse | `@keyframes targetScan` | <img src="assets/chips/chip-chamfer-spec.svg" align="center" /> |
| `Ladder Bus` | Cascade Glow | `@keyframes rungGlow` | `ACTIVE` |

    </td>
    <td width="40" valign="top" align="center" style="line-height: 0; padding: 0;">
      <img src="assets/rails/rail-right-ladder-amber.svg" height="210" width="14" />
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
      <img src="assets/chips/chip-decay-right-src.svg" align="center" /> ➔ <code>generator/builder.py</code><br/>
      <img src="assets/chips/chip-decay-right-tag.svg" align="center" /> ➔ Релиз v2.2 Dual-Theme<br/>
      <img src="assets/chips/chip-decay-right-done.svg" align="center" /> ➔ 100% валидация XML
    </td>
    <td width="50%" valign="top">
      <b>[ 🛠️ COLUMN B: COMMANDS ]</b><br/><br/>
      <code>python cli.py --theme cyberpunk</code><br/>
      <code>python cli.py --theme amber</code><br/>
      <code>python cli.py --theme tokyo</code>
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
├── headers/
│   ├── header-terminal-cyberpunk.svg    # Флагманский 3D терминал с радаром 360° и сканером
│   ├── header-tactical-amber.svg        # Тактический 45° HUD с прицелом
│   └── header-minimal-tokyo.svg         # Минималистичный баннер с эквалайзером
├── frames/
│   ├── frame-top-brackets-green.svg     # Открытые скобы с направляющими зубцами вниз (Mode A)
│   ├── frame-bottom-brackets-green.svg  # Скобы с подхватывающими зубцами вверх
│   ├── frame-top-chamfer-amber.svg      # Тактический скос 45° (Mode B)
│   ├── frame-bottom-chamfer-amber.svg   # Тактический поддон 45°
│   ├── frame-top-enclosure-cyan.svg     # Замкнутый контур под шины данных (Mode C)
│   └── frame-bottom-enclosure-cyan.svg  # Замыкающая нижняя планка
├── splitters/
│   ├── splitter-terminal-cyberpunk.svg  # Т-образный сплиттер подмодулей (├── [01] ──┤)
│   ├── splitter-tactical-amber.svg      # Шевронный тактический сплиттер (▲═══ [02] ═══▲)
│   └── splitter-decay-tokyo.svg         # Растворяющийся пиксельный сплиттер (░▒▓ [03] ▓▒░)
├── adapters/
│   ├── transition-shoulder-top-amber.svg    # Верхнее 45° плечо, расширяющееся под таблицу
│   └── transition-shoulder-bottom-amber.svg # Нижнее 45° плечо, замыкающее таблицу
├── rails/
│   ├── gutter-left-cyberpunk.svg        # Дизеринг 54px шашкой и раскиданные пиксели (левый)
│   ├── gutter-right-cyberpunk.svg       # Дизеринг 54px шашкой и раскиданные пиксели (правый)
│   ├── rail-left-ladder-amber.svg       # Анимированная лестница данных
│   ├── rail-left-laser-cyan.svg         # Тонкая неоновая направляющая 1px
│   └── rail-left-matrix-green.svg       # Матричный поток точек
└── chips/
    ├── chip-closed-*.svg                # Замкнутые капсулы
    ├── chip-chamfer-*.svg               # 45° тактические бейджи
    ├── chip-decay-right-*.svg           # Растворение пикселей вправо
    ├── chip-decay-left-*.svg            # Выход пикселей влево
    └── chip-pulse-*.svg                 # Чипы с живым мерцающим маяком
```

<br/>

<div align="center">

<a href="https://github.com/Kazinagg"><img src="assets/chips/chip-closed-github.svg" alt="GitHub Profile" /></a>

<br/><br/>

<sub>PIXEL README KIT v2.2 &bull; CRAFTED FOR TRANSLUCENT DUAL-THEME GITHUB PROFILES &bull; 2026</sub>

</div>
