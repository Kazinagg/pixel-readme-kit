# 🌓 Лаборатория тестирования тем GitHub и прозрачности SVG

> [!IMPORTANT]
> **Временный тестовый стенд**: Главный `README.md` временно заменен на страницу тестов для проверки работы на главной странице репозитория.
> [📄 Посмотреть оригинальный README репозитория можно здесь](README.original.md).

---

В этом документе представлены **4 практических теста** адаптации SVG-графики под светлую и тёмную темы GitHub, а также тест шапки с **полностью прозрачным фоном**.

> [!TIP]
> **Как тестировать прямо сейчас на GitHub**:
> 1. Откройте эту страницу на главной репозитория [github.com/Kazinagg/pixel-readme-kit](https://github.com/Kazinagg/pixel-readme-kit).
> 2. Кликните на ваш аватар в правом верхнем углу GitHub ➔ **Theme** ➔ выберите **Dark default** или **Light default**.
> 3. Либо переключите тему в настройках вашей ОС (Windows / macOS) для проверки системных медиа-запросов.

---

## 🧪 Тест 1. Официальный синтаксис GitHub (`#gh-dark-mode-only` и `#gh-light-mode-only`)

GitHub скрывает и показывает изображения по селектору `[src$="#gh-dark-mode-only"]` и `[src$="#gh-light-mode-only"]` на основе темы аккаунта GitHub.

### Вариант 1А: С относительными путями (Официальный синтаксис):

![Cyberpunk Dark Header](assets/theme-tests/header-gh-dark.svg#gh-dark-mode-only)
![Cyberpunk Light Header](assets/theme-tests/header-gh-light.svg#gh-light-mode-only)

```markdown
![Cyberpunk Dark Header](assets/theme-tests/header-gh-dark.svg#gh-dark-mode-only)
![Cyberpunk Light Header](assets/theme-tests/header-gh-light.svg#gh-light-mode-only)
```

### Вариант 1Б: С прямыми Raw URL (Если GitHub не сохраняет хэш при локальном рендере):

![Cyberpunk Dark Header Raw](https://raw.githubusercontent.com/Kazinagg/pixel-readme-kit/main/assets/theme-tests/header-gh-dark.svg#gh-dark-mode-only)
![Cyberpunk Light Header Raw](https://raw.githubusercontent.com/Kazinagg/pixel-readme-kit/main/assets/theme-tests/header-gh-light.svg#gh-light-mode-only)

```markdown
![Cyberpunk Dark Header Raw](https://raw.githubusercontent.com/Kazinagg/pixel-readme-kit/main/assets/theme-tests/header-gh-dark.svg#gh-dark-mode-only)
![Cyberpunk Light Header Raw](https://raw.githubusercontent.com/Kazinagg/pixel-readme-kit/main/assets/theme-tests/header-gh-light.svg#gh-light-mode-only)
```

---

## 🧪 Тест 2. HTML5-тег `<picture>` с `prefers-color-scheme`

Реагирует на системную тему операционной системы / браузера.

### Вариант 2А: Тег `<picture>` с прямыми Raw URL (Рекомендуемый для GitHub):
*(GitHub не всегда перезаписывает относительные пути внутри атрибута `srcset` тега `<source>`, поэтому прямые Raw URL гарантируют загрузку)*:

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Kazinagg/pixel-readme-kit/main/assets/theme-tests/header-pic-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Kazinagg/pixel-readme-kit/main/assets/theme-tests/header-pic-light.svg">
  <img alt="Adaptive Header Picture Raw" src="https://raw.githubusercontent.com/Kazinagg/pixel-readme-kit/main/assets/theme-tests/header-pic-dark.svg" width="100%">
</picture>

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Kazinagg/pixel-readme-kit/main/assets/theme-tests/header-pic-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Kazinagg/pixel-readme-kit/main/assets/theme-tests/header-pic-light.svg">
  <img alt="Adaptive Header Picture" src="https://raw.githubusercontent.com/Kazinagg/pixel-readme-kit/main/assets/theme-tests/header-pic-dark.svg" width="100%">
</picture>
```

### Вариант 2Б: Тег `<picture>` с относительными путями:

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/theme-tests/header-pic-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/theme-tests/header-pic-light.svg">
  <img alt="Adaptive Header Picture Relative" src="assets/theme-tests/header-pic-dark.svg" width="100%">
</picture>

---

## 🧪 Тест 3. Один SVG с адаптивным CSS `@media (prefers-color-scheme: dark)` ✅

> [!NOTE]
> Этот способ подтверждён как работающий на GitHub! Браузер загружает **всего 1 файл** и перекрашивает его на лету.

### Живой результат на GitHub:

![Adaptive Single SVG](assets/theme-tests/header-adaptive-internal.svg)

### Исходный Markdown код:
```markdown
![Adaptive Single SVG](assets/theme-tests/header-adaptive-internal.svg)
```

---

## 🧪 Тест 4. Шапка с полностью прозрачным фоном (Zero Fill / 100% Alpha)

В стандартном генераторе `pixel-readme-kit` используется подложка `rgba(10, 14, 23, 0.85)` (**True Alpha Blending**). В этом тесте подложка полностью удалена (`fill="none"`, `rect` убран).

### Живой результат на GitHub:

![Cyberpunk Transparent Header](assets/theme-tests/header-transparent.svg)

### Исходный Markdown код:
```markdown
![Cyberpunk Transparent Header](assets/theme-tests/header-transparent.svg)
```

---

## 📊 Сводное сравнение методов

| Метод | Как переключается | Кол-во файлов | Зависимость | Совместимость с Camo Proxy |
| :--- | :--- | :--- | :--- | :--- |
| **1. Хэши `#gh-*-mode-only`** | Автоматически GitHub | 2 файла | Тема в настройках GitHub | 100% отлично |
| **2. Тег `<picture>`** | Браузером по медиа-запросу | 2 файла | Системная тема ОС | Требует raw URL для `<source>` |
| **3. Внутренний `@media`** | Браузером по медиа-запросу | **1 файл** | Системная тема ОС | 100% отлично (работает из коробки) |
| **4. Полная прозрачность** | Не переключается (фон GitHub) | **1 файл** | Нет (прозрачный alpha) | 100% отлично |
| **5. Фирменный True Alpha** | Не требует переключения | **1 файл** | Универсальный контраст > 7:1 | 100% отлично |

---

[📄 Посмотреть оригинальный README репозитория можно здесь](README.original.md)
