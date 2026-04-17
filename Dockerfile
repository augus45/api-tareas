FROM python:3.10-slim

# Directorio de trabajo en el contenedor
WORKDIR /app

# Copia los requerimientos y los instala
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación
COPY . .

# Expone el puerto 8000
EXPOSE 8000

# Comando para levantar uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
