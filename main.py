from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from database import engine, SessionLocal
from auth import hashear_password, verificar_password, crear_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://frontend-tareas-rose.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/tareas")
def listar_tareas(db: Session = Depends(get_db)):
    return db.query(models.Tarea).all()

@app.get("/")
def hola_mundo():
    return {"mensaje": "Hola mundo"}

@app.get("/saludo/{nombre}")
def saludar(nombre: str):
    return {"mensaje": f"Hola {nombre}!"}

@app.get("/saludo/{nombre}/{apellido}")
def saludar_completo(nombre: str, apellido: str):
    return {"mensaje": f"Hola {nombre} {apellido}!"}

class TareaCreate(BaseModel):
    titulo: str
    descripcion: str
    prioridad: str = "media"
    

@app.post("/tareas")
def crear_tarea(tarea: TareaCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    nueva_tarea = models.Tarea(
        titulo=tarea.titulo,
        descripcion=tarea.descripcion,
        prioridad=tarea.prioridad
    )
    db.add(nueva_tarea)
    db.commit()
    db.refresh(nueva_tarea)
    return nueva_tarea

@app.delete("/tareas/{tarea_id}")
def eliminar_tarea(tarea_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    tarea = db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    db.delete(tarea)
    db.commit()
    return {"mensaje": "tarea borrada"}

@app.put("/tareas/{tarea_id}/completar")
def tarea_completada(tarea_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    tarea = db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    tarea.completada = True
    db.commit()
    return {"mensaje": "tarea completada con éxito"}

class TareaUpdate(BaseModel):
    titulo: str
    descripcion: str
    prioridad: str   

@app.put("/tareas/{tarea_id}")
def actualizar_tarea(tarea_id: int, datos: TareaUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    tarea = db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    tarea.titulo = datos.titulo
    tarea.descripcion = datos.descripcion
    tarea.prioridad = datos.prioridad
    db.commit()
    return {"mensaje": "tarea actualizada"}


class UsuarioCreate(BaseModel):
    email: str
    password: str

@app.post("/register")
def register(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    nuevo_usuario = models.Usuario(
        email=usuario.email,
        password=hashear_password(usuario.password)
    )
    db.add(nuevo_usuario)
    db.commit()
    return {"mensaje": "Usuario creado con éxito"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.email == form_data.username).first()
    if not db_usuario:
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
    if not verificar_password(form_data.password, db_usuario.password):
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
    token = crear_token({"sub": db_usuario.email})
    return {"access_token": token, "token_type": "bearer"}
    