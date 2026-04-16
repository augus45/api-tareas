import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, get_db
from database import Base
import models
from auth import get_current_user

from sqlalchemy.pool import StaticPool

# Usar una base de datos en memoria para no afectar los datos reales durante las pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sobrescribir la dependencia de base de datos
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Sobrescribir la dependencia del usuario (para evitar tener que generar tokens)
def override_get_current_user():
    return {"sub": "test@example.com"}

app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    # Crear las tablas antes de cada test
    Base.metadata.create_all(bind=engine)
    yield
    # Eliminar las tablas después de cada test para tener un estado limpio
    Base.metadata.drop_all(bind=engine)

def test_hola_mundo():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mensaje": "Hola mundo"}

def test_saludar():
    response = client.get("/saludo/Juan")
    assert response.status_code == 200
    assert response.json() == {"mensaje": "Hola Juan!"}

def test_saludar_completo():
    response = client.get("/saludo/Juan/Perez")
    assert response.status_code == 200
    assert response.json() == {"mensaje": "Hola Juan Perez!"}

def test_listar_tareas_vacio():
    response = client.get("/tareas")
    assert response.status_code == 200
    assert response.json() == []

def test_crear_tarea():
    payload = {
        "titulo": "Comprar pan",
        "descripcion": "Pan francés para la cena",
        "prioridad": "alta"
    }
    response = client.post("/tareas", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == "Comprar pan"
    assert data["descripcion"] == "Pan francés para la cena"
    assert data["prioridad"] == "alta"
    assert data["completada"] == False
    assert "id" in data

def test_eliminar_tarea_existente():
    # Primero creamos una tarea
    respuesta_crear = client.post("/tareas", json={"titulo": "A", "descripcion": "B", "prioridad": "baja"})
    tarea_id = respuesta_crear.json()["id"]
    
    # Luego la eliminamos
    respuesta_eliminar = client.delete(f"/tareas/{tarea_id}")
    assert respuesta_eliminar.status_code == 200
    assert respuesta_eliminar.json() == {"mensaje": "tarea borrada"}
    
    # Comprobamos que ya no existe
    respuesta_listar = client.get("/tareas")
    assert len(respuesta_listar.json()) == 0

def test_eliminar_tarea_no_existente():
    response = client.delete("/tareas/999")
    assert response.status_code == 404

def test_completar_tarea():
    # Creamos una tarea
    respuesta_crear = client.post("/tareas", json={"titulo": "Test Completar", "descripcion": "A", "prioridad": "media"})
    tarea_id = respuesta_crear.json()["id"]
    
    # La marcamos como completada
    respuesta_completar = client.put(f"/tareas/{tarea_id}/completar")
    assert respuesta_completar.status_code == 200
    
    # Comprobamos que se marcó correctamente
    respuesta_listar = client.get("/tareas")
    tareas = respuesta_listar.json()
    assert len(tareas) == 1
    assert tareas[0]["id"] == tarea_id
    assert tareas[0]["completada"] is True

def test_actualizar_tarea():
    # Creamos una tarea
    respuesta_crear = client.post("/tareas", json={"titulo": "Viejo Titulo", "descripcion": "C", "prioridad": "baja"})
    tarea_id = respuesta_crear.json()["id"]
    
    # La actualizamos
    payload_actualizado = {
        "titulo": "Nuevo Titulo",
        "descripcion": "Nueva descripcion",
        "prioridad": "alta"
    }
    respuesta_actualizar = client.put(f"/tareas/{tarea_id}", json=payload_actualizado)
    assert respuesta_actualizar.status_code == 200
    
    # Comprobamos
    respuesta_listar = client.get("/tareas")
    tareas = respuesta_listar.json()
    assert tareas[0]["titulo"] == "Nuevo Titulo"
    assert tareas[0]["prioridad"] == "alta"
