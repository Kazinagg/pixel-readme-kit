# Полный реестр компонентов ReadmeKit (16 типов блоков)

Документ содержит полный перечень всех 16 компонентов генератора, их директивы разметки, атрибуты и визуальные особенности в канонических темах дизайн-системы.

---

## Архитектурная модель: 3 Уровня Дизайн-Системы

```
1. СТИЛЬ (Style / Visual Paradigm):
   • PIXEL   — Ретро-пиксели, 8-bit, Sci-Fi HUD
   • MODERN  — Чистый вектор, скругления, Silicon Valley / Linear
   • SKETCH  — Рукотворный скетч, Excalidraw, штриховка, скотч

2. ТЕМА (Theme / Geometric Flavor) — 5 канонических тем:
   • cyberpunk     (Стиль: pixel)  — 3D-шрифт, радар 360°, эквалайзер, неоновые акценты
   • tactical      (Стиль: pixel)  — Скосы 45°, chevron hazard stripes, прицел crosshair, лазер
   • minimal       (Стиль: pixel)  — Tokyo Minimal, швейцарская сетка, dot-matrix, чистые контуры
   • modern-clean  (Стиль: modern) — Скругленные карточки, градиенты, чистый вектор
   • rough-doodle  (Стиль: sketch) — Неровный карандашный контур, Excalidraw, штриховка

3. РАСЦВЕТКА (Color Preset / Palette):
   • Для cyberpunk:    cyberpunk, neon-matrix, matrix, synthwave, amber
   • Для tactical:     tactical, amber
   • Для minimal:      minimal, tokyo, clean-mono
   • Для modern-clean: slate-dark, nordic-frost, linear-violet, emerald-clean, modern-slate, clean-mono
   • Для rough-doodle: excali-dark, whiteboard, notebook-graph, blueprint-sketch
```

---

## Сводная таблица компонентов

| № | Тип блока (`block_type`) | Функция генератора | Категория | Поддержка тем (все 5) |
|---|--------------------------|-------------------|-----------|-----------------------|
| 1 | `header` | `generate_header` | Баннеры и заголовки | Cyberpunk / Tactical / Minimal / Modern / Sketch |
| 2 | `window` | `generate_frame` (top/bottom) | Контейнеры контента | Cyberpunk / Tactical / Minimal / Modern / Sketch |
| 3 | `terminal` | `generate_frame` (term_top/bottom)| Контейнеры консоли | Cyberpunk / Tactical / Minimal / Modern / Sketch |
| 4 | `quote` | `generate_callout` (is_quote=True)| Цитаты и заметки | Cyberpunk / Tactical / Minimal / Modern / Sketch |
| 5 | `callout` | `generate_callout` | Предупреждения и плашки| Cyberpunk / Tactical / Minimal / Modern / Sketch |
| 6 | `footer` | `generate_footer` | Подвалы и навигация | Cyberpunk / Tactical / Minimal / Modern / Sketch |
| 7 | `divider` | `generate_divider` | Разделители линий | Cyberpunk / Tactical / Minimal / Modern / Sketch |
| 8 | `splitter` | `generate_splitter` | Разделители секций | Cyberpunk / Tactical / Minimal / Modern / Sketch |
| 9 | `chip` | `generate_chip` | Бейджи и микро-теги | Cyberpunk / Tactical / Minimal / Modern / Sketch |
| 10 | `metrics` | `generate_metrics` | KPI и карточки метрик | Cyberpunk / Tactical / Minimal / Modern / Sketch |
| 11 | `progress` | `generate_progress` | Индикаторы прогресса | Cyberpunk / Tactical / Minimal / Modern / Sketch |
| 12 | `techstack` | `generate_techstack` | Сетка технологий | Cyberpunk / Tactical / Minimal / Modern / Sketch |
| 13 | `timeline` | `generate_timeline` | Хронология и роадмап | Cyberpunk / Tactical / Minimal / Modern / Sketch |
| 14 | `starchart` | `generate_starchart` | График звезд GitHub | Cyberpunk / Tactical / Minimal / Modern / Sketch |
| 15 | `profile` | `generate_profile_card` | Карточка профиля автора| Cyberpunk / Tactical / Minimal / Modern / Sketch |
| 16 | `social` | `generate_social` | OpenGraph / Соц-карточка | Cyberpunk / Tactical / Minimal / Modern / Sketch |

