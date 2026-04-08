# API de Tareas

API REST construida con FastAPI y SQLite.

## Tecnologías
- Python
- FastAPI
- SQLAlchemy
- SQLite

## Endpoints
- GET /tareas — listar tareas
- POST /tareas — crear tarea
- PUT /tareas/{id} — actualizar tarea
- PUT /tareas/{id}/completar — marcar como completada
- DELETE /tareas/{id} — eliminar tarea

## Cómo correrlo
pip install fastapi uvicorn sqlalchemy
uvicorn main:app --reload
