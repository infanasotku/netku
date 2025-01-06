from datetime import timedelta, datetime
from passlib.context import CryptContext
import jwt

from app.contracts.clients import SecurityClient
from app.schemas.client import TokenPayload


class SecurityClientImpl(SecurityClient):
    algorithm = "HS256"

    def __init__(self, secret: str, *, expires_delta: timedelta | None = None):
        self.context = CryptContext(schemes=["bcrypt"])
        self.expires_delta = expires_delta or timedelta(minutes=15)
        self.secret = secret

    def get_hash(self, source: str) -> str:
        return self.context.hash(source)

    def verify_source(self, plain_source, hashed_source):
        return self.context.verify(plain_source, hashed_source)

    def create_access_token(self, data: dict) -> str:
        expire = datetime.now() + self.expires_delta
        return jwt.encode(
            {"exp": expire, **data}, self.secret, algorithm=self.algorithm
        )

    def parse_access_token(self, token: str) -> TokenPayload:
        payload: dict = jwt.decode(token, self.secret, algorithms=self.algorithm)
        client_id = payload.get("sub")
        if client_id is None:
            raise KeyError("Missing sub in the token.")
        scopes: str = payload.get("scopes", "")
        return TokenPayload(client_id=client_id, scopes=scopes.split())