---

## Подробное описание каждого блока

### 1. `header` — Заголовочный баннер (Hero Header)
- **Назначение**: Главный баннер репозитория или страницы.
- **Синтаксис директивы**:
  ```html
  <!-- pixel-kit:header title="PROJECT TITLE" subtitle="System Descriptor" tag="[V4.2]" spec1="PYTHON 3.11+" spec2="100% SVG" spec3="NOMINAL" style="pixel" theme="cyberpunk" preset="cyberpunk" mode="auto" -->
  ```
- **Параметры**:
  - `title` (str, обяз.): Главный заголовок.
  - `subtitle` (str): Подзаголовок / описание.
  - `tag` (str): Угловой тег (по умолчанию `[SYS_INIT]`).
  - `spec1`, `spec2`, `spec3` (str): Три технических параметра в правой колонке.
  - `compact` (bool): Компактный режим высотой 100px вместо 160px.
  - `tag_url`, `close_url` (str): Ссылки кликабельности для тега и кнопки закрытия.
- **Особенности в темах**:
  - `cyberpunk`: 3D пиксельный экструдированный шрифт, круговой радар 360°, полоса аудио-эквалайзера.
  - `tactical`: Скосы 45°, прицельная сетка crosshair, лазерная линия сканирования, трафаретные элементы.
  - `minimal`: Чистая точечная сетка dot-matrix, швейцарская типографика, минималистичные контуры.
  - `modern-clean`: Скругленные векторные углы, мягкие тени и градиенты.
  - `rough-doodle`: Рукописный шрифт, неровный двойной контур, декоративный скотч в углах.

---

### 2. `window` — Карточный контейнер (Window Enclosure)
- **Назначение**: Оборачивает произвольный Markdown-контент в рамку окна.
- **Синтаксис директивы**:
  ```html
  <!-- pixel-kit:window title="CORE // ARCHITECTURE" tag="[SYS_LOG]" style="pixel" theme="tactical" -->
  Ваш markdown контент, таблицы, списки или текст.
  <!-- /pixel-kit:window -->
  ```
- **Параметры**:
  - `title` (str): Заголовок окна.
  - `tag` (str): Статусный тег окна.
  - `tag_url`, `close_url` (str): Интерактивные ссылки.
  - `out_top`, `out_bottom` (str): Пользовательские имена файлов верхней и нижней крышки.

---

### 3. `terminal` — Консольный контейнер (Terminal Shell)
- **Назначение**: Оборачивает терминальные логи, примеры запуска команд и код.
- **Синтаксис директивы**:
  ```html
  <!-- pixel-kit:terminal title="BASH // DEPLOYMENT" tag="[ONLINE]" style="pixel" theme="cyberpunk" -->
  ```bash
  $ python -m generator.server --port 3000
  [OK] SERVER ONLINE
  ```
  <!-- /pixel-kit:terminal -->
  ```
- **Параметры**:
  - `title` (str): Заголовок консоли.
  - `tag` (str): Статусный тег.
  - `state` (str): `open` или `closed`.

---

### 4. `quote` — Архитектурная цитата / Заметка (Specification Notice)
- **Назначение**: Выделение важных архитектурных заметок и цитат.
- **Синтаксис директивы**:
  ```html
  <!-- pixel-kit:quote title="ARCHITECTURAL NOTICE" subtitle="Component standard" badge="NOTE" style="modern" theme="modern-clean" -->
  Текст цитаты или разъяснения архитектуры.
  <!-- /pixel-kit:quote -->
  ```
- **Параметры**:
  - `title` (str): Заголовок плашки.
  - `subtitle` (str): Подпись / контекст.
  - `badge` (str): Тип бейджа (`NOTE`, `TIP`, `IMPORTANT`, `WARNING`, `CAUTION`).
  - `badge_color` (str): Hex цвет бейджа.

