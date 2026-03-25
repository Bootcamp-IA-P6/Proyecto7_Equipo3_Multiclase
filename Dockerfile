# Imagen base ligera con Python 3.11
FROM python:3.11-slim

# Evitar prompts interactivos durante la instalacion
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instalar uv (gestor de dependencias rapido)
RUN pip install --no-cache-dir uv

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar archivos de dependencias primero (aprovecha cache de Docker)
COPY pyproject.toml .
COPY uv.lock* .

# Instalar dependencias con uv sin instalar el proyecto en si
RUN uv sync --frozen --no-dev --no-install-project

# Copiar el codigo de la aplicacion
COPY app.py .
COPY src/ ./src/
COPY models/ ./models/

# Exponer el puerto de Streamlit
EXPOSE 8501

# Configuracion de Streamlit para produccion
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Comando de arranque
CMD ["uv", "run", "streamlit", "run", "app.py"]
