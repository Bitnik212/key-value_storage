import datetime
from urllib.parse import urlparse
from typing import Any

import jwt

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from fastapi import HTTPException
from jwt import ExpiredSignatureError, InvalidSignatureError, InvalidTokenError, InvalidIssuerError

from app.ServerConfig import ServerConfig


class JWTUtil:
    HEADER_ALG_NAME = "alg"
    DATA_EXPIRATION_NAME = "exp"
    DATA_ISSUER_NAME = "iss"
    ALL_HOSTS = "*"

    def __init__(self):
        self.env = ServerConfig()

    @property
    def public_key(self) -> RSAPublicKey:
        public_key = open(self.env.public_key_path, 'r').read()
        return serialization.load_ssh_public_key(data=public_key.encode())

    def verify_jwt(self, token: str) -> bool:
        return bool(self.decode_jwt(token))

    def decode_jwt(self, token: str) -> dict:
        try:
            header_data = jwt.get_unverified_header(token)
            decoded_token = jwt.decode(jwt=token, key=self.public_key, algorithms=[header_data[self.HEADER_ALG_NAME]])
            self.check_expiration(decoded_token)
            self.check_allowed_issuer(decoded_token)
            return decoded_token
        except ExpiredSignatureError as e:
            raise HTTPException(status_code=403, detail=str(e))
        except InvalidSignatureError as e:
            raise HTTPException(status_code=403, detail=str(e))
        except InvalidIssuerError as e:
            raise HTTPException(status_code=403, detail=str(e))
        except InvalidTokenError as e:
            raise HTTPException(status_code=403, detail=str(e))

    def is_expired(self, token: dict[str, Any]) -> bool:
        exp_timestamp = int(token[self.DATA_EXPIRATION_NAME]) / 1000
        exp_datetime = datetime.datetime.fromtimestamp(exp_timestamp)
        now = datetime.datetime.now()
        return exp_datetime <= now

    def check_expiration(self, token: dict[str, Any]):
        if self.is_expired(token):
            raise InvalidTokenError("Token expired")

    def check_allowed_issuer(self, token: dict[str, Any]):
        if not self.is_allowed_issuer(token):
            raise InvalidIssuerError("Issuer not in allowed list")

    def is_allowed_issuer(self, token: dict[str, Any]) -> bool:
        issuer = str(token[self.DATA_ISSUER_NAME])
        issuer = urlparse(url=issuer)
        issuer_hostname = issuer.netloc
        if issuer_hostname in self.env.jwt_allowed_issuer_hosts or self.ALL_HOSTS in self.env.jwt_allowed_issuer_hosts:
            return True
        else:
            for hostname in self.env.jwt_allowed_issuer_hosts:
                if self.ALL_HOSTS in hostname:
                    hostname_splited = hostname.split(".")
                    if self.ALL_HOSTS in hostname_splited and len(hostname_splited) >= 3:
                        return self.__check_wildcard(wildcard=hostname, hostname=issuer_hostname)

    def __check_wildcard(self, wildcard: str, hostname: str) -> bool:
        """
        Проверка на то входит ли домен в разрешенную зону.
        :param wildcard: разрешенная зона.
        :param hostname: домен.
        """
        correct = False
        splited_wildcard = wildcard.split(".")
        splited_hostname = hostname.split(".")
        wildcard_index = splited_wildcard.index(self.ALL_HOSTS)
        if len(splited_wildcard) == len(splited_hostname):
            correct_count = 0
            for i in splited_wildcard[wildcard_index+1:]:
                if splited_hostname.index(i) == splited_wildcard.index(i):
                    correct_count += 1
            if correct_count == len(splited_wildcard[wildcard_index+1:]):
                correct = True
        return correct
