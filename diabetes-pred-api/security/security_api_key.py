from fastapi import Security
from fastapi.security import APIKeyHeader
from starlette.exceptions import HTTPException
from security.security_data_manager import security_data_manager

API_KEY_NAME = "x-api-key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, scheme_name="API Key Header", auto_error=False)

def verificar_api_key(header_param: str = Security(api_key_header)):
    if not header_param:
        raise HTTPException(status_code=401, detail="Acceso Denegado")
    elif header_param and security_data_manager.comprobar_api_key(header_param):
        return header_param
    else:
        raise HTTPException(status_code=401, detail="Acceso Denegado")