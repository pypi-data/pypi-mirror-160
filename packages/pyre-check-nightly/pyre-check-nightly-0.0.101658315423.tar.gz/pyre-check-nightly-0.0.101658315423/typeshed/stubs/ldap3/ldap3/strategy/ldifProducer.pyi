from typing import Any

from .base import BaseStrategy

class LdifProducerStrategy(BaseStrategy):
    sync: bool
    no_real_dsa: bool
    pooled: bool
    can_stream: bool
    line_separator: Any
    all_base64: bool
    stream: Any
    order: Any
    def __init__(self, ldap_connection) -> None: ...
    def receiving(self) -> None: ...
    def send(self, message_type, request, controls: Any | None = ...): ...
    def post_send_single_response(self, message_id): ...
    def post_send_search(self, message_id) -> None: ...
    def accumulate_stream(self, fragment) -> None: ...
    def get_stream(self): ...
    def set_stream(self, value) -> None: ...
