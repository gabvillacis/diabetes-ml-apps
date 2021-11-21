from sqlalchemy import Table, MetaData, Column, String, DateTime

metadata = MetaData()

ApiKey = Table(
    'api_keys', metadata,
    Column('api_key', String(100), primary_key=True),
    Column('nombre_app', String(100), nullable=False),
    Column('descripcion_app', String(200), nullable=False),
    Column('fecha_creacion', DateTime)
)