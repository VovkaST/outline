# AGENTS.md

Справка для агентов по репозиторию. Подробная инструкция по развёртыванию — в [README.md](README.md), по приложению установки — в [INSTALLATION_README.md](app_server/assets/INSTALLATION_README.md). Здесь только то, что нужно знать до начала работы.

## Что это за проект

Платёжный фронт + API для продажи VPN-подписок. Клиент попадает на страницу `/task/{task_id}/`, выбирает тариф, оплачивает через платёжный шлюз и получает ключ/подписку. Задачи и клиенты живут в CRM Planfix, уведомления — через Telegram-бот.

Три деплоя из одного кода:
* **server** — FastAPI-API (`python -m server run`);
* **bot** — Telegram-бот (`python -m bot run`);
* **assets** — Vue-фронт, собирается в статику и раздаётся nginx.

Один и тот же код разворачивается на нескольких стендах (несколько сайтов/владельцев), различия — в `.env` и `site-config.json` каждого стенда. Это причина большинства расхождений «на dev не воспроизводится».

## Структура

| Путь | Что внутри |
|---|---|
| [server.py](server.py), [bot.py](bot.py) | CLI-точки входа (click), выставляют `SETTINGS_MODULE` |
| [app_server/](app_server/) | FastAPI-приложение: [app.py](app_server/app.py) (сборка app, middleware, rate limit, обработчики ошибок), [routes/](app_server/routes/) (`keys`, `orders`, `payments`, `payments_2`, `server`, `subscription`, `tasks`), `dtos.py`, `config.py` |
| [app_bot/](app_bot/) | Telegram-бот: `bot.py`, `handlers/`, `interaction/`, `routes.py` (эндпоинты бота, подключаются в app_server), `s3.py` |
| [services/](services/) | Внешние интеграции: `payment.py` (Т-Банк), `yookassa.py`, `wata.py`, `planfix/`, `http_service.py` (общий aiohttp-клиент, `BaseHTTPService.close_all()` в lifespan) |
| [root/](root/) | Инфраструктура: `config.py` (`settings`), `middleware/`, `media_storage.py`, `exceptions.py`, `utils/` |
| [settings/](settings/) | `base.py` + `local.py`/`prod.py`, читают переменные окружения (`env.get`/`env.as_int`) |
| [app_server/assets/](app_server/assets/) | Фронт (Vue 3 + TS + Vite + Pinia + vue-router + SCSS) |
| [nginx/api-server](nginx/api-server) | Шаблон конфига сайта: статика из `app_server/assets/dist`, `/api` проксируется на `127.0.0.1:8000` |
| [.github/workflows/](.github/workflows/) | `ci.yml` (ruff + eslint + vue-tsc) и ручные деплои `deploy-back/bot/front` через `deploy-reusable.yml` |

## Фронт: ключевые факты

