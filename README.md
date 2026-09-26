# 🧪 ЛАБОРАТОРИЯ ЭКСПЕРИМЕНТОВ // TEST SUITE (ПРИОРИТЕТ 2)

<div id="top"></div>

<div align="center">

<img src="assets/headers/header-tactical-amber.svg" width="100%" alt="Priority 2 Lab Header" />

<br/>

<a href="SHOWCASE.md"><img src="assets/chips/chip-closed-core.svg" align="center" /> <b>[ 🏛️ ПОЛНЫЙ SHOWCASE README ]</b></a>
&nbsp;&nbsp;
<a href="CATALOG.md"><img src="assets/chips/nav-catalog.svg" align="center" /> <b>[ 📚 КАТАЛОГ 100+ АССЕТОВ ]</b></a>

<br/><br/>

<img src="assets/divider-laser-amber.svg" width="100%" alt="Laser Divider" />

</div>

> [!IMPORTANT]
> 🔬 **АКТИВЕН РЕЖИМ ЖИВОЙ КАЛИБРОВКИ НА GITHUB (TEST SUITE)**
> Данный файл временно установлен в качестве основного **`README.md`** репозитория, чтобы в реальном времени оценить поведение санитайзера GitHub, адаптивность таблиц и устранение зазоров.
> Исходный представительский витринный ридми сохранен в **[SHOWCASE.md](SHOWCASE.md)**.

---

## 📑 Оглавление тестов

