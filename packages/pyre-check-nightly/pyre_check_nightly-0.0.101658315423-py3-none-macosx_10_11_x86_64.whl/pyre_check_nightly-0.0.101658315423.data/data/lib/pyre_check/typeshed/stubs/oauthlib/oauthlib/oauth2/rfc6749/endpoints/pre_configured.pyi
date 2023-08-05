from typing import Any

from .authorization import AuthorizationEndpoint as AuthorizationEndpoint
from .introspect import IntrospectEndpoint as IntrospectEndpoint
from .resource import ResourceEndpoint as ResourceEndpoint
from .revocation import RevocationEndpoint as RevocationEndpoint
from .token import TokenEndpoint as TokenEndpoint

class Server(AuthorizationEndpoint, IntrospectEndpoint, TokenEndpoint, ResourceEndpoint, RevocationEndpoint):
    auth_grant: Any
    implicit_grant: Any
    password_grant: Any
    credentials_grant: Any
    refresh_grant: Any
    bearer: Any
    def __init__(
        self,
        request_validator,
        token_expires_in: Any | None = ...,
        token_generator: Any | None = ...,
        refresh_token_generator: Any | None = ...,
        *args,
        **kwargs,
    ) -> None: ...

class WebApplicationServer(AuthorizationEndpoint, IntrospectEndpoint, TokenEndpoint, ResourceEndpoint, RevocationEndpoint):
    auth_grant: Any
    refresh_grant: Any
    bearer: Any
    def __init__(
        self,
        request_validator,
        token_generator: Any | None = ...,
        token_expires_in: Any | None = ...,
        refresh_token_generator: Any | None = ...,
        **kwargs,
    ) -> None: ...

class MobileApplicationServer(AuthorizationEndpoint, IntrospectEndpoint, ResourceEndpoint, RevocationEndpoint):
    implicit_grant: Any
    bearer: Any
    def __init__(
        self,
        request_validator,
        token_generator: Any | None = ...,
        token_expires_in: Any | None = ...,
        refresh_token_generator: Any | None = ...,
        **kwargs,
    ) -> None: ...

class LegacyApplicationServer(TokenEndpoint, IntrospectEndpoint, ResourceEndpoint, RevocationEndpoint):
    password_grant: Any
    refresh_grant: Any
    bearer: Any
    def __init__(
        self,
        request_validator,
        token_generator: Any | None = ...,
        token_expires_in: Any | None = ...,
        refresh_token_generator: Any | None = ...,
        **kwargs,
    ) -> None: ...

class BackendApplicationServer(TokenEndpoint, IntrospectEndpoint, ResourceEndpoint, RevocationEndpoint):
    credentials_grant: Any
    bearer: Any
    def __init__(
        self,
        request_validator,
        token_generator: Any | None = ...,
        token_expires_in: Any | None = ...,
        refresh_token_generator: Any | None = ...,
        **kwargs,
    ) -> None: ...
