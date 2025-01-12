from datetime import timedelta, datetime
import bcrypt
import jwt

from app.contracts.clients import SecurityClient
from app.schemas.token import TokenPayload


class SecurityClientImpl(SecurityClient):
    algorithm = "HS256"

    def __init__(self, secret: str, *, expires_delta: timedelta | None = None):
        self.expires_delta = expires_delta or timedelta(minutes=15)
        self.secret = secret

    def get_hash(self, source):
        encoded_source = source.encode()
        ecnoded_hash = bcrypt.hashpw(encoded_source, bcrypt.gensalt())
        return ecnoded_hash.decode()

    def verify_source(self, plain_source, hashed_source):
        return bcrypt.checkpw(plain_source.encode(), hashed_source.encode())

    def create_access_token(self, data):
        expire = datetime.now() + self.expires_delta
        return jwt.encode(
            {"exp": expire, **data}, self.secret, algorithm=self.algorithm
        )

    def parse_access_token(self, token):
        try:
            payload: dict = jwt.decode(token, self.secret, algorithms=self.algorithm)
        except Exception:
            return
        client_id = payload.get("sub")
        expire = payload.get("exp")
        if client_id is None:
            return
        if expire is None:
            return
        scopes: str = payload.get("scopes", "")
        return TokenPayload(client_id=client_id, scopes=scopes.split(), expire=expire)
