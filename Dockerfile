# Base image (Forzar arquitectura AMD64 en Mac M1/M2)
FROM --platform=linux/amd64 python:3.10-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 

# Instalar herramientas necesarias
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    curl \
    apt-transport-https \
    gnupg \
    gcc \
    build-essential 

# Agregar la clave de Microsoft
RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

# Agregar el repositorio de Microsoft
RUN curl -sSL https://packages.microsoft.com/config/debian/11/prod.list | tee /etc/apt/sources.list.d/mssql-release.list

# Instalar los paquetes de Microsoft correctamente
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools

# Agregar herramientas de SQL al PATH
ENV PATH="/opt/mssql-tools/bin:$PATH"

# Crear directorio de la aplicación
WORKDIR /app

# Copiar dependencias y código
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Exponer el puerto
EXPOSE 8000

# Iniciar el servidor
CMD ["python3", "app.py"]
