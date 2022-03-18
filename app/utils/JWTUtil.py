import jwt
import pem

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.dsa import DSAPublicKey
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from fastapi import HTTPException
from jwt import ExpiredSignatureError, InvalidSignatureError
from pem import PublicKey, AbstractPEMObject

from app.Config import Config


class JWTUtil:
    def __init__(self):
        self.env = Config()

    def verify_jwt(self, token: str) -> bool:
        return bool(self.decode_jwt(token))

    def decode_jwt(self, token: str) -> dict:
        try:
            header_data = jwt.get_unverified_header(token)
            decoded_token = jwt.decode(jwt=token, key=self.public_key, algorithms=[header_data['alg']])
            jwt.get_unverified_header(token)
            return decoded_token
        except ExpiredSignatureError as error:
            raise HTTPException(status_code=403, detail=str(error))
        except InvalidSignatureError as e:
            raise HTTPException(status_code=403, detail=str(e))

    @property
    def public_key(self) -> RSAPublicKey:
        public_key = open(self.env.public_key_path, 'r').read()
        return serialization.load_ssh_public_key(data=public_key.encode())
