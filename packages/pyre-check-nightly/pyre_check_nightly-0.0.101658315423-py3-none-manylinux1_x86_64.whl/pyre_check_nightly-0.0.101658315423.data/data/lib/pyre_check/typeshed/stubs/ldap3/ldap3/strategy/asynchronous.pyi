from threading import Thread
from typing import Any

from ..strategy.base import BaseStrategy

class AsyncStrategy(BaseStrategy):
    class ReceiverSocketThread(Thread):
        connection: Any
        socket_size: Any
        def __init__(self, ldap_connection) -> None: ...
        def run(self) -> None: ...
    sync: bool
    no_real_dsa: bool
    pooled: bool
    can_stream: bool
    receiver: Any
    async_lock: Any
    event_lock: Any
    def __init__(self, ldap_connection) -> None: ...
    def open(self, reset_usage: bool = ..., read_server_info: bool = ...) -> None: ...
    def close(self) -> None: ...
    def set_event_for_message(self, message_id) -> None: ...
    def post_send_search(self, message_id): ...
    def post_send_single_response(self, message_id): ...
    def receiving(self) -> None: ...
    def get_stream(self) -> None: ...
    def set_stream(self, value) -> None: ...
