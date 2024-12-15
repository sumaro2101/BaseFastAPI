from .backends import authenticator


active_user = authenticator.current_user(
    active=True,
    verified=True,
)

superuser = authenticator.current_user(
    active=True,
    verified=True,
    superuser=True,
)
