from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID

from config import Settings

global_settings = Settings()

keycloak_openid = KeycloakOpenID(
    server_url=global_settings.keycloack_server_url,
    client_id=global_settings.keycloack_client_id,
    realm_name=global_settings.keycloack_realm_name,
    client_secret_key=global_settings.keycloack_client_secrect_key,
    verify=True,
)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.eroomsuite.com/auth/realms/EroomSuite/protocol/openid-connect/auth",
    tokenUrl="https://accounts.eroomsuite.com/auth/realms/EroomSuite/protocol/openid-connect/token",
    auto_error=False,
)


async def keycloack_guard(token: str = Depends(oauth2_scheme)):
    try:
        KEYCLOAK_PUBLIC_KEY = (
            "-----BEGIN PUBLIC KEY-----\n"
            + keycloak_openid.public_key()
            + "\n-----END PUBLIC KEY-----"
        )
        return keycloak_openid.decode_token(
            token,
            key=KEYCLOAK_PUBLIC_KEY,
            options={"verify_signature": True, "verify_aud": False, "exp": True},
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
