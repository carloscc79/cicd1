# ==========================================
# STAGE 1: Builder (Compilación de dependencias)
# ==========================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Silenciar advertencias de debconf en compilación
ARG DEBIAN_FRONTEND=noninteractive
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar herramientas necesarias para compilar paquetes
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --no-warn-script-location --root-user-action=ignore --user -r requirements.txt

# ==========================================
# STAGE 2: Runtime (Imagen Final Ligera)
# ==========================================
FROM python:3.11-slim AS runner

WORKDIR /app

# Silenciar advertencias de debconf en compilación
ARG DEBIAN_FRONTEND=noninteractive

# Instalar solo librerías de ejecución para PostgreSQL y curl (para healthcheck en Docker)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario sin privilegios por seguridad (Hardening)
RUN useradd -m -u 10001 appuser

# Copiar dependencias desde builder hacia la carpeta HOME del appuser
COPY --from=builder /root/.local /home/appuser/.local

# Copiar código fuente
COPY src/ /app/src/

# Otorgar permisos al usuario sobre la app y sobre sus librerías instaladas
RUN chown -R appuser:appuser /app /home/appuser/.local

# Configurar el PATH señalando al HOME de appuser
ENV PATH=/home/appuser/.local/bin:$PATH

USER appuser

EXPOSE 8080

# Comando de arranque usando Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]