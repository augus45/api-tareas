from datetime import datetime, timedelta
from jose import JWTError, jwt 
from passlib.context  import  CryptContext

SECRET_KEY = "clave-secreta-muy-segura-cambiar-en-produccion"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_password(password, password_hasheado):
    return pwd_context.verify(password, password_hasheado)

def hashear_password(password):
    return pwd_context.hash(password)

def crear_token(data: dict):
    datos = data.copy()
    expira = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    datos.update({"exp": expira})
    return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
