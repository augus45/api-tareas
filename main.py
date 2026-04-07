from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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
def crear_tarea(tarea: TareaCreate, db: Session = Depends(get_db)):
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
def eliminar_tarea(tarea_id: int, db: Session = Depends(get_db)):
    tarea = db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    db.delete(tarea)
    db.commit()
    return {"mensaje": "tarea borrada"}

@app.put("/tareas/{tarea_id}/completar")
def tarea_completada(tarea_id: int, db: Session = Depends(get_db)):
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
def actualizar_tarea(tarea_id: int, datos: TareaUpdate, db: Session = Depends(get_db)):
    tarea = db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    tarea.titulo = datos.titulo
    tarea.descripcion = datos.descripcion
    tarea.prioridad = datos.prioridad
    db.commit()
    return {"mensaje": "tarea actualizada"}
    