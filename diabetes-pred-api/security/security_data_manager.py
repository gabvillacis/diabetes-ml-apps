import sqlite3
import secrets
from datetime import datetime
import threading

class SecurityDataManager:
    def __init__(self):
        self.db_location = 'security.db'
        self.init_db()
    
    def init_db(self):
        with sqlite3.connect(self.db_location) as connection:
            c = connection.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS api_keys(
                          api_key TEXT PRIMARY KEY,
                          nombre_app TEXT,
                          descripcion_app TEXT,
                          fecha_creacion TEXT,
                          fecha_ultimo_req TEXT,
                          contador_req INTEGER)""")
            
            connection.commit()
            
    
    def crear_api_key(self, nombre_app: str, descripcion_app: str) -> str:
        api_key = secrets.token_urlsafe(75)        
        fecha_actual = datetime.utcnow().isoformat()
        
        with sqlite3.connect(self.db_location) as connection:
            c = connection.cursor()
            
            c.execute("""INSERT INTO api_keys(api_key, nombre_app, descripcion_app, fecha_creacion, fecha_ultimo_req, contador_req)
                            VALUES(?, ?, ?, ?, ?, ?)""", [api_key, nombre_app, descripcion_app, fecha_actual, None, 0])

            connection.commit()
            
        return api_key
    

    def comprobar_api_key(self, api_key: str) -> bool:
        with sqlite3.connect(self.db_location) as connection:
            
            c = connection.cursor()
            
            c.execute("""SELECT api_key FROM api_keys WHERE api_key = ?""", [api_key] )
            response = c.fetchone()
            
            if not response:
                return False
            else:
                threading.Thread(target=self.actualizar_uso_api_key, args=[api_key]).start()
                return True
        
            
    def actualizar_uso_api_key(self, api_key: str):
        with sqlite3.connect(self.db_location) as connection:
            c = connection.cursor()
            
            fecha_actual = datetime.utcnow().isoformat()
            
            c.execute("""UPDATE api_keys SET contador_req = contador_req + 1, fecha_ultimo_req = ? WHERE api_key = ?""",
                      [fecha_actual, api_key])
            
            connection.commit()
    
    
security_data_manager = SecurityDataManager()