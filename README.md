## YouTube Analyze (MVP)

Tool that fetches a YouTube transcript and produces a concise summary with Gemini. Early-stage build: single screen, URL input, button, video preview, and the generated text.

### Status

- MVP in progress; happy-path works.
- Minimal, distraction-free UI/UX.
- Docker packaging is planned to simplify deployment anywhere.
- Plan: publish a trial on a free hosting; the link will appear here once ready.

### How to run locally

Requirements: Python 3.12+, [uv](https://docs.astral.sh/uv/) (backend deps), pnpm 10+, Node 20+.

**1) Backend (FastAPI + Gemini)**

```bash
cd analyze_api
uv sync  # install deps from pyproject.toml

# Add Gemini key to .env
echo "GEMINI_API_KEY=your_key_here" > .env

uv run uvicorn main:app --reload --port 8000
```

**2) Frontend (Vite + React + shadcn/ui)**

```bash
cd analyze_web
pnpm install
pnpm dev  # defaults to http://localhost:5173
```

Frontend calls `http://localhost:8000/video/transcript/?url=...`, so run the backend first.

### What’s next

- Dockerfile/compose to build frontend + backend with a single command.
- Trial sandbox on free hosting (link will be added here once live).
- Small UX improvements (persist last links, dark/light mode).
- Change all hardcoded links to .env

# YouTube Analyze (MVP)

Инструмент, который забирает транскрипт с YouTube и делает краткий конспект через Gemini. Сейчас это ранняя версия: один экран, инпут с URL, кнопка, превью ролика и готовый текст.

## Статус

- MVP в разработке, базовый happy-path работает.
- Дизайн и UX минималистичные, без дополнительных экранов.
- Скоро добавлю Docker-сборку, чтобы упростить деплой куда угодно.
- План: задеплоить trial-версию на бесплатный хостинг; здесь появится ссылка, как только будет готово.

## Как запустить локально

Требования: Python 3.12+, [uv](https://docs.astral.sh/uv/) (для зависимостей бэкенда), pnpm 10+, Node 20+.

### 1) Бэкенд (FastAPI + Gemini)

```bash
cd analyze_api
uv sync  # установит зависимости из pyproject.toml

# Добавь ключ Gemini в .env
echo "GEMINI_API_KEY=your_key_here" > .env

uv run uvicorn main:app --reload --port 8000
```

### 2) Фронтенд (Vite + React + shadcn/ui)

```bash
cd analyze_web
pnpm install
pnpm dev  # по умолчанию http://localhost:5173
```

Фронт стучится на `http://localhost:8000/video/transcript/?url=...`, поэтому важно запустить бэкенд перед отправкой запросов.

## Что планируется дальше

- Dockerfile/compose для сборки фронта и бэка одной командой.
- Песочница на бесплатном хостинге (сюда добавлю ссылку, как только подниму триал).
- Небольшие улучшения UX (сохранение последних ссылок, тёмная/светлая тема).
- Перенести все хардкодные ссылки на .env
