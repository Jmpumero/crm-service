import json
from fastapi import Security

from jose import JWTError, jwt, JWSError, jws

from fastapi.security.api_key import APIKeyHeader

from redis import Redis


from error_handlers.unauthorized import UnauthorizedException
from error_handlers.bad_gateway import BadGatewayException

import main

from config.config import Settings

global_settings = Settings()
error_message = "You don't have Permission"

api_key_name = (
    Redis(host="localhost", port=6379, db=0, decode_responses=True).get("API_KEY_NAME")
    or ""
)

api_key_in_header = APIKeyHeader(name=api_key_name, auto_error=False)


async def get_api_key(
    api_key_in_header: str = Security(api_key_in_header),
):
    api_key_in_redis_raw: str = await main.app.state.redis_repo.get("API_KEYS")
    
    api_key_in_redis_filtered = list(filter(lambda key: (key["api_key"] == api_key_in_header), 
                                                         json.loads(api_key_in_redis_raw)))
    
    app_name_in_header = await get_current_user(api_key_in_header)
    
    app_name_in_redis = jwt.decode(api_key_in_redis_filtered[0]['api_key'], 
                                   global_settings.jwt_secret, 
                                   algorithms=[global_settings.jwt_algorithm]).get('aplication_name')
    
    if app_name_in_header == app_name_in_redis:
        return app_name_in_header
    else:
        raise UnauthorizedException(message=error_message)

async def get_current_user(token: str):
        try:
            username = await verify_token(token)
            return username.get('aplication_name')
        except:
            raise UnauthorizedException(message=error_message)
    

async def verify_token(token:str):
    try:
        jws.verify(token, global_settings.jwt_secret, algorithms=[global_settings.jwt_algorithm])
        payload = jwt.decode(token, global_settings.jwt_secret, algorithms=[global_settings.jwt_algorithm])
        return payload            
    except JWSError:
        raise UnauthorizedException(message=error_message)
    except JWTError:
        raise UnauthorizedException(message=error_message)
    except:
        raise BadGatewayException(message="Internal Server Error")