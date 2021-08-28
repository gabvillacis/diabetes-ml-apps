from fastapi import APIRouter
from pydantic import BaseModel
from security.security_data_manager import security_data_manager

class ApiKeyIn(BaseModel):
    nombre_app: str
    descripcion_app: str

class ApiKeyOut(BaseModel):
    api_key: str
    

admin_security_router = APIRouter()

@admin_security_router.post('/api-keys', response_model=ApiKeyOut, status_code=201)
def generar_nuevo_api_key(api_key_input: ApiKeyIn):
    api_key_creado = security_data_manager.crear_api_key(api_key_input.nombre_app, api_key_input.descripcion_app)
    
    return ApiKeyOut(api_key=api_key_creado)
    