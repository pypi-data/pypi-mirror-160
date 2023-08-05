from typing import Any
from typing_extensions import Literal

def register(viewer, order: int = ...) -> None: ...
def show(image, title: Any | None = ..., **options): ...

class Viewer:
    def show(self, image, **options): ...
    format: Any
    options: Any
    def get_format(self, image): ...
    def get_command(self, file, **options) -> None: ...
    def save_image(self, image): ...
    def show_image(self, image, **options): ...
    def show_file(self, file, **options): ...

class WindowsViewer(Viewer):
    format: str
    options: Any
    def get_command(self, file, **options): ...

class MacViewer(Viewer):
    format: str
    options: Any
    def get_command(self, file, **options): ...
    def show_file(self, file, **options): ...

class UnixViewer(Viewer):
    format: str
    options: Any
    def get_command(self, file, **options): ...
    def show_file(self, file, **options): ...

class XDGViewer(UnixViewer):
    def get_command_ex(self, file, **options) -> tuple[Literal["xdg-open"], Literal["xdg-open"]]: ...

class DisplayViewer(UnixViewer):
    def get_command_ex(self, file, title: str | None = ..., **options): ...

class GmDisplayViewer(UnixViewer):
    def get_command_ex(self, file, **options): ...

class EogViewer(UnixViewer):
    def get_command_ex(self, file, **options): ...

class XVViewer(UnixViewer):
    def get_command_ex(self, file, title: Any | None = ..., **options): ...

class IPythonViewer(Viewer):
    def show_image(self, image, **options): ...
