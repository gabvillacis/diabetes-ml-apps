import secrets
from datetime import datetime
from databases import Database
from db.database import get_database
from db.models import ApiKey
from sqlalchemy import select

class SecurityDataManager:
    
    async def crear_api_key(self, nombre_app: str, descripcion_app: str, db: Database = get_database()) -> str:
        api_key = secrets.token_urlsafe(75)
                
        new_apiKey = dict(
            api_key=api_key,
            nombre_app=nombre_app,
            descripcion_app=descripcion_app,
            fecha_creacion=datetime.now())
                
        await db.execute(ApiKey.insert(new_apiKey))
            
        return api_key
    

    async def comprobar_api_key(self, api_key: str, db: Database = get_database()) -> bool:
        api_key_in_db = await db.fetch_one(
            select(ApiKey.columns).where(ApiKey.c.api_key == api_key))
        if api_key_in_db is None:
            return False
        else:
            return True

    
    
security_data_manager = SecurityDataManager()