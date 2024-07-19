from fastapi_users.authentication import BearerTransport

bearer_transport = BearerTransport(
    # TODO: update URL
    tokenUrl="auth/jwt/login"
)
