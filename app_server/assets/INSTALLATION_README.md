# Приложение установки Happ

Приложение установки собирается отдельно от основного приложения и может использоваться независимо.

## Структура

- `src/installation-main.ts` - точка входа для приложения установки
- `src/AppInstallation.vue` - корневой компонент приложения установки
- `src/views/AppInstallationView.vue` - главный компонент представления
- `src/components/installation/` - компоненты приложения установки
- `installation.html` - HTML шаблон для приложения установки
- `vite.config.installation.ts` - конфигурация Vite для сборки приложения установки

## Команды

### Разработка

```bash
npm run dev:installation
# или
yarn dev:installation
```

Запускает dev-сервер на порту 8081 с hot-reload.

### Сборка

```bash
npm run build:installation
# или
yarn build:installation
```

Собирает приложение установки в папку `dist-installation/`.

### Превью собранного приложения

```bash
npm run preview:installation
# или
yarn preview:installation
```

Запускает превью собранного приложения на порту 8081.

## Использование

После сборки файлы будут находиться в папке `dist-installation/`. 
Главный HTML файл - `dist-installation/installation.html`.

Приложение установки полностью независимо и не требует основного приложения для работы.

## Переменные окружения

Ссылки на приложения и подписку настраиваются через переменные окружения. 
Создайте файл `.env` в корне папки `app_server/assets/` на основе `.env.example`:

```bash
cp .env.example .env
```

Доступные переменные:
- `VITE_APP_LINK_ANDROID` - ссылка на Google Play
- `VITE_APP_LINK_IPHONE_US` - ссылка на App Store (US) для iPhone/iPad
- `VITE_APP_LINK_IPHONE_RU` - ссылка на App Store (RU) для iPhone/iPad
- `VITE_APP_LINK_WINDOWS` - ссылка на скачивание для Windows
- `VITE_APP_LINK_MAC_US` - ссылка на App Store (US) для macOS
- `VITE_APP_LINK_MAC_RU` - ссылка на App Store (RU) для macOS
- `VITE_SUBSCRIPTION_URL` - ссылка на страницу подписки

Если переменные не заданы, используются значения по умолчанию из `.env.example`.

## Особенности

- Отдельная точка входа (`installation-main.ts`)
- Отдельный HTML шаблон (`installation.html`)
- Отдельная конфигурация сборки (`vite.config.installation.ts`)
- Отдельная папка для сборки (`dist-installation/`)
- Не использует роутер Vue - простое монолитное приложение
- Все стили и зависимости включены в сборку
