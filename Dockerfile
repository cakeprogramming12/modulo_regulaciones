# Usa una imagen base de Python
FROM python:3.9-slim

# Evita el buffering en la salida
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requerimientos y luego instálalos
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el resto de la aplicación
COPY . /app/

# Expone el puerto 8000
EXPOSE 8000

# Ejecuta las migraciones y levanta el servidor
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
