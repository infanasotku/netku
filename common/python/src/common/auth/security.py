from datetime import timedelta, datetime
import bcrypt
import jwt

from common.contracts.clients import SecurityClient
from common.schemas.token import TokenPayload


class PyJWTSecurityClient(SecurityClient):
    algorithm = "RS256"

    def __init__(
        self,
        public_key: str,
        private_key: str | None,
        *,
        expires_delta: timedelta | None = None,
    ):
        self.expires_delta = expires_delta or timedelta(minutes=15)
        self._private_key = private_key
        self._public_key = public_key

    def get_hash(self, source):
        encoded_source = source.encode()
        ecnoded_hash = bcrypt.hashpw(encoded_source, bcrypt.gensalt())
        return ecnoded_hash.decode()

    def verify_source(self, plain_source, hashed_source):
        return bcrypt.checkpw(plain_source.encode(), hashed_source.encode())

    def create_access_token(self, data):
        if self._private_key is None:
            raise ValueError("Private key not specified for creating token.")
        expire = datetime.now() + self.expires_delta
        return jwt.encode(
            {"exp": expire, **data}, self._private_key, algorithm=self.algorithm
        )

    def parse_access_token(self, token):
        try:
            payload: dict = jwt.decode(
                token, self._public_key, algorithms=self.algorithm
            )
        except Exception:
            return
        external_client_id = payload.get("sub")
        expire = payload.get("exp")
        if external_client_id is None:
            return
        if expire is None:
            return
        scopes: str = payload.get("scopes", "")
        return TokenPayload(
            external_client_id=external_client_id, scopes=scopes.split(), expire=expire
        )
