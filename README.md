# Общие требования
Работать лучше через SSH. Для этого нужно создать ключ.
Процесс создания описан в [документации GitHub](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent). Кратко:

1. В терминале выполнить, заменив указанный в примере адрес электронной почты:
```commandline
ssh-keygen -t ed25519 -C "your_email@example.com"
```
В результате будет создан новый ключ SSH, где в качестве метки будет использоваться указанный адрес электронной почты.

Когда появится запрос "Ввести файл, в котором сохранить ключ", можно нажать клавишу ВВОД , чтобы принять расположение файла по умолчанию. Обратите внимание, что если вы создали ключи SSH ранее, ssh-keygen может попросить переписать другой ключ, в этом случае рекомендуется создать пользовательский ключ SSH. Для этого введите расположение файла по умолчанию и замените id_ALGORITHM на имя пользовательского ключа.

```commandline
Enter a file in which to save the key (/home/YOU/.ssh/id_ALGORITHM):[Press enter]
```

2. В командной строке введите безопасную парольную фразу (можно оставить пустой):
```commandline
Enter passphrase (empty for no passphrase): [Type a passphrase]
Enter same passphrase again: [Type passphrase again]
```

### Добавление ключа SSH в ssh-agent
Перед добавлением нового ключа SSH в ssh-agent для управления ключами необходимо проверить наличие существующих ключей SSH и создать новый ключ SSH.

1. Запустите агент SSH в фоновом режиме.

```commandline
eval "$(ssh-agent -s)"
```
В зависимости от среды может потребоваться использовать другую команду. Например, вам может потребоваться доступ с правами root, для чего необходимо выполнить `sudo -s -H` перед запуском агента SSH. Может также потребоваться использовать `exec ssh-agent bash` или `exec ssh-agent zsh` для запуска агента SSH.

2. Добавьте закрытый ключ SSH в ssh-agent.

Если вы создали ключ с другим именем или добавляете существующий ключ с другим именем, замените id_ed25519 в команде именем файла закрытого ключа.

```commandline
ssh-add ~/.ssh/id_ed25519
```

3. Добавьте открытый ключ SSH в учетную запись на GitHub. Дополнительные сведения см. в разделе [Добавление нового SSH-ключа в ваш аккаунт GitHub](https://docs.github.com/ru/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).

## Клонирование проекта
Клонировать репозиторий лучше в общий, доступный для всех пользователей ОС, каталог, например `/opt`, чтобы не было проблем доступа для nginx. Для этого нужно просто перейти в него:
```commandline
cd /opt
```
_**Не размещать код в домашней директории `root`!!!**_

Далее создаем каталог проекта 
```commandline
mkdir projectName
```
и клонируем в него репозиторий:

```commandline
git clone git@github.com:VovkaST/outline.git projectName
cd projectName
```

## Настройка
**Все команды выполняются из корневого каталога приложения.**
Для большинства необходимы права суперпользователя (sudo).

### Docker
```commandline
sudo apt update
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
echo "Adding current user to docker group"
sudo usermod -aG docker "$USER"
```

После добавления пользователя в группу `docker` необходимо **перелогиниться** или выполнить `newgrp docker`. Проверка установки:

```commandline
docker compose version
```

### Nginx:
Установка nginx:
```commandline
sudo apt update && sudo apt install nginx -y
```
Закинуть файл настроек nginx для сайта.
```commandline
sudo cp nginx/api-server /etc/nginx/sites-available/api-server
```
**В целевом файле необходимо изменить**:
* `HOST_NAME_OR_IP` &ndash; ip-адрес или имя домена (при наличии, _обязательно для HTTPS_).
* `PATH_TO_APP` &ndash; путь до рабочего каталога приложения (`/opt/projectName` - см.выше).

И создать символическую ссылку на него в каталоге доступных сайтов:
```commandline
sudo ln -s /etc/nginx/sites-available/api-server /etc/nginx/sites-enabled/
```
Проверить корректность настроек:
```commandline
sudo nginx -t
```
Если все ок, перезапускаем службу Nginx:
```commandline
sudo systemctl restart nginx.service
```

**Приложение установки** (опционально) собирается в `dist-installation/` и раздаётся отдельно. Пример location в конфиге Nginx:

```nginx
location = /installation {
    alias /PATH_TO_APP/app_server/assets/dist-installation/installation.html;
}

location /installation/ {
    alias /PATH_TO_APP/app_server/assets/dist-installation/;
}
```

Сборка: `docker compose up assets-installation` (см. раздел «Запуск приложения»).

### Certbot (только при наличии доменного имени)
Установить зависимости:
```commandline
apt update && apt install python3 python3-dev python3-venv libaugeas-dev gcc -y
```
Создадим виртуальное окружение:
```commandline
python3 -m venv /opt/certbot/
/opt/certbot/bin/pip install --upgrade pip
```
И установим Certbot:
```commandline
/opt/certbot/bin/pip install certbot certbot-nginx
```
Создадим символическую ссылку для корректного запуска:
```commandline
ln -s /opt/certbot/bin/certbot /usr/bin/certbot
```
Запросим сертификат:
```commandline
certbot --nginx
```
Настроим автоматическое обновление сертификата:
```commandline
echo "0 0,12 * * * root /opt/certbot/bin/python -c 'import random; import time; time.sleep(random.random() * 3600)' && sudo certbot renew -q" | sudo tee -a /etc/crontab > /dev/null
```
Обновление до актуальной версии (опционально с течением времени):
```commandline
/opt/certbot/bin/pip install --upgrade certbot certbot-nginx
```

### Несколько сайтов на одном сервере
Для каждого дополнительного сайта повторить шаги из раздела «Nginx»:

1. Скопировать конфиг под новое имя (например, второй сайт — `api-server-second`):
   ```commandline
   cp nginx/api-server /etc/nginx/sites-available/api-server-second
   ```
2. В новом файле заменить `HOST_NAME_OR_IP` на домен/IP второго сайта и `PATH_TO_APP` на путь к каталогу приложения этого сайта (отдельная копия приложения со своим `.env` и `app_server/assets/site-config.json`).
3. Включить сайт и перезапустить Nginx:
   ```commandline
   ln -s /etc/nginx/sites-available/api-server-second /etc/nginx/sites-enabled/
   nginx -t && systemctl restart nginx.service
   ```
4. Для настройки HTTPS по новому домену просто запросить сертификат и выбрать нужный домен из списка:
```commandline
certbot --nginx
```
5. Для каждого приложения на одном хосте запускаются свои Docker-контейнеры. Т.к. используются одинаковые по структуре `docker-compose.yaml`, **необходимо задать уникальные имена контейнеров и порты**:
```yaml
services:
  server:
    container_name: outline-api-server-second  # уникальное имя
    ports:
      - "127.0.0.1:8001:8000"  # свободный порт на хосте
  bot:
    container_name: outline-bot-second
  assets:
    container_name: outline-assets-second
  assets-installation:
    container_name: outline-assets-installation-second
```

В конфиге Nginx для второго сайта `proxy_pass` должен указывать на соответствующий порт API (например, `http://127.0.0.1:8001/api`).

### Переменные окружения (backend)

Для передачи настроек в API и бот создайте файл `.env` в корне проекта по образцу `.env.example`:

| Переменная | Назначение |
|------------|------------|
| `SITE_URL` | URL сайта для генерации внутренних ссылок (например, `https://example.ru`) |
| `REQUEST_TOKEN` | Токен для защищённых эндпоинтов (Telegram-бот, рекуррентные платежи Т-Банк); если не используется — можно не задавать |
| `YOOKASSA_ACCOUNT_ID`, `YOOKASSA_TOKEN` | Учётные данные ЮKassa (основная платёжная интеграция по умолчанию) |
| `YOOKASSA_USE_SUCCESS_PAYMENT_REDIRECT_URL` | URL редиректа после успешной оплаты; поддерживается плейсхолдер `{task_id}` |
| `TBANK_TERMINAL_ID`, `TBANK_TERMINAL_PASSWORD` | Учётные данные Т-Банк |
| `TBANK_USE_SUCCESS_PAYMENT_REDIRECT_URL`, `TBANK_USE_FAIL_PAYMENT_REDIRECT_URL` | URL редиректов Т-Банк; в success-URL — плейсхолдер `{task_id}` |
| `WATA_TOKEN` | Токен WATA |
| `WATA_USE_SUCCESS_PAYMENT_REDIRECT_URL`, `WATA_USE_FAIL_PAYMENT_REDIRECT_URL` | URL редиректов WATA; в success-URL — плейсхолдер `{task_id}` |
| `PLANFIX_ACCOUNT`, `PLANFIX_TOKEN` | Интеграция с PlanFix |
| `DEFAULT_PAYMENT_DEADLINE` | Время жизни ссылки на оплату в минутах (по умолчанию `30`) |
| `DEFAULT_RATE_LIMIT` | Лимит запросов к API (по умолчанию `50/minute`) |
| `S3_ACCESS_KEY`, `S3_SECRET_KEY`, `S3_BUCKET_NAME`, `S3_ENDPOINT_URL` | Хранилище S3 (Yandex Object Storage и аналоги) |
| `BOT_TOKEN` | Токен Telegram-бота (для контейнера `bot`) |

Рекомендуемый URL успешной оплаты для всех платёжных систем: `https://example.ru/task/{task_id}/success/`.

### Переменные окружения фронтенда (`app_server/assets/.env`)

Создайте по образцу `app_server/assets/.env.example`. Значения **вшиваются при сборке** контейнера `assets` — после изменения нужна пересборка фронта.

| Переменная | По умолчанию | Назначение |
|------------|--------------|------------|
| `VITE_USE_DUMMY_CONFIG` | `false` | Dummy-режим: подменная страница успешной оплаты и текст публичной оферты (см. ниже) |
| `VITE_BASE_URL` | `http://127.0.0.1:8000` | Базовый URL API (для локальной разработки) |
| `VITE_APP_POOLING_INTERVAL` | `1500` | Интервал опроса статуса платежа, мс |
| `VITE_APP_LINK_ANDROID` | см. `.env.example` | Ссылка на Google Play |
| `VITE_APP_LINK_IPHONE_US`, `VITE_APP_LINK_IPHONE_RU` | см. `.env.example` | Ссылки на App Store |
| `VITE_APP_LINK_WINDOWS` | см. `.env.example` | Ссылка на установщик Windows |
| `VITE_APP_LINK_MAC_US`, `VITE_APP_LINK_MAC_RU` | см. `.env.example` | Ссылки на App Store для macOS |
| `VITE_SUBSCRIPTION_URL` | см. `.env.example` | URL страницы подписки |

#### Dummy-режим (white-label)

Флаг `VITE_USE_DUMMY_CONFIG` переключает:

- содержимое маршрута `/task/{task_id}/success/` — `false` (по умолчанию) инструкции по активации VPN, `true` dummy-страница «облачное хранилище»;
- текст публичной оферты в футере — `false` оферта с автоплатежом, `true` оферта на хранение видеозаписей;
- страницу выбора тарифа `/task/{task_id}/` — при `true`:
  - показывается info-блок `DummyStorageInfo` (описание услуги хранения и строка «Услугу оказывает организация …» с `site.name`);
  - скрыты: блок «Оплата подписки» (`SubscriptionRef`), карточка «1 ключ / одно устройство», WhatsApp-предупреждение об оплате за клиента и кнопка добавления подписки.

В dummy-режиме поле `tariffs[].period` — произвольная подпись тарифа (например, объём: `"100 ГБ"`, `"1 ТБ"`), а не период подписки. Заголовок над тарифами задаётся через `site.tariffsHeader`.

Цена на dummy-странице подставляется из `site-config.json` → `tariffs[0].price` (в бейдже и в тексте шага 3).

Включение:

```commandline
# app_server/assets/.env
VITE_USE_DUMMY_CONFIG=true
```

После изменения:

```commandline
docker compose up assets
```

### Страницы фронтенда

| Маршрут | Назначение |
|---------|------------|
| `/task/{task_id}/` | Выбор тарифа и оплата |
| `/task/{task_id}/success/` | Страница успешной оплаты (VPN или dummy — по флагу `VITE_USE_DUMMY_CONFIG`) |
| `/payment/app/tariffs/?task={id}` | Редирект на `/task/{id}/` (обратная совместимость) |

### site-config.json

В нем хранятся настройки владельца сайта, отображаемые на фронте. Файл не в репозитории. Создать вручную: скопировать `app_server/assets/site-config.json.example` в `site-config.json` в каталоге `app_server/assets/` и заполнить. При сборке фронта настройки **вшиваются в JavaScript-бандл**. Поэтому **после изменения на продуктовом стенде необходимо пересобрать фронт** (см. ниже).

Значения по умолчанию для необязательных полей задаются в коде — [`app_server/assets/src/config/siteConfig.defaults.ts`](app_server/assets/src/config/siteConfig.defaults.ts), а не дублируются в JSON.

**Обязательные поля** (должны быть в JSON):

| Блок | Поля | Примечание |
|------|------|------------|
| `site` | `name`, `url`, `title` | Название сайта, URL и заголовок страницы |
| `organization` | `fullName`, `inn`, `legalAddress`, `bank`, `bankAccount`, `correspondentAccount`, `bik`, `phone`, `email` | Реквизиты ИП/ООО для футера и оферты |
| `publicOffer` | `city`, `representativeName` | Город и ФИО представителя в род. падеже |
| `tariffs` | минимум 1 элемент | Список тарифов `{ "period": string, "price": number, "featured?": boolean }`. `period` — подпись тарифа (период подписки или, в dummy-режиме, объём: `"100 ГБ"`, `"300 ГБ"`). Первый тариф (`tariffs[0].price`) используется на подменной странице успешной оплаты при `VITE_USE_DUMMY_CONFIG=true` |

**Необязательные поля** (есть значения по умолчанию в коде):

| Поле | Значение по умолчанию | Примечание |
|------|----------------------|------------|
| `site.copyrightSuffix` | `''` | Суффикс копирайта в футере |
| `site.tariffsHeader` | `'Выберите тариф'` | Заголовок блока выбора тарифа |
| `publicOffer.representativeBasis` | `'Устава'` | Основание полномочий представителя |
| `organization.ogrn` | — | ОГРН (не задаётся по умолчанию) |
| `supportItems` | `[]` | Ссылки поддержки (кнопки в блоке «Напишите нам»), массив `{ "url", "text" }` |
| `subscriptionAddUrl` | `''` | URL для кнопки «Добавить подписку» |
| `announcement` | не задан | Настройки баннера на странице тарифов |

Настройки `announcement`:
- `title` — заголовок баннера.
- `paragraphs` — массив строк с основным текстом баннера.
- `cta` — выделенная строка призыва к действию (опционально).
- `deadline` — ISO дата-время, до которого показывается таймер и сам баннер (опционально).

Логика отображения баннера:
- Если `announcement` отсутствует — баннер не отображается.
- Если `deadline` не задан — баннер отображается всегда, таймер не показывается.
- Если `deadline` задан и текущее время меньше него — показываются баннер и таймер.
- Если `deadline` задан и время истекло — баннер не отображается.



### Запуск приложения
Перед первым запуском необходимо дать права на исполнение файлу скрипта:
```commandline
chmod +x run_server.sh
```

Затем запустить его:
```commandline
./run_server.sh
```

Скрипт собирает Docker-образ, пересобирает основной фронт (`assets`) и поднимает API (`server`).

**Сборка приложения установки** (опционально, в `dist-installation/`):

```commandline
docker compose up assets-installation
```

### Перезапуск и пересборка после изменений

| Что изменилось | Команда |
|----------------|---------|
| Корневой `.env` (backend) | `docker compose up -d server` и/или `docker compose up -d bot` |
| `app_server/assets/.env` или `site-config.json` | `docker compose up assets` |
| Приложение установки | `docker compose up assets-installation` |

Для one-shot сборки фронта (`assets`, `assets-installation`) предпочтительно `docker compose up` **без** `-d` — контейнер завершится после сборки.

## _Только для локальной разработки. Для доступа на продуктовом сервере необходима соответствующая настройка Nginx._
По умолчанию приложение будет доступно в браузере по адресу: http://127.0.0.1:8000/.
API-документация:
* Swagger: http://127.0.0.1:8000/docs/
* Redoc: http://127.0.0.1:8000/redoc/


## Проверка состояния сервисов

### Healthcheck API

Контейнер `server` проверяет доступность по эндпоинту:

```commandline
curl http://127.0.0.1:8000/api/health/
```

### Состояние контейнеров
```commandline
docker ps
CONTAINER ID   IMAGE                            COMMAND                  CREATED         STATUS         PORTS                      NAMES
fdbda06e0bbb   outline-app-python-3.10:latest   "python -m server --…"   5 minutes ago   Up 5 minutes   127.0.0.1:8000->8000/tcp   outline-api-server
0820cabc2512   outline-app-python-3.10:latest   "python -m bot run"      5 minutes ago   Up 5 minutes                              outline-bot
```
В зависимости от целевого решения, должны быть запущены контейнеры `outline-bot` (Telegram-бот) и/или `outline-api-server` (API платёжного сервиса). Контейнеры `outline-assets` и `outline-assets-installation` — одноразовые: запускаются для сборки фронта и завершаются. Имена контейнеров могут отличаться при настройке нескольких сайтов (см. раздел **Несколько сайтов на одном сервере**).
Для вывода всех, даже остановленных контейнеров, добавить ключ `-a`.

### Просмотр логов контейнера
Вывод всех логов контейнера `outline-api-server` (имя указано в последнем столбце вывода команды `docker ps` выше)
```commandline
docker logs outline-api-server
```

Вывод последних 100 строк логов контейнера `outline-api-server`:
```commandline
docker logs outline-api-server --tail 100
```

Вывод последних 100 строк логов контейнера `outline-api-server` и дальнейшее "живое" их отслеживание:
```commandline
docker logs outline-api-server --tail 100 --follow
```
Остановка отслеживания: `Ctrl+C`.
