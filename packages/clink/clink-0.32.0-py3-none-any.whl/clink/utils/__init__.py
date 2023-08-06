import asyncio

from . import decorators, functional, participants, sentry


__all__ = ["maybe_list", "method_decorator"]


consumer_listeners_table = participants.consumer_listeners_table

maybe_list = functional.maybe_list

method_decorator = decorators.method_decorator

set_scope_tags = sentry.set_scope_tags


def get_running_loop() -> asyncio.AbstractEventLoop:  # pragma: no cover
    if hasattr(asyncio, "get_running_loop"):
        return asyncio.get_running_loop()  # type: ignore[attr-defined]
    else:  # Python 3.6
        return asyncio.get_event_loop()
