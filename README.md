# API de Tareas

API REST construida con FastAPI y SQLite para la gestión de tareas, ahora con soporte para autenticación de usuarios.

## Tecnologías
- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pytest (para pruebas automatizadas)
- JWT (JSON Web Tokens para autenticación)

## Endpoints

### Autenticación
- `POST /register` — registrar un nuevo usuario
- `POST /login` — iniciar sesión y obtener token JWT

### Tareas (Requieren Autenticación)
- `GET /tareas` — listar tareas
- `POST /tareas` — crear tarea (título, descripción, prioridad)
- `PUT /tareas/{id}` — actualizar tarea
- `PUT /tareas/{id}/completar` — marcar tarea como completada
- `DELETE /tareas/{id}` — eliminar tarea

## Cómo correrlo en local

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar la aplicación:
```bash
uvicorn main:app --reload
```

## Pruebas
Para correr los tests automatizados:
```bash
pytest test_main.py
```
