from contextlib import suppress

from ..context import ctx
from ..loader import HANDLERS, logger
from ..objects.tg_objects import Update
from ..requests.get_updates import get_updates
from ..base.exceptions import StopProcessing, ExitHandler
from ..handlers.base import Handler


def execute_handler(handler: Handler):
    try:
        handler.func()
    except ExitHandler:
        pass

    if handler.exclusive:
        raise StopProcessing()


def notify_first_handlers():
    for handler in HANDLERS:
        if not handler.check_first:
            continue

        for _filter in handler.filters:
            if not _filter():
                break
        else:
            execute_handler(handler)


def notify_default_handlers():
    for handler in HANDLERS:
        if handler.check_first or handler.check_last or handler.check_after_any:
            continue

        for _filter in handler.filters:
            if not _filter():
                break
        else:
            execute_handler(handler)


def notify_last_handlers():
    for handler in HANDLERS:
        if not handler.check_last:
            continue

        for _filter in handler.filters:
            if not _filter():
                break
        else:
            execute_handler(handler)


def notify_after_any_handlers():
    for handler in HANDLERS:
        if not handler.check_after_any:
            continue

        for _filter in handler.filters:
            if not _filter():
                break
        else:
            execute_handler(handler)


def notify_handlers():
    try:
        notify_first_handlers()
        notify_default_handlers()
        notify_last_handlers()
    except StopProcessing:
        pass

    try:
        notify_after_any_handlers()
    except StopProcessing:
        pass


def process_update(update: Update) -> None:
    ctx.update = update
    notify_handlers()
    ctx.update = None


def process_updates(updates: list[Update]):
    for update in updates:
        process_update(update)


def start_polling(skip_updates: bool):
    offset = None

    if skip_updates:
        updates = get_updates(offset=offset)
        if updates:
            offset = updates[-1].update_id + 1

    while True:
        try:
            updates = get_updates(offset=offset)

            if updates:
                logger.info(updates)
                offset = updates[-1].update_id + 1
                process_updates(updates)
        except Exception as exc:
            logger.exception(exc)


def run(
        skip_updates: bool = False,
        parse_mode: str = None,
        disable_web_page_preview: bool = None,
        disable_notification: bool = None,
        protect_content: bool = None,
):
    logger.info('Starting up...')

    ctx.parse_mode = parse_mode
    ctx.disable_web_page_preview = disable_web_page_preview
    ctx.disable_notification = disable_notification
    ctx.protect_content = protect_content

    try:
        start_polling(skip_updates)
    except KeyboardInterrupt:
        logger.info('Shutting down...')
