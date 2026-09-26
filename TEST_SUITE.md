# 🧪 ЛАБОРАТОРИЯ ЭКСПЕРИМЕНТОВ // TEST SUITE (ПРИОРИТЕТ 2)

<div id="top"></div>

<div align="center">

<img src="assets/headers/header-tactical-amber.svg" width="100%" alt="Priority 2 Lab Header" />

<br/>

<a href="README.md"><img src="assets/chips/chip-closed-core.svg" align="center" /> <b>[ ⬅️ ГЛАВНЫЙ README ]</b></a>
&nbsp;&nbsp;
<a href="CATALOG.md"><img src="assets/chips/nav-catalog.svg" align="center" /> <b>[ 📚 КАТАЛОГ АССЕТОВ ]</b></a>

<br/><br/>

<img src="assets/divider-laser-amber.svg" width="100%" alt="Laser Divider" />

</div>

> **ЦЕЛЬ ЭКСПЕРИМЕНТА**: Исследовать точные ограничения разметки GitHub Markdown / Camo Proxy, протестировать устранение вертикальных зазоров между SVG и оценить 4 архитектурных варианта оформления границ окна (включая таблицу из одной ячейки) для максимальной интеграции блоков в живой текст.

---

## 📑 Оглавление тестов

1. [Исследование ограничений GitHub Markdown & Camo Proxy](#1-исследование-ограничений-github-markdown--camo-proxy)
2. [Тест 1: Устранение вертикальных отступов между SVG](#2-тест-1-устранение-вертикальных-отступов-между-svg)
3. [Тест 2: Таблица из одной ячейки как границы окна](#3-тест-2-таблица-из-одной-ячейки-как-границы-окна)
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
      Нельзя убрать серую рамку ячеек таблицы через HTML. Если используем таблицу — рамка <b>всегда будет видна</b>. Наша стратегия: использовать эту рамку как фичу!
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

## 2. ⚡ Тест 1: Устранение вертикальных отступов между SVG

Почему между SVG возникает зазор?
1. **Markdown абзац (`\n\n`)**: пустая строка создает тег `<p>` с нижним отступом `margin-bottom: 16px`.
2. **DOM Whitespace (`\n`)**: перенос строки между тегами `<img>` браузер рендерит как пробельный символ в строчно-блочном контексте (давая щель 3–5px из-за базовой линии шрифта).

Ниже 4 способа стыковки верхнего фрейма и переходного адаптера плеч:

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

### Вариант 1Г: Внутри `<div align="center">` без переносов
```html
<div align="center"><img src="assets/frames/frame-top-chamfer-amber.svg" width="100%"/><img src="assets/adapters/transition-shoulder-top-amber.svg" width="100%"/></div>
```
**Рендеринг 1Г**:
<div align="center"><img src="assets/frames/frame-top-chamfer-amber.svg" width="100%"/><img src="assets/adapters/transition-shoulder-top-amber.svg" width="100%"/></div>

---

<div id="3-тест-2-таблица-из-одной-ячейки-как-границы-окна"></div>

## 3. 🧱 Тест 2: Таблица из одной ячейки как границы окна

Ваша идея: *можно ли сделать таблицу из одной ячейки `<table><tr><td>` и использовать ее нативную рамку как границы окна?*

Протестируем 3 вариации:

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

### Вариант 2Б: Таблица-Монолит (Шапка, Контент и Футер в строках единой таблицы)
Все элементы помещены в одну таблицу из 3 строк (`<tr>`):
1. Строка 1: Верхняя планка
2. Строка 2: Markdown контент
3. Строка 3: Нижняя планка

<table width="100%">
<tr>
<td align="center">
<img src="assets/frames/frame-top-brackets-green.svg" width="100%" />
</td>
</tr>
<tr>
<td>

#### ⚡ СТРОКА 2 // ЖИВОЙ КОНТЕНТ МОНОЛИТА
Обратите внимание: между строками таблицы GitHub автоматически рисует тонкие 1px разделительные линии.
- Линия между шапкой и текстом выглядит как встроенный технологический шов.
- Линия перед поддоном завершает логический блок.

- <img src="assets/bullets/bullet-square-green.svg" align="center" /> Потоковая телеметрия активна
- <img src="assets/bullets/bullet-prompt-green.svg" align="center" /> Буфер памяти синхронизирован

</td>
</tr>
<tr>
<td align="center">
<img src="assets/frames/frame-bottom-brackets-green.svg" width="100%" />
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
| **2. Цитата `<blockquote>`** | Идеальная поддержка на мобилках, стильная акцентная линия слева, нулевой код. | Нет верхней и нижней рамки (только левая шина). | Примечания, важные сообщения, краткие инструкции. |
| **3. 3-колоночные 54px Rails** | Максимальный визуальный WOW-эффект, полноценный HUD-интерфейс, детализированный дизеринг. | Требует строгой разметки ширины шин `width="54"`. | Главные обзорные разделы, титульные окна. |
| **4. `<details>` терминал** | Интерактивное сворачивание, компактность страницы. | Требует клика для просмотра, стрелка браузера слева. | Детальные логи, спецификации, длинные таблицы. |

---

<div align="center">

<a href="#top"><img src="assets/footers/footer-terminal-cyberpunk.svg" width="100%" alt="Return to top" /></a>

<br/><br/>

<a href="README.md"><img src="assets/chips/chip-closed-core.svg" align="center" /> <b>[ ⬅️ ВЕРНУТЬСЯ В ГЛАВНЫЙ README ]</b></a>

<br/><br/>

<sub>PIXEL README KIT v2.2 &bull; RESEARCH LAB &bull; 2026</sub>

</div>
