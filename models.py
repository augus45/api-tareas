from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Tarea(Base):
    __tablename__="tareas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    descripcion = Column(String)
    completada = Column(Boolean, default=False)
    prioridad = Column(String, default="media")