---

### 5. `callout` — Автономная плашка уведомления (Alert Banner)
- **Назначение**: Однострочный информационный баннер для привлечения внимания.
- **Синтаксис директивы**:
  ```html
  <!-- pixel-kit:callout title="SECURITY ADVISORY" subtitle="Update dependency versions to latest patch" callout_type="warning" style="pixel" theme="tactical" -->
  ```
- **Параметры**:
  - `title` (str): Заголовок уведомления.
  - `subtitle` (str): Поясняющий текст.
  - `callout_type` (str): Тип (`tip`, `note`, `warning`, `danger`).
  - `badge_color` (str): Пользовательский цвет бейджа.

---

### 6. `footer` — Подвал и статусная полоса (Footer Status Bar)
- **Назначение**: Закрывающий блок README с навигацией «Наверх» и системным статусом.
- **Синтаксис директивы**:
  ```html
  <!-- pixel-kit:footer status="SYSTEM NOMINAL // ALL TESTS GREEN" nav_text="BACK TO TOP [^]" sub_text="BUILD 2026.10" style="pixel" theme="minimal" -->
  ```
- **Параметры**:
  - `status` (str): Статусный текст слева.
  - `nav_text` (str): Текст ссылки возврата наверх справа.
  - `sub_text` (str): Вторичная техническая информация.

---

### 7. `divider` — Декоративный разделитель (Horizontal Rule)
- **Назначение**: Разделение смысловых блоков страницы стилизованной линией.
- **Синтаксис директивы**:
  ```html
  <!-- pixel-kit:divider style="pixel" theme="cyberpunk" -->
  ```
- **Параметры**:
  - `width` (int): Ширина в пикселях (по умолчанию 850).
- **Особенности в темах**:
  - `cyberpunk`: Оптическая шина с неоновыми импульсами в центре.
  - `tactical`: Полосатый Mil-Spec паттерн со скосами 45°.
  - `minimal`: Сверхтонкая швейцарская линия с координатными засечками.
  - `modern-clean`: Мягкий градиентный переход.
  - `rough-doodle`: Живая карандашная волнистая линия.

---

### 8. `splitter` — Разделитель секций с заголовком (Section Splitter)
- **Назначение**: Разделитель с встроенным центрированным заголовком секции.
- **Синтаксис директивы**:
  ```html
  <!-- pixel-kit:splitter label="SECTION // CORE ARCHITECTURE" style="sketch" theme="rough-doodle" -->
  ```
- **Параметры**:
  - `label` (str): Текст названия секции.

---

### 9. `chip` — Компактный бейдж (Micro Status Chip)
- **Назначение**: Статусы, версии, ссылки на лицензию, счетчики звезд.
- **Синтаксис директивы**:
  ```html
  <!-- pixel-kit:chip text="STATUS: 200 OK" type="decay" decay_dir="right" style="pixel" theme="cyberpunk" -->
  ```
- **Параметры**:
  - `text` (str): Текст бейджа.
  - `type` (str): Вариант геометрии (`closed`, `decay`, `badge`).
  - `decay_dir` (str): Направление пиксельного рассеивания (`left`, `right`, `both`).

---

### 10. `metrics` — Панель показателей (KPI Metrics Grid)
- **Назначение**: Отображение 1–4 карточек ключевых метрик проекта.
- **Синтаксис директивы**:
  ```html
  <!-- pixel-kit:metrics items="CORE UPTIME: 99.98% | LATENCY: 12ms | MEMORY: 64MB" style="modern" theme="modern-clean" -->
  ```
  Или контейнерная форма:
  ```html
  <!-- pixel-kit:metrics style="pixel" theme="cyberpunk" -->
  card label="UPTIME" value="99.9%" delta="+0.2%" status="NOMINAL"
  card label="REQUESTS" value="1.4M" delta="+12%" status="PEAK"
  <!-- /pixel-kit:metrics -->
  ```

---

### 11. `progress` — Шкала выполнения (Progress Gauge)
- **Назначение**: Индикатор готовности проекта, покрытия тестами или использования ресурсов.
- **Синтаксис директивы**:
  ```html
  <!-- pixel-kit:progress value="85" label="SPRINT COMPLETION" sub="34 OF 40 TASKS COMPLETED" style="pixel" theme="tactical" -->
  ```
- **Параметры**:
  - `value` (int): Значение от 0 до 100.
  - `label` (str): Название метрики.
  - `sub` (str): Подпись / детализация.

---

### 12. `techstack` — Сетка технологий (Tech Stack Matrix)
- **Назначение**: Презентация стека технологий с векторными пиктограммами.
- **Синтаксис директивы**:
  ```html
  <!-- pixel-kit:techstack items="python,rust,docker,git,typescript" columns="5" style="sketch" theme="rough-doodle" -->
  ```
- **Параметры**:
  - `items` (str или список): Идентификаторы технологий (`python`, `cpp`, `rust`, `docker`, `git`, `javascript`, `typescript`, `react`, `html`, `css` и т.д.).
  - `columns` (int): Количество колонок (от 2 до 8).

---

### 13. `timeline` — Дорожная карта (Roadmap / Timeline)
- **Назначение**: Хронология релизов, этапов разработки или вех проекта.
- **Синтаксис директивы**:
  ```html
  <!-- pixel-kit:timeline style="pixel" theme="cyberpunk" -->
  milestone title="v1.0 GENESIS" date="2024-Q1" status="COMPLETED" desc="Core pixel engine and 8-bit typography"
  milestone title="v2.0 VECTOR" date="2025-Q2" status="ACTIVE" desc="Modern clean vector paradigms"
  milestone title="v3.0 HORIZON" date="2026-Q4" status="PLANNED" desc="Universal 3-tier design system kit"
  <!-- /pixel-kit:timeline -->
  ```

---

### 14. `starchart` — График динамики звезд GitHub (Star Telemetry)
- **Назначение**: Визуализация роста популярности репозитория.
- **Синтаксис директивы**:
  ```html
  <!-- pixel-kit:starchart repo="Kazinagg/pixel-readme-kit" title="TELEMETRY // STAR GROWTH" style="modern" theme="modern-clean" -->
  ```
- **Параметры**:
  - `repo` (str): Репозиторий GitHub в формате `owner/repo`.
  - `title` (str): Заголовок графика.
  - `current` (int): Текущее количество звезд.
  - `delta` (str): Изменение за период.

---

### 15. `profile` — Карточка разработчика (Profile HUD Card)
- **Назначение**: Презентация автора проекта или мейнтейнера.
- **Синтаксис директивы**:
  ```html
  <!-- pixel-kit:profile name="CYBER_ARCHITECT" role="SYSTEM SPECIALIST" bio="Building modular pixel and vector HUD experiences" status="ONLINE" location="TOKYO / NET" badge="CORE_DEV" style="pixel" theme="cyberpunk" -->
  ```
- **Параметры**:
  - `name` (str): Имя или никнейм разработчика.
  - `role` (str): Роль / специализация.
  - `bio` (str): Краткая биография.
  - `status` (str): Статус активности (`ONLINE`, `BUSY`, `AWAY`).
  - `location` (str): Локация.
  - `badge` (str): Квалификационный бейдж.

---

### 16. `social` — Социальная карточка OpenGraph (Social Preview Card)
- **Назначение**: Создание превью-карточки репозитория для соцсетей и GitHub.
- **Синтаксис директивы**:
  ```html
  <!-- pixel-kit:social title="PIXEL README KIT" subtitle="Modular Vector & Pixel HUD Components for GitHub" repo="Kazinagg/pixel-readme-kit" tags="PYTHON,SVG,STUDIO,GITHUB" style="pixel" theme="cyberpunk" -->
  ```
- **Параметры**:
  - `title` (str): Главное название проекта.
  - `subtitle` (str): Слоганы и краткое описание.
  - `repo` (str): Название репозитория.
  - `tags` (str): Список тегов через запятую.
