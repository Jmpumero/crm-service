import json
from enum import Enum
from typing import Any, List, Optional, Set
from urllib.request import urlopen

from fastapi import Security
from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.openapi.models import (
    OAuthFlowAuthorizationCode,
    OAuthFlowClientCredentials,
    OAuthFlowImplicit,
    OAuthFlowPassword,
)
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.openapi.models import OAuth2 as OAuth2Model
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt
from jose.exceptions import JWTError
from starlette.status import HTTP_401_UNAUTHORIZED

from config import Settings

global_settings = Settings()


class GrantType(str, Enum):
    AUTHORIZATION_CODE = "authorization_code"
    CLIENT_CREDENTIALS = "client_credentials"
    IMPLICIT = "implicit"
    PASSWORD = "password"


class OpenIDConnect(SecurityBase):
    def __init__(
        self,
        *,
        url: str,
        scheme_name: str = "OpenID Connect",
        allowed_grant_types: List[GrantType] = [GrantType.AUTHORIZATION_CODE],
        auto_error: Optional[bool] = True,
        jwt_decode_options: Optional[dict[str, str]] = None,
        audience: Optional[str] = "",
    ) -> None:
        self.scheme_name = scheme_name
        self.auto_error = auto_error
        self.jwt_decode_options = jwt_decode_options
        self.audience = audience

        self.well_known: dict[str, str] = self.get_well_known(url)
        self.jwks: dict[str, str] = self.get_jwks(self.well_known)

        grant_types: Set[str] = set(self.well_known["grant_types_supported"])
        grant_types: Set[str] = grant_types.intersection(allowed_grant_types)

        flows: OAuthFlowsModel = OAuthFlowsModel()

        authz_url: str = self.well_known["authorization_endpoint"]
        token_url: str = self.well_known["token_endpoint"]

        if GrantType.AUTHORIZATION_CODE in grant_types:
            flows.authorizationCode = OAuthFlowAuthorizationCode(
                authorizationUrl=authz_url,
                tokenUrl=token_url,
            )

        if GrantType.CLIENT_CREDENTIALS in grant_types:
            flows.clientCredentials = OAuthFlowClientCredentials(tokenUrl=token_url)

        if GrantType.PASSWORD in grant_types:
            flows.password = OAuthFlowPassword(tokenUrl=token_url)

        if GrantType.IMPLICIT in grant_types:
            flows.implicit = OAuthFlowImplicit(authorizationUrl=authz_url)

        self.model: OAuth2Model = OAuth2Model(flows=flows)

    async def __call__(self, request: Request) -> Any:
        authorization: str = request.headers.get("Authorization")
        scheme, token = get_authorization_scheme_param(authorization)

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            return None

        try:
            decode_token: Any = jwt.decode(
                token,
                self.jwks,
                audience=self.audience,
                options=self.jwt_decode_options,
            )

            return decode_token

        except JWTError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="JWT validation failed",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def get_well_known(self, issuer: str) -> dict[str, str]:
        url = f"{issuer}/.well-known/openid-configuration"

        with urlopen(url) as response:
            if response.status != 200:
                raise RuntimeError("fail to fetch well-known")

            return json.load(response)

    def get_jwks(self, well_known: dict[str, str]) -> dict[str, str]:
        url = well_known["jwks_uri"]

        with urlopen(url) as response:
            if response.status != 200:
                raise RuntimeError("fail to fetch jwks")

            return json.load(response)


allowed_grant_types = [
    GrantType.IMPLICIT,
    GrantType.AUTHORIZATION_CODE,
    GrantType.PASSWORD,
    GrantType.CLIENT_CREDENTIALS,
]

auth_scheme = OpenIDConnect(
    url=f"{global_settings.KEYCLOACK_SERVER_URL}/realms/{global_settings.KEYCLOACK_REALM_NAME}",
    scheme_name="Keycloak",
    allowed_grant_types=allowed_grant_types,
    audience="cast-master-api",
)


def keycloack_guard(claims: dict[str, str] = Security(auth_scheme)):

    return claims