* Сборка: `vite build`, вход [src/main.ts](app_server/assets/src/main.ts) → `dist/`; отдельная сборка приложения установки — [vite.config.installation.ts](app_server/assets/vite.config.installation.ts) → `dist-installation/`.
* Маршруты SPA — [src/router/index.ts](app_server/assets/src/router/index.ts): `/task/:taskId/`, `/task/:taskId/success/`, редирект со старого `/payment/app/tariffs/?task=`.
* API-клиент **генерируется**: `yarn schema:generate` из `src/api/schema.json` в `src/api/generated/public`. Не править сгенерированное руками, не забывать про этот шаг перед сборкой/линтом.
* Две темы оформления — [src/themes/](app_server/assets/src/themes/) (`classic`, `babochki`), выбираются через `site.theme`; неизвестное значение падает в `classic`. Тема проставляется атрибутом `data-theme` на `:root` в [App.vue:10](app_server/assets/src/App.vue#L10), компоненты ветвятся по `isBabochkiTheme` (в теме `babochki` часть блоков скрыта, а в логотипе вместо буквы рисуется SVG-бабочка).
* Флаг `VITE_USE_DUMMY_CONFIG` включает «подменный» режим (dummy-страница успеха, оферта хранилища вместо VPN) — влияет на состав блоков в [AppTariffSelectView.vue](app_server/assets/src/views/AppTariffSelectView.vue) и [PaymentSuccessView.vue](app_server/assets/src/views/PaymentSuccessView.vue).

### site-config.json — главный источник расхождений со стендами

* [app_server/assets/site-config.json](app_server/assets/site-config.json) **не в репозитории** (в `.gitignore`), создаётся из `site-config.json.example`. У каждого стенда он свой.
* Конфиг **импортируется как JSON-модуль** ([src/config/siteConfig.ts](app_server/assets/src/config/siteConfig.ts)) и **вшивается в бандл на сборке**. Правка на проде без `docker compose up assets` не даёт эффекта. Runtime-загрузки конфига нет; `dist/site-config.json`, если он где-то лежит, ни на что не влияет.
* Значения по умолчанию и валидация обязательных полей — [src/config/siteConfig.defaults.ts](app_server/assets/src/config/siteConfig.defaults.ts) (`mergeSiteConfig`, бросает ошибку на отсутствующих полях). Дефолты держим в коде, а не в JSON.
* Доступ в компонентах — только через `useConfig()` ([src/composables/useConfig.ts](app_server/assets/src/composables/useConfig.ts)), возвращает `readonly` ref.
* Данные из конфига заполняет владелец сайта вручную, поэтому в строках регулярно попадаются невидимые символы (NBSP, zero-width, BOM). Любой разбор строк из конфига должен нормализовать пробелы — см. `siteName` в [Header.component.vue](app_server/assets/src/components/tariffs/Header.component.vue).

## Бэкенд: ключевые факты

* FastAPI + uvicorn, Python 3.10, версии зависимостей зафиксированы в [requirements/base.txt](requirements/base.txt) (`local.txt` — для разработки).
* Настройки — только через переменные окружения корневого `.env` (см. [.env.example](.env.example)); модуль выбирается `SETTINGS_MODULE` (`settings.local` по умолчанию в CLI, `settings.prod` в docker-compose).
* Платёжные шлюзы: Т-Банк, ЮKassa, WATA. Выбор по умолчанию — `DEFAULT_PAYMENT_AGENT`. У каждого свои `*_USE_SUCCESS_PAYMENT_REDIRECT_URL` / `*_USE_FAIL_...`, в них поддерживается плейсхолдер `{task_id}`.
* Middleware подключаются по списку строк `settings.MIDDLEWARE` через importlib; rate limit — slowapi, `DEFAULT_RATE_LIMIT`.
* Ошибки: `AppError`, `PaymentError`, `PaymentGatewayError` с обработчиками в [error_handlers.py](app_server/error_handlers.py) — новые ошибки заводить в этой иерархии, а не отдавать голые HTTPException.
* Секреты (`.env`, `keys/`, `media/`, `logs/`) в репозиторий не попадают и в вывод/коммиты тоже.

## Команды

Бэкенд (из корня):

```bash
ruff check .          # то же гоняет CI
ruff format --check .
```

Фронт (из `app_server/assets`):

```bash
yarn schema:generate  # обязательный шаг перед lint/build на чистом клоне
yarn type-check       # vue-tsc, гоняется в CI
yarn exec eslint "src/**/*.ts" --max-warnings 0   # CI линтует только .ts
yarn dev              # http://127.0.0.1:8080
yarn build-only       # сборка в dist/ (--emptyOutDir)
```

Docker (из корня):

```bash
./run_server.sh                    # образ + пересборка фронта + подъём API
docker compose up assets           # только пересборка фронта (после правки .env/site-config.json)
docker compose up -d server bot    # backend
docker compose -f docker-compose-local.yaml up assets   # dev-сервер фронта в контейнере
```

Тесты: конфигурация pytest есть в [setup.cfg](setup.cfg), но каталога с тестами в репозитории нет — не обещать «прогоню тесты», проверять правки линтерами, `type-check` и ручным сценарием.

Известная особенность окружения: `npx eslint <файл>.vue` падает с `Parsing error: '>' expected` на **любом** `.vue` в репозитории — это состояние конфига линтера, а не дефект правки. CI линтует только `src/**/*.ts`.

## Соглашения

* Язык общения и текстов для пользователя — русский. Комментарии в коде тоже русские, пишем их только там, где логика неочевидна.
* Python: ruff, `line-length = 120`, двойные кавычки, target `py310`, isort с first-party `root`, `app_server`.
* TS/Vue: `<script setup lang="ts">`, Composition API, алиас `@` → `src`, SCSS в scoped-блоках, стилевые значения — через CSS-переменные тем (`var(--primary)`, `var(--logo-mark-background)`), а не хардкодом цвета.
* Ветки от `master`, названия вида `feature/<тема>`. Коммитить и пушить только по явной просьбе.
* При правках, влияющих на поведение стендов (новые поля конфига, новые переменные окружения, изменение процедуры сборки), обновлять соответствующие таблицы в [README.md](README.md).

## Диагностика проблем «работает на dev, не работает на проде»

Почти всегда причина одна из трёх:

1. **Фронт не пересобран** — `site-config.json`/`.env` вшиваются в бандл. Проверить дату `app_server/assets/dist` и наличие значения в бандле (`grep -o '<значение>' app_server/assets/dist/*.js`).
2. **Данные конфига отличаются** — включая невидимые символы. Проверять побайтово:
   `python3 -c "import json;d=json.load(open('app_server/assets/site-config.json'));n=d['site']['name'];print(repr(n),[hex(ord(c)) for c in n], d['site'].get('theme'))"`.
3. **Кэш у клиента** — в [nginx/api-server](nginx/api-server) `index.html` отдаётся без `Cache-Control` (хэшируются только js/css). Проверять жёсткой перезагрузкой или приватным окном.