1. [Исследование ограничений GitHub Markdown & Camo Proxy](#1-исследование-ограничений-github-markdown--camo-proxy)
2. [Тест 1: Устранение вертикальных и боковых зазоров между SVG](#2-тест-1-устранение-вертикальных-и-боковых-зазоров-между-svg)
   - [1А–1Г: Склейка по вертикали (Whitespace vs HTML-комментарии)](#вариант-1в-склеивание-через-html-комментарий----читаемый-код--без-пробелов-в-dom)
   - [1Д: Устранение боковых прозрачных полей (Flush x=1..849 без прокладки)](#тест-1д-устранение-боковых-отступов-в-svg-flush-x1849-без-прокладки)
3. [Тест 2: Одноячеечные таблицы и решение проблемы «границы в границах»](#3-тест-2-одноячеечные-таблицы-и-решение-проблемы-границы-в-границах)
   - [Вариант 2А: Чистая 1-ячеечная таблица с внешними крышками Top & Bottom](#вариант-2а-чистая-1-ячеечная-таблица-с-внешними-крышками-top--bottom)
   - [Вариант 2А-Tactical: Chamfer без переходной прокладки на таблице](#вариант-2а-tactical-тактический-chamfer-без-прокладки-прямо-на-таблице)
   - [Вариант 2Б (Старый): Проблема «границы в границах» при замкнутых рамках](#вариант-2б-старый-проблема-границы-в-границах-при-замкнутых-рамках)
   - [Вариант 2Б-NEW: Пробный стиль `table_minimal` (Интегрированный HUD-планшет)](#вариант-2б-new-пробный-стиль-table_minimal-интегрированный-hud-планшет)
   - [Вариант 2Б-Cyan: Киберпанк-монолит без двойных рамок](#вариант-2б-cyan-киберпанк-монолит-без-двойных-рамок)
   - [Вариант 2В: 1-ячеечная таблица со сплиттером подмодулей](#вариант-2в-1-ячеечная-таблица-со-встроенным-sub-block-сплиттером)
4. [Тест 3: Сравнение 4 архитектур оформления границ](#4-тест-3-сравнение-4-архитектур-оформления-границ)
5. [Резюме и опросник для выбора направления](#5-резюме-и-опросник-для-выбора-направления)

---

<div id="1-исследование-ограничений-github-markdown--camo-proxy"></div>

## 1. 🔍 Исследование ограничений GitHub Markdown & Camo Proxy

Что GitHub **разрешает**, что **переопределяет** и что **жестко вырезает**:

<table width="100%">
  <tr>
    <th width="28%">Подсистема</th>
    <th width="36%">Поведение GitHub</th>
    <th width="36%">Последствие для дизайн-системы</th>
  </tr>
  <tr>
    <td><b>Атрибут <code>style="..."</code></b></td>
    <td>
      <img src="assets/bullets/bullet-alert-amber.svg" align="center" /> <b>100% вырезается</b> санитайзером на любых HTML-тегах (<code>&lt;td&gt;</code>, <code>&lt;div&gt;</code>, <code>&lt;p&gt;</code>).
    </td>
    <td>
      Нельзя задать inline CSS: <code>padding: 0</code>, <code>border: none</code>, <code>margin: 0</code>, <code>line-height: 0</code>. Нужно опираться только на нативный CSS GitHub.
    </td>
  </tr>
  <tr>
    <td><b>Рамки таблиц (<code>table, td</code>)</b></td>
    <td>
      GitHub принудительно накладывает:<br/>
      <code>td { padding: 6px 13px; border: 1px solid var(--borderColor-default); }</code>
    </td>
    <td>
      Нельзя убрать серую рамку ячеек таблицы через HTML. Если используем таблицу — рамка <b>всегда будет видна</b>. Наша стратегия: обыграть эту рамку как фичу!
    </td>
  </tr>
  <tr>
    <td><b>Разрешенные HTML-атрибуты</b></td>
    <td>
      <img src="assets/bullets/bullet-check-cyan.svg" align="center" /> <b>Сохраняются</b>: <code>align</code>, <code>valign</code>, <code>width</code>, <code>height</code>, <code>colspan</code>, <code>rowspan</code>.
    </td>
    <td>
      Выравнивание контента по центру или верху, а также жесткую фиксацию ширины колонок (например, <code>width="54"</code>) делать можно и нужно.
    </td>
  </tr>
  <tr>
    <td><b>Прямой тег <code>&lt;svg&gt;</code></b></td>
    <td>
      <img src="assets/bullets/bullet-alert-amber.svg" align="center" /> <b>100% вырезается</b> из Markdown.
    </td>
    <td>
      Любой SVG должен вставляться через <code>&lt;img src="path.svg" /&gt;</code>.
    </td>
  </tr>
  <tr>
    <td><b>GitHub Camo Proxy</b></td>
    <td>
      Вырезает <code>&lt;script&gt;</code>, <code>&lt;foreignObject&gt;</code>, внешние шрифты.<br/>
      <img src="assets/bullets/bullet-check-cyan.svg" align="center" /> <b>Разрешает</b>: <code>@keyframes</code>, SMIL <code>&lt;animate&gt;</code>, <code>&lt;animateTransform&gt;</code>, <code>@media (prefers-color-scheme)</code>.
    </td>
    <td>
      Все анимации (радар, сканеры, маяки) работают идеально внутри SVG, если XML 100% валиден (амперсанды экранированы как <code>&amp;amp;</code>).
    </td>
  </tr>
</table>

---

<div id="2-тест-1-устранение-вертикальных-отступов-между-svg"></div>

## 2. ⚡ Тест 1: Устранение вертикальных и боковых зазоров между SVG

### Причина вертикальных зазоров:
1. **Markdown абзац (`\n\n`)**: пустая строка создает тег `<p>` с нижним отступом `margin-bottom: 16px`.
2. **DOM Whitespace (`\n`)**: перенос строки между тегами `<img>` браузер рендерит как пробельный символ в строчно-блочном контексте (давая щель 3–5px из-за базовой линии шрифта).

Ниже сравнение способов стыковки верхнего фрейма и переходного адаптера плеч:

### Вариант 1А: Стандартный перенос строки в коде (Есть зазор ~4px)
```html
<img src="assets/frames/frame-top-chamfer-amber.svg" width="100%" />
<img src="assets/adapters/transition-shoulder-top-amber.svg" width="100%" />
```
**Рендеринг 1А**:
<img src="assets/frames/frame-top-chamfer-amber.svg" width="100%" />
<img src="assets/adapters/transition-shoulder-top-amber.svg" width="100%" />

<br/>

### Вариант 1Б: Склеивание в одну строку без пробелов (Минимальный зазор)
```html
<img src="assets/frames/frame-top-chamfer-amber.svg" width="100%"/><img src="assets/adapters/transition-shoulder-top-amber.svg" width="100%"/>
```
**Рендеринг 1Б**:
<img src="assets/frames/frame-top-chamfer-amber.svg" width="100%"/><img src="assets/adapters/transition-shoulder-top-amber.svg" width="100%"/>

<br/>

### Вариант 1В: Склеивание через HTML-комментарий `<!-- -->` (Читаемый код + без пробелов в DOM)
```html
<img src="assets/frames/frame-top-chamfer-amber.svg" width="100%"/><!--
--><img src="assets/adapters/transition-shoulder-top-amber.svg" width="100%"/>
```
**Рендеринг 1В**:
<img src="assets/frames/frame-top-chamfer-amber.svg" width="100%"/><!--
--><img src="assets/adapters/transition-shoulder-top-amber.svg" width="100%"/>

<br/>

---

<div id="тест-1д-устранение-боковых-отступов-в-svg-flush-x1849-без-прокладки"></div>

### 🎯 Тест 1Д: Устранение боковых отступов в SVG (Flush x=1..849 без прокладки)

В ранних версиях фреймы имели прозрачные отступы по бокам (`x=4..6px`), из-за чего требовался переходный адаптер-плечо (`transition-shoulder`), чтобы расширить шину до `x=1` (ширины таблицы).

**Что сделано сейчас**:
1. Все направляющие зубцы и внешний контур шапок и поддонов выведены вплотную к краям: `x=1` слева и `x=849` (`width-1`) справа.
2. Прозрачные боковые поля полностью устранены во всех стилях: `chamfer`, `brackets`, `enclosure`, `minimal`.
3. Теперь фреймы стыкуются с границами таблиц GitHub **напрямую БЕЗ адаптера-прокладки**:

```html
<!-- Тактический Chamfer без прокладки: зубцы садятся прямо на границы таблицы -->
<img src="assets/frames/frame-top-chamfer-amber.svg" width="100%" />
<table width="100%">
  <tr><td>Содержимое таблицы</td></tr>
</table>
<img src="assets/frames/frame-bottom-chamfer-amber.svg" width="100%" />
```

---

<div id="3-тест-2-одноячеечные-таблицы-и-решение-проблемы-границы-в-границах"></div>

## 3. 🧱 Тест 2: Одноячеечные таблицы и решение проблемы «границы в границах»

Тестируем поведение нативной ячейки `<table><tr><td>` как корпуса окна.

### Вариант 2А: Чистая 1-ячеечная таблица с внешними крышками Top & Bottom
- Верхняя крышка стыкуется сверху.
- Нативная рамка ячейки GitHub (`border: 1px solid var(--borderColor-default)`) образует аккуратный бокс контента.
- Нижняя крышка замыкает бокс снизу.

<img src="assets/frames/frame-top-enclosure-cyan.svg" width="100%" />

<table width="100%">
<tr>
<td>

#### 🧬 МОДУЛЬ: ОДНОЯЧЕЕЧНЫЙ ТЕРМИНАЛ (ВАРИАНТ 2А)
- <img src="assets/bullets/bullet-check-cyan.svg" align="center" /> **100% нативная адаптивность**: на смартфонах таблица сжимается идеально, текст автоматически переносится.
- <img src="assets/bullets/bullet-diamond-cyan.svg" align="center" /> **Нет боковых рельсов**: нулевой риск сплющивания картинок, ширина всегда 100%.
- <img src="assets/bullets/bullet-arrow-pink.svg" align="center" /> **Встроенный padding**: GitHub автоматически дает `padding: 6px 13px`.

```bash
# Пример терминальной команды внутри одиночной ячейки
python generator/cli.py --theme cyberpunk --style terminal
```

</td>
</tr>
</table>

<img src="assets/frames/frame-bottom-enclosure-cyan.svg" width="100%" />

<br/>

### Вариант 2А-Tactical: Тактический Chamfer БЕЗ прокладки прямо на таблице
Здесь тактический фрейм садится прямо на таблицу — обратите внимание на левый и правый угол: направляющие зубцы теперь идеально совпадают с шириной таблицы:

<img src="assets/frames/frame-top-chamfer-amber.svg" width="100%" />

<table width="100%">
<tr>
<td>

#### ⚡ ТАКТИЧЕСКИЙ ОДНОЯЧЕЕЧНЫЙ БОКС (БЕЗ ПРОКЛАДКИ)
- <img src="assets/bullets/bullet-chevron-amber.svg" align="center" /> Боковые поля в SVG полностью отсутствуют.
- <img src="assets/bullets/bullet-plus-amber.svg" align="center" /> Концы зубцов фрейма (`x=1`, `x=849`) точно позиционируются над гранями ячейки таблицы.
- <img src="assets/bullets/bullet-alert-amber.svg" align="center" /> Никаких промежуточных адаптеров не требуется.

</td>
</tr>
</table>

<img src="assets/frames/frame-bottom-chamfer-amber.svg" width="100%" />

<br/>

### Вариант 2Б (Старый): Проблема «границы в границах» при замкнутых рамках
В этом варианте шапка со своей замкнутой прямоугольной рамкой была помещена внутрь ячейки `<td>`.
В результате возник визуальный артефакт: рамка ячейки таблицы обрамляет рамку фрейма с отступом 13px (двойные границы):

<table width="100%">
<tr>
<td align="center">
<img src="assets/frames/frame-top-brackets-green.svg" width="100%" />
</td>
</tr>
<tr>
<td>

#### ⚠️ ДЕМОНСТРАЦИЯ ДВОЙНЫХ ГРАНИЦ (OLD VARIANT 2B)
Посмотрите на серую рамку вокруг шапки:
1. Внешняя серая линия — рамка таблицы GitHub.
2. Внутренняя рамка — нарисована внутри SVG.
3. Между ними — неубираемый padding 13px.

</td>
</tr>
<tr>
<td align="center">
<img src="assets/frames/frame-bottom-brackets-green.svg" width="100%" />
</td>
</tr>
</table>

<br/>

### Вариант 2Б-NEW: Пробный стиль `table_minimal` (Интегрированный HUD-планшет)
🎯 **Решение проблемы «границы в границах»**:
1. В SVG **полностью убран внешний замкнутый прямоугольник**.
2. В углах расположены технологические маркеры `┌` и `┐`, которые обнимают внутренние углы ячейки.
3. **Нативная рамка таблицы GitHub становится внешним корпусом окна**.
4. Внутренняя разделительная линия строк таблицы GitHub работает как технологический шов под приборной панелью.

<table width="100%">
<tr>
<td align="center">
<img src="assets/frames/frame-top-table-minimal.svg" width="100%" />
</td>
</tr>
<tr>
<td>

#### 🟢 НОВЫЙ ИНТЕГРИРОВАННЫЙ СТИЛЬ: ZERO DOUBLE BORDERS
- <img src="assets/bullets/bullet-square-green.svg" align="center" /> **Внешний корпус**: нативная 1px серая рамка таблицы GitHub (в темной теме `#30363d`, в светлой `#d0d7de`).
- <img src="assets/bullets/bullet-prompt-green.svg" align="center" /> **Приборная панель (Строка 1)**: встроенная в строку шапка с LED-индикатором, статусом `[TABLE_HUD]` и оконными кнопками `_ □ ×`.
- <img src="assets/bullets/bullet-check-cyan.svg" align="center" /> **Шов**: 1px разделитель между `<tr>` служит линией отсечки шапки от рабочего поля.
- <img src="assets/bullets/bullet-dither-light-green.svg" align="center" /> **Нижний поддон (Строка 3)**: статусная планка буфера телеметрии с угловыми зацепами `└` и `┘`.

</td>
</tr>
<tr>
<td align="center">
<img src="assets/frames/frame-bottom-table-minimal.svg" width="100%" />
</td>
</tr>
</table>

<br/>

### Вариант 2Б-Cyan: Киберпанк-монолит без двойных рамок

<table width="100%">
<tr>
<td align="center">
<img src="assets/frames/frame-top-table-minimal-cyan.svg" width="100%" />
</td>
</tr>
<tr>
<td>

#### 🔷 КИБЕРПАНК МОНОЛИТ // CYBER_TABLE
- <img src="assets/bullets/bullet-diamond-cyan.svg" align="center" /> Идеальная чистота линий: ноль дублирования границ.
- <img src="assets/bullets/bullet-marker-cyan.svg" align="center" /> Автоматически реагирует на светлую/темную тему GitHub.
- <img src="assets/bullets/bullet-arrow-pink.svg" align="center" /> Содержимое поддерживает списки, таблицы, формулы и бейджи без конфликтов.

```json
{
  "module": "CYBER_MONOLITH",
  "borders": "NATIVE_TABLE_LEVERAGED",
  "double_borders": false,
  "status": "OPTIMAL"
}
```

</td>
</tr>
<tr>
<td align="center">
<img src="assets/frames/frame-bottom-table-minimal-cyan.svg" width="100%" />
</td>
</tr>
</table>

<br/>

### Вариант 2В: 1-ячеечная таблица со встроенным Sub-Block сплиттером
Внутри одной ячейки размещен живой текст, расщепленный посередине T-образным сплиттером:

<table width="100%">
<tr>
<td>

#### 📁 СЕКЦИЯ 01 // ПЕРВИЧНЫЙ ПАКЕТ
Живой текст вводной части модуля. Поддерживает списки, формулы и бейджи:
- <img src="assets/chips/chip-closed-core.svg" align="center" /> Ядро дизайн-системы

<img src="assets/splitters/splitter-terminal-cyberpunk.svg" width="100%" />

#### ⚙️ СЕКЦИЯ 02 // ВТОРИЧНЫЙ ПАКЕТ
Второй подмодуль, продолжающийся внутри той же самой рамки окна:
- <img src="assets/chips/chip-decay-right-done.svg" align="center" /> Валидация XML пройдена

</td>
</tr>
</table>

---

<div id="4-тест-3-сравнение-4-архитектур-оформления-границ"></div>

## 4. 📐 Тест 3: Сравнение 4 архитектур оформления границ

Сравним 4 кардинально разных подхода к интеграции блоков в Markdown:

### Архитектура I: Нативная цитата `<blockquote>` (Zero Table / Pure Markdown)
> **Идея**: Полный отказ от таблиц. Используется нативная левая акцентная линия GitHub (`border-left: 0.25em solid`). Внутрь помещаются рамки, сплиттеры и чипы.

> <img src="assets/callouts/callout-note-cyan.svg" width="100%" />
>
> #### 🧬 АРХИТЕКТУРА I: НА ТАКТОВОЙ ЦИТАТЕ GITHUB
> **Преимущества**:
> - <img src="assets/bullets/bullet-check-cyan.svg" align="center" /> **Абсолютная адаптивность**: на смартфонах цитаты выглядят превосходно.
> - <img src="assets/bullets/bullet-diamond-cyan.svg" align="center" /> **Нулевой риск проблем с таблицами**: нет padding-ограничений GitHub.
> - <img src="assets/bullets/bullet-arrow-pink.svg" align="center" /> **Внутреннее расщепление**:
>
> <img src="assets/splitters/splitter-decay-tokyo.svg" width="100%" />
>
> Подмодуль продолжается внутри цитаты с сохранением цветной вертикальной шины слева.

<br/>

### Архитектура II: Таблица из одной ячейки (Single-Cell Box)
> **Идея**: Вся область обрамляется тонким 1px контуром нативной ячейки GitHub.

<img src="assets/callouts/callout-warning-amber.svg" width="100%" />

<table width="100%">
<tr>
<td>

#### 🟡 АРХИТЕКТУРА II: ОДНОЯЧЕЕЧНЫЙ БОКС
- Создает полноценную замкнутую рамку вокруг текста.
- Цвет рамки автоматически адаптируется под тему пользователя (`#30363d` в Dark, `#d0d7de` в Light).
- Не требует боковых картинок-рельсов.

</td>
</tr>
</table>

<br/>

### Архитектура III: 3-Колоночная таблица с 54px Gutter Rails (Фирменный стиль v2.2)
> **Идея**: Максимальный ретро-киберпанк. Настоящие пиксельные шины данных с шахматным дизерингом слева и справа.

<img src="assets/frames/frame-top-enclosure-cyan.svg" width="100%" />

<table border="0" cellpadding="0" cellspacing="0" width="100%">
  <tr>
    <td width="54" align="center" valign="top" style="padding: 0;">
      <img src="assets/rails/gutter-left-cyberpunk.svg" width="54" height="180" />
    </td>
    <td style="padding: 10px 24px;">

#### 🔵 АРХИТЕКТУРА III: 54PX ШИНЫ ДАННЫХ
Самый монументальный и детализированный вид. Ширина ячеек зафиксирована на `54px`, предотвращая сплющивание графики.

    </td>
    <td width="54" align="center" valign="top" style="padding: 0;">
      <img src="assets/rails/gutter-right-cyberpunk.svg" width="54" height="180" />
    </td>
  </tr>
</table>

<img src="assets/frames/frame-bottom-enclosure-cyan.svg" width="100%" />

<br/>

### Архитектура IV: Сворачиваемый HUD-терминал (`<details>` / `<summary>`)
> **Идея**: Интерактивное сворачиваемое окно. Шапка служит кнопкой сворачивания/разворачивания.

<details open>
<summary><b>[ ▶ НАЖМИТЕ ДЛЯ СВОРАЧИВАНИЯ / РАЗВОРАЧИВАНИЯ ТЕРМИНАЛА ]</b></summary>

<br/>

<img src="assets/callouts/callout-critical-magenta.svg" width="100%" />

<table width="100%">
<tr>
<td>

#### 🔴 АРХИТЕКТУРА IV: ИНТЕРАКТИВНЫЙ РАСКРЫВАЮЩИЙСЯ ТЕРМИНАЛ
Пользователь может сворачивать вспомогательные логические блоки (логи, тесты, подробные таблицы), оставляя README компактным.
- Нативная поддержка в браузере без JavaScript.
- Полная совместимость с GitHub Markdown.

</td>
</tr>
</table>

<img src="assets/footers/footer-matrix-green.svg" width="100%" />

</details>

---

<div id="5-резюме-и-опросник-для-выбора-направления"></div>

## 5. 🎯 Резюме и опросник для выбора направления

| Вариант | Плюсы | Минусы | Для чего подходит лучше всего |
| :--- | :--- | :--- | :--- |
| **1. Таблица из 1 ячейки (Single Cell)** | 100% адаптивность, нативный чистый бордер GitHub, нет риска сплющивания картинок, лаконичный код. | Рамка стандартная серая (нельзя покрасить в неон средствами HTML). | Основные блоки документации, API-справка, код. |
| **2. Таблица-Монолит `table_minimal`** | Ноль двойных границ, встроенный HUD-планшет в строке таблицы, выглядит как единый цельный прибор. | Внутри ячейки действует неубираемый padding 13px от GitHub. | Интерактивные консоли, структурированные разделы. |
| **3. Внешние крышки (Вариант 2А)** | Крышки накрывают таблицу сверху и снизу, направляющие зубцы садятся прямо на углы. | Верхняя и нижняя планки отделены от таблицы на 1–2px. | Карточки продуктов, модули с акцентными шапками. |
| **4. Цитата `<blockquote>`** | Идеальная поддержка на мобилках, стильная акцентная линия слева, нулевой код. | Нет верхней и нижней рамки (только левая шина). | Примечания, важные сообщения, краткие инструкции. |
| **5. 3-колоночные 54px Rails** | Максимальный визуальный WOW-эффект, полноценный HUD-интерфейс, детализированный дизеринг. | Требует строгой разметки ширины шин `width="54"`. | Главные обзорные разделы, титульные окна. |

---

<div align="center">

<a href="#top"><img src="assets/footers/footer-terminal-cyberpunk.svg" width="100%" alt="Return to top" /></a>

<br/><br/>

<a href="SHOWCASE.md"><img src="assets/chips/chip-closed-core.svg" align="center" /> <b>[ ⬅️ ПЕРЕЙТИ В ПОЛНЫЙ SHOWCASE README ]</b></a>

<br/><br/>

<sub>PIXEL README KIT v2.2 &bull; RESEARCH LAB &bull; 2026</sub>

</div>
