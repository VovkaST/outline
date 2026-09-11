"""HTML-страницы редиректа (`GET /tg/go` и `GET /tg/go/run`).

Минималистичные страницы без внешних ассетов — отрисовываются мгновенно. Палитра и типографика
взяты из фронта `app_server/assets/` (classic-тема, `src/themes/classic.scss` + `src/assets/base.scss`),
чтобы страница выглядела продолжением сайта, а не чужим платёжным шлюзом.
"""

import html
import json

from root.config import settings

_MARK = "🔐"


def _bot_username() -> str:
    return (settings.BOT_USERNAME or "").lstrip("@")


def _page(title: str, body: str, button_tail: str | None = None, redirect_url: str = "") -> str:
    """Общая обёртка всех страниц редиректа.

    `button_tail` — хвост ссылки «Вернуться в бота» (`?start=...` или ""); без имени бота кнопку
    не рисуем. `redirect_url` ставит `<meta refresh>` — он обязан быть в `<head>`.
    """
    button_html = ""
    bot_username = _bot_username()
    if button_tail is not None and bot_username:
        href = f"https://t.me/{html.escape(bot_username)}{html.escape(button_tail)}"
        button_html = f'\n        <a href="{href}" class="button">Вернуться в бота</a>'

    refresh_html = (
        f'\n    <meta http-equiv="refresh" content="0;url={html.escape(redirect_url)}">' if redirect_url else ""
    )

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">{refresh_html}
    <title>{html.escape(title)}</title>
    <style>
        /* Палитра classic-темы фронта (app_server/assets/src/themes/classic.scss). */
        :root {{
            --bg: #ffffff;
            --bg-soft: #f6f7f9;
            --border: #e6e8ec;
            --ink: #0f1115;
            --ink-dim: #5a6270;
            --ink-faint: #8b95a3;
            --primary: #c9a961;
            --primary-hover: #b8954a;
            --primary-soft: #faf3e3;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-soft);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            color: var(--ink);
            -webkit-font-smoothing: antialiased;
        }}
        .container {{
            background: var(--bg);
            border: 1px solid var(--border);
            border-radius: 16px;
            box-shadow: 0 12px 40px rgba(15, 17, 21, 0.12);
            padding: 40px 32px;
            max-width: 420px;
            width: 100%;
            text-align: center;
        }}
        .mark {{
            width: 56px;
            height: 56px;
            margin: 0 auto 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            border-radius: 16px;
            background: linear-gradient(135deg, #d4b876, #a8893f);
            color: #ffffff;
            box-shadow: 0 4px 14px rgba(201, 169, 97, 0.4);
        }}
        h1 {{
            font-size: 18px;
            font-weight: 700;
            letter-spacing: -0.2px;
            color: var(--ink);
            margin-bottom: 12px;
        }}
        p {{
            font-size: 15px;
            line-height: 1.6;
            color: var(--ink-dim);
            margin-bottom: 20px;
        }}
        .button {{
            display: inline-block;
            padding: 12px 28px;
            background: var(--primary);
            color: #ffffff;
            text-decoration: none;
            border-radius: 0.6rem;
            font-weight: 600;
            font-size: 15px;
        }}
        .button:hover {{ background: var(--primary-hover); }}
        .fallback {{ font-size: 13px; color: var(--ink-faint); margin-bottom: 0; }}
        .fallback a {{ color: var(--primary-hover); }}
        .spinner {{
            display: inline-block;
            width: 40px;
            height: 40px;
            border: 4px solid var(--primary-soft);
            border-top-color: var(--primary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 18px;
        }}
        @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="mark">{_MARK}</div>
        <h1>{html.escape(title)}</h1>
        {body}{button_html}
    </div>
</body>
</html>
"""


def page_waiting(
    run_url: str,
    title: str = "Готовим оплату",
    fallback_text: str = "Если оплата не открылась — нажмите здесь",
) -> str:
    """Страница-прокладка: отдаётся мгновенно и сама уходит на `run_url`.

    Переход дублирован намеренно: `<meta refresh>` в `<head>` работает без JavaScript,
    `location.replace` — быстрее и не оставляет прокладку в истории браузера (иначе кнопка
    «назад» с платёжной формы возвращала бы клиента сюда, и платёж создавался бы заново).
    Видимая ссылка — последний рубеж.

    У атрибута `href` и у JS-строки разные правила экранирования `&`: `html.escape` даёт
    `&amp;`, браузер разворачивает это обратно только в атрибуте. Внутри `<script>` замену
    пришлось бы не делать — для JS-литерала используем `json.dumps`.
    """
    body = f"""<div class="spinner"></div>
        <p>{html.escape(title)}…</p>
        <p class="fallback"><a href="{html.escape(run_url)}">{html.escape(fallback_text)}</a></p>
        <script>
            location.replace({json.dumps(run_url)});
        </script>"""
    return _page(title, body, redirect_url=run_url)


def page_error() -> str:
    """Платёж не создан: сбой сети, отказ API, не настроены креды или нет задачи в Planfix."""
    body = """<p>Не получилось создать платёж — похоже, это временный сбой.</p>
        <p>Попробуйте ещё раз, а если не выйдет — напишите нам в поддержку.</p>"""
    return _page("Не получилось", body, button_tail="")


def page_expired() -> str:
    """Подпись не сошлась, срок ссылки истёк или тариф неизвестен.

    Для клиента все случаи выглядят одинаково — «ссылка больше не работает». Подробности не
    раскрываем: по разным текстам подбирать подпись было бы проще.
    """
    body = """<p>Ссылка устарела или повреждена.</p>
        <p>Откройте бота заново и попробуйте ещё раз.</p>"""
    return _page("Ссылка устарела", body, button_tail="")
