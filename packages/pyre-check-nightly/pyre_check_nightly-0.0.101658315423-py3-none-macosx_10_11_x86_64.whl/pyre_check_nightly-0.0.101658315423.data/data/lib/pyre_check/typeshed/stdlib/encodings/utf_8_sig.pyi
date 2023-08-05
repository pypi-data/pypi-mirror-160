import codecs

class IncrementalEncoder(codecs.IncrementalEncoder):
    def __init__(self, errors: str = ...) -> None: ...
    def encode(self, input: str, final: bool = ...) -> bytes: ...
    def reset(self) -> None: ...
    def getstate(self) -> int: ...  # type: ignore[override]
    def setstate(self, state: int) -> None: ...  # type: ignore[override]

class IncrementalDecoder(codecs.BufferedIncrementalDecoder):
    def __init__(self, errors: str = ...) -> None: ...
    def _buffer_decode(self, input: bytes, errors: str | None, final: bool) -> tuple[str, int]: ...
    def reset(self) -> None: ...
    def getstate(self) -> tuple[bytes, int]: ...
    def setstate(self, state: tuple[bytes, int]) -> None: ...

class StreamWriter(codecs.StreamWriter):
    def reset(self) -> None: ...
    def encode(self, input: str, errors: str | None = ...) -> tuple[bytes, int]: ...

class StreamReader(codecs.StreamReader):
    def reset(self) -> None: ...
    def decode(self, input: bytes, errors: str | None = ...) -> tuple[str, int]: ...

def getregentry() -> codecs.CodecInfo: ...
def encode(input: str, errors: str | None = ...) -> tuple[bytes, int]: ...
def decode(input: bytes, errors: str | None = ...) -> tuple[str, int]: ...
