from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker, Session
from app.database.config import DATABASE_URL
from app.database.models import base

# Configuración del Motor (Engine) de SQLAlchemy
# create_engine es síncrono, se usará para la configuración inicial
engine = engine.create_engine(DATABASE_URL)

# Sesión Local: La usaremos para crear/gestionar las sesiones de DB.
# autocommit=False: Control manual de las transacciones (commit)
# autoflush=False: Evita que los cambios se envíen automáticamente a la DB
# bind=engine: Asocia esta SessionLocal al motor de conexión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def createDBTable():
    """Crea las tablas en la base de datos según los modelos definidos."""
    try:
        base.metadata.create_all(bind=engine)
        print("Tablas creadas exitosamente.")
    except Exception as e:
        print(f"Error al crear las tablas: {e}")

def getDB():
    """Proporciona una sesión de base de datos para las operaciones."""
    db = SessionLocal() # Crear una nueva sesión de base de datos
    try:
        yield db # Le pasa la sesión al contexto que lo llame en este caso al endpoint
    finally:
        db.close() # Asegura que la sesión se cierre después de su uso