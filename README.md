# Сервис для генерации подписки

## Клонирование репозитория
```commandline
git clone git@github.com:VovkaST/outline.git
cd outline
```

## Настройка
**Все команды выполняются из корневого каталога приложения.**
Для большинства необходимы права суперпользователя (sudo).

### Docker
```commandline
apt update
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg
echo   "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
tee /etc/apt/sources.list.d/docker.list > /dev/null
apt update
apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose
echo "Adding current user to docker group"
usermod -aG docker $USER  
```

### Nginx:
Установка nginx:
```commandline
apt update && apt install nginx -y
```
Закинуть файл настроек nginx для сайта.
```commandline
cp nginx/api-server /etc/nginx/sites-available/api-server
```
**В целевом файле необходимо изменить**:
* `HOST_NAME_OR_IP` &ndash; ip-адрес или имя домена (при наличии, _обязательно для HTTPS_).
* `PATH_TO_APP` &ndash; путь до рабочего каталога приложения.

И создать символическую ссылку на него в каталоге доступных сайтов:
```commandline
ln -s /etc/nginx/sites-available/api-server /etc/nginx/sites-enabled/
```
Проверить корректность настроек:
```commandline
nginx -t
```
Если все ок, перезапускаем:
```commandline
systemctl restart nginx.service
```

### Certbot (только при наличии доменного имени)
Установить зависимости:
```commandline
apt update && apt install python3 python3-dev python3-venv libaugeas-dev gcc
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
5. Для каждого приложения будет запускаться свой Docker-контейнер для обработки API. Т.к. используются одинаковые по структуре docker-compose-файлы, **необходимо изменить имя контейнера сервера** в `docker-compose.yaml`:
```yaml
services:
  server:
    image: outline-app-python-3.10:latest
    container_name: outline-api-server  # Задать уникальное имя контейнера
    env_file:
      - .env
    environment:
...
    ports:
      - "127.0.0.1:8001:8000"  # Изменить порт на хосте на свободный, например 8001
```

### Переменные окружения
Для передачи настроек в приложение необходимо создать файл `.env` по образцу `.env.example`:
* `SITE_URL` &ndash; url-сайта для генерации ссылок на внутренние ресурсы
* `REQUEST_TOKEN` &ndash; токен для эндпоинтов, требующих авторизацию
* `TBANK_TERMINAL_ID` &ndash; идентификатор терминала Т-банка
* `TBANK_TERMINAL_PASSWORD` &ndash; пароль терминала
* `TBANK_USE_SUCCESS_PAYMENT_REDIRECT_URL` &ndash; url для редиректов успешных платежей
* `TBANK_USE_FAIL_PAYMENT_REDIRECT_URL` &ndash; url для редиректов платежей, завершившихся ошибкой
* `YOOKASSA_ACCOUNT_ID` &ndash; идентификатор аккаунта Yookassa
* `YOOKASSA_TOKEN` &ndash; токен API Yookassa
* `YOOKASSA_USE_SUCCESS_PAYMENT_REDIRECT_URL` &ndash; url для редиректов успешных платежей 
* `PLANFIX_ACCOUNT` &ndash; имя аккаунта PlanFix
* `PLANFIX_TOKEN` &ndash; токен API PlanFix
* `DEFAULT_PAYMENT_DEADLINE` &ndash; время жизни ссылки платежа (необязательный).

### site-config.json

В нем хранятся настройки владельца сайта, отображаемые на фронте. Файл не в репозитории. Создать вручную: скопировать `app_server/assets/site-config.json.example` в `site-config.json` в каталоге `app_server/assets/` и заполнить. При сборке фронта файл копируется в `dist/`, чтобы работал и в production. Поэтому **после изменения на продуктовом стенде необходимо пересобрать фронт** (см. ниже).

**Структура:**

| Блок | Поля | Примечание |
|------|------|------------|
| `site` | `name`, `copyrightSuffix?`, `url`, `title` | Название сайта, суффикс копирайта в футере, URL и заголовок страницы |
| `organisation` | `fullName`, `inn`, `ogrn?`, `legalAddress`, `bank`, `bankAccount`, `correspondentAccount`, `bik`, `phone`, `email` | Реквизиты ИП/ООО для футера и оферты |
| `publicOffer` | `city`, `representativeName`, `representativeBasis` | Город, ФИО представителя в род. падеже, основание (напр. «Устава») |
| `supportItems` | массив `{ "url", "text" }` | Ссылки поддержки (кнопки в блоке «Напишите нам») |



### Запуск приложения
Перед первым запуском необходимо дать права на исполнение файлу скрипта:
```commandline
chmod +x run_server.sh
```

Затем для запустить его:
```commandline
./run_server.sh
```

### Перезапуск приложения после простого изменения переменных окружения
После изменения переменных окружения в `.env`-файле необходимо перезапустить целевой контейнер:
```commandline
docker compose up -d server    # Приложение API
docker compose up -d bot       # Telegram-бот
docker compose up -d assets    # Пересобрать фронт
```

## _Только для локальной разработки. Для доступа на продуктовом сервере необходима соответствующая настройка Nginx._
По умолчанию приложение будет доступно в браузере по адресу: http://127.0.0.1:8000/.
API-документация:
* Swagger: http://127.0.0.1:8000/docs/
* Redoc: http://127.0.0.1:8000/redoc/
