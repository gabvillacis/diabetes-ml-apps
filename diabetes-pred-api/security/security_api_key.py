from fastapi import Security, Depends
from fastapi.security import APIKeyHeader
from starlette.exceptions import HTTPException
from security.security_data_manager import security_data_manager
import databases
from db.database import get_database

API_KEY_NAME = "x-api-key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, scheme_name="API Key Header", auto_error=False)

async def verificar_api_key(header_param: str = Security(api_key_header), database: databases.Database = Depends(get_database)):
    if not header_param:
        raise HTTPException(status_code=401, detail="Acceso Denegado")
    elif header_param and await security_data_manager.comprobar_api_key(header_param, database):
        return header_param
    else:
        raise HTTPException(status_code=401, detail="Acceso Denegado")