## YouTube Analyze (MVP)

Tool that fetches a YouTube transcript and produces a concise summary with Gemini. Early-stage build: single screen, URL input, button, video preview, and the generated text.

### Status

- MVP in progress; happy-path works.
- Minimal, distraction-free UI/UX.
- Dockerfiles and compose configs are in place (dev/prod overlays).
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

### Run with Docker Compose

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
OR
docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build
```

Place your `.env` with `GEMINI_API_KEY` in `analyze_api/.env` before building.

### What’s next

- Trial sandbox on free hosting (link will be added here once live).
- Small UX improvements (persist last links, dark/light mode).
- Move hardcoded URLs to env configs.

# YouTube Analyze (MVP)

Инструмент, который забирает транскрипт с YouTube и делает краткий конспект через Gemini. Сейчас это ранняя версия: один экран, инпут с URL, кнопка, превью ролика и готовый текст.

## Статус

- MVP в разработке, базовый happy-path работает.
- Дизайн и UX минималистичные, без дополнительных экранов.
- Есть Dockerfile и docker-compose (dev/prod слои).
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

## Запуск через Docker Compose

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

ИЛИ

docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build
```

Положи `.env` с `GEMINI_API_KEY` в `analyze_api/.env` перед сборкой.

## Что планируется дальше

- Dockerfile/compose для сборки фронта и бэка одной командой.
- Песочница на бесплатном хостинге (сюда добавлю ссылку, как только подниму триал).
- Небольшие улучшения UX (сохранение последних ссылок, тёмная/светлая тема).
- Перенести все хардкодные ссылки на .env
