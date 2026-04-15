from __future__ import annotations

import morepath
from nextorm import TransactionError, db_session


class App(morepath.App):
    pass


@App.setting_section(section="next")
def get_next_settings() -> dict[str, int | bool | list[type[TransactionError]]]:
    return {
        "allowed_exceptions": [],
        "immediate": False,
        "retry": 0,
        "retry_exceptions": [TransactionError],
        "serializable": False,
        "strict": False,
    }


@App.tween_factory(over=morepath.EXCVIEW)
def next_tween_factory(app, handler):
    @db_session(
        allowed_exceptions=app.settings.next.allowed_exceptions,
        immediate=app.settings.next.immediate,
        retry=app.settings.next.retry,
        retry_exceptions=app.settings.next.retry_exceptions,
        serializable=app.settings.next.serializable,
        strict=app.settings.next.strict,
    )
    def next_tween(request):
        return handler(request)

    return next_tween
