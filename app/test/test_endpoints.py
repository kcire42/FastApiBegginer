import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import base
from app.database.databaseConnection import getDB
from app.main import app
# Importamos la API Key secreta para usarla en la cabecera de la prueba
from app.Api.security import api_key, verify_api_token 

# ----------------------------------------------------------------------
# 1. Configuración de la Base de Datos de Prueba (SQLite en memoria)
# ----------------------------------------------------------------------

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db" 
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ----------------------------------------------------------------------
# 2. Funciones de Sobrescritura de Dependencias
# ----------------------------------------------------------------------

# Esta función es la que reemplaza a getDB
def override_get_db_for_test():
    """Generador que provee una sesión de DB de prueba, y limpia al terminar."""
    base.metadata.create_all(bind=engine) # Crea las tablas para la prueba
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        base.metadata.drop_all(bind=engine) # Elimina las tablas después de la prueba

# NUEVA FUNCIÓN MOCKEADA: siempre devuelve True para pasar la seguridad
def mock_verify_api_token():
    """Simula la verificación de token, siempre pasando."""
    return True

# ----------------------------------------------------------------------
# 3. Inicialización del Cliente de Prueba como Fixture (¡CORRECCIÓN CLAVE!)
# ----------------------------------------------------------------------

# La selección original fue reemplazada por este fixture
@pytest.fixture(scope="function")
def client():
    """
    Fixture que crea el cliente de prueba de FastAPI y sobrescribe las dependencias
    (DB y Seguridad) para cada test, garantizando el aislamiento.
    """
    # Sobrescribir las dependencias: DB y Seguridad
    app.dependency_overrides[getDB] = override_get_db_for_test
    app.dependency_overrides[verify_api_token] = mock_verify_api_token # Mockear la seguridad
    
    # Crear el cliente de prueba
    with TestClient(app) as c:
        yield c
        
    # Limpiar las sobrescrituras al finalizar la función de prueba
    app.dependency_overrides.clear()

# ----------------------------------------------------------------------
# 4. Definición de las Pruebas
# ----------------------------------------------------------------------

customer_data = {
    "name": "Prueba",
    "description": "Cliente de prueba",
    "age": 30,
    "email": "prueba@test.com"
}
# Encabezado correcto: usa X-API-Key, no Authorization: Bearer
AUTH_HEADERS = {"X-API-Key": api_key}


def test_health_check_public(client: TestClient):
    """Prueba que el endpoint /health responde correctamente sin auth."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_customer_with_wrong_key():
    """
    Prueba que el endpoint protegido falla con una clave incorrecta (401 Unauthorized).
    Esta prueba NO usa el fixture 'client' para que la seguridad esté activa.
    """
    wrong_headers = {"X-API-Key": "clave-mala-falsa"}
    
    # Creamos un cliente temporal solo con el mock de DB, pero con la seguridad REAL
    temp_app = app
    temp_app.dependency_overrides[getDB] = override_get_db_for_test
    unauth_client = TestClient(temp_app)
    
    response = unauth_client.post("/customers/", json=customer_data, headers=wrong_headers)
    
    # Limpiamos la dependencia de DB después de usar el cliente temporal
    temp_app.dependency_overrides.clear()
    
    # verify_api_token debe devolver 401 si la clave es incorrecta
    assert response.status_code == 401
    assert "Invalid authentication credentials" in response.json()["detail"]


def test_create_and_get_customer_successful(client: TestClient):
    """
    Prueba el flujo completo: crear un cliente (con mock de auth) y luego obtenerlo.
    """
    # 1. POST (Creación con seguridad mockeada a True)
    response = client.post("/customers/", json=customer_data, headers=AUTH_HEADERS)
    assert response.status_code == 200
    created_customer = response.json()
    assert created_customer["email"] == customer_data["email"]

    # 2. GET (Recuperación de todos los clientes - protegido)
    get_all_response = client.get("/customers")
    assert get_all_response.status_code == 200
    customers = get_all_response.json()
    print("Customers retrieved:", customers)
    assert len(customers) == 1
    assert customers[0]["name"] == "Prueba"
    
    # # 3. GET (Recuperación por ID - no protegido)
    # customer_id = created_customer["id"]
    # get_id_response = client.get(f"/customers/{customer_id}")
    
    # assert get_id_response.status_code == 200
    # assert get_id_response.json()["id"] == customer_id

def test_read_root_message(client: TestClient):
    """Prueba que el endpoint / (raíz) devuelve el mensaje 'World'."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "World"}