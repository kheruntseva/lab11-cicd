# Лабораторная работа 11 — CI/CD (GitHub Actions)

Простая веб-форма обратной связи с автоматизированными UI-тестами (Selenium) и пайплайном CI/CD.

## Структура проекта

```
lab11/
├── index.html              # Веб-страница с формой
├── css/style.css
├── js/app.js
├── tests/test_ui.py        # 5 автоматизированных UI-тестов
├── requirements.txt
├── .github/workflows/ci.yml
└── README.md
```

## Ветки Git

| Ветка | Назначение |
|-------|------------|
| `main` | Продакшен, деплой на GitHub Pages |
| `dev`  | Основная ветка разработки |
| `fix`  | Ветка для задачи (фича / исправление) |

**Не коммитьте напрямую в `main`** — только через Pull Request.

## Локальный запуск

```bash
pip install -r requirements.txt
python -m http.server 8000
# Откройте http://127.0.0.1:8000/index.html

python -m pytest tests/ -v
```

Требуется установленный Google Chrome.

## Настройка GitHub

### 1. Создайте репозиторий на GitHub

1. [github.com/new](https://github.com/new) — имя, например `lab11-cicd`
2. **Не** добавляйте README при создании (он уже есть локально)

### 2. Первый push

```bash
cd "D:\проекты 6 сем\Тестирование\lab11"
git remote add origin https://github.com/ВАШ_ЛОГИН/lab11-cicd.git
git push -u origin main
git push -u origin dev
git push -u origin fix
```

### 3. Включите GitHub Pages

**Settings → Pages → Build and deployment:**
- Source: **GitHub Actions**

Деплой запускается автоматически только после успешных тестов при push в `main`.

## Сценарий работы с ветками (п. 6–7)

```bash
git checkout fix
```

Измените текст на форме (например, кнопку с «Отправить» на «Send») — тесты **должны упасть**.

```bash
git add .
git commit --trailer "Co-authored-by: Cursor <cursoragent@cursor.com>" -m "Изменён текст кнопки"
git push origin fix
```

На GitHub:
1. **Pull Request:** `fix` → `dev` — дождитесь CI, исправьте ошибки, merge
2. **Pull Request:** `dev` → `main` — после успешных тестов merge → деплой на Pages

## Проверка падения тестов (п. 5)

Временно измените в `index.html` текст кнопки:

```html
<button type="submit" id="submit-btn">Send</button>
```

Тест `test_submit_button_text` упадёт. Верните «Отправить» перед merge.

## CI/CD

- **CI:** при каждом push и PR запускаются Selenium-тесты
- **CD:** деплой на GitHub Pages только при push в `main` после успешного `test` job