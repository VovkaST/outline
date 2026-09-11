"""Промежуточная страница оплаты для бота: `GET /tg/go` и `GET /tg/go/run`.

Кнопка тарифа в боте — это URL-кнопка на подписанную ссылку `/tg/go?a=pay&t=<tariff>&u=<tg_id>&e=&s=`.

- `GET /tg/go` — проверяет подпись и мгновенно отдаёт HTML-прокладку со спиннером, которая
  тут же уходит на `/tg/go/run` (тот же querystring).
- `GET /tg/go/run` — снова проверяет подпись, находит задачу клиента в Planfix, создаёт платёж
  через платёжный сервис из `settings.DEFAULT_PAYMENT_AGENT` (`init_payment`, та же логика,
  что за `GET /api/v2/payment/init/`) и редиректит (302) на форму оплаты.

Две стадии нужны, чтобы Telegram-webview получил страницу мгновенно, а долгий вызов платёжного
шлюза шёл уже во второй, «настоящей» навигации; `location.replace` не оставляет прокладку в
history (иначе «назад» с формы оплаты пересоздавал бы платёж).
"""

import logging

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from app_bot import links
from app_bot.tariffs import get_tariff
from app_bot.utils.dialogs import clear_username
from app_server import redirect_pages as pages
from app_server.utils import DEFAULT_PAYMENT_AGENT, get_payment_service
from root.utils.others import get_route_name
from services import planfix_webchat
from services.planfix.exceptions import TaskNotFoundError
from services.planfix.utils import get_task

logger = logging.getLogger("app_server")

routes = APIRouter(tags=["Redirect"], include_in_schema=False, generate_unique_id_function=get_route_name)


@routes.get(links.PATH)
async def redirect_entry(request: Request):
    """Точка входа: проверяет подпись, отдаёт прокладку с автопереходом на `/tg/go/run`."""
    params = links.verify(request.query_params)
    if params is None or params.get("a") != "pay":
        return HTMLResponse(pages.page_expired())

    # Подпись покрывает все параметры, поэтому переносим querystring во второй шаг целиком.
    run_url = f"{links.PATH_RUN}?{request.url.query}"
    return HTMLResponse(pages.page_waiting(run_url))


@routes.get(links.PATH_RUN)
async def redirect_run(request: Request):
    """Реальная обработка: тариф -> задача Planfix -> платёж -> 302 на оплату."""
    params = links.verify(request.query_params)
    if params is None or params.get("a") != "pay":
        return HTMLResponse(pages.page_expired())

    tariff = get_tariff(params.get("t", ""))
    telegram_id = params.get("u", "")
    if tariff is None or not telegram_id.isdigit():
        return HTMLResponse(pages.page_expired())

    try:
        task = await get_task(telegram_id=int(telegram_id))
    except TaskNotFoundError:
        logger.warning("redirect_run: задача Planfix не найдена для tg=%s", telegram_id)
        return HTMLResponse(pages.page_error())

    # Лог выбора тарифа в Planfix — до долгого вызова шлюза, чтобы событие не потерялось.
    try:
        await planfix_webchat.chat.new_message(
            chat_id=telegram_id,
            contact_id=telegram_id,
            contact_name=clear_username(None),
            message=f"Выбрал тариф: {tariff.title}",
        )
    except Exception:  # noqa: BLE001
        logger.warning("redirect_run: не удалось залогировать выбор тарифа в Planfix", exc_info=True)

    # Платёжная система — только из настроек (DEFAULT_PAYMENT_AGENT). В отличие от
    # /api/v2/payment/init/ (app_server/routes/payments_2.py) здесь нет query-параметра
    # payment_agent: ссылка приходит из подписанной кнопки бота, и клиент не должен иметь
    # возможности подменить платёжный шлюз через URL.
    service = get_payment_service(DEFAULT_PAYMENT_AGENT)
    if service is None:
        logger.error("redirect_run: платёжная система %s не сконфигурирована", DEFAULT_PAYMENT_AGENT)
        return HTMLResponse(pages.page_error())

    try:
        payment = await service.init_payment(
            task_id=str(task.id),
            amount=tariff.price * 100,  # init_payment ожидает копейки
            description=f"Подписка: {tariff.title}",
        )
    except Exception:  # noqa: BLE001
        logger.exception("redirect_run: init_payment упал (tg=%s, tariff=%s)", telegram_id, tariff.id)
        return HTMLResponse(pages.page_error())

    return RedirectResponse(payment.confirmation_url, status_code=302)
