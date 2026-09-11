**Demostrador de Pipeline CI/CD con DevSecOps**



Proyecto de referencia y estándar reutilizable para la automatización, empaquetado seguro y despliegue de microservicios con Docker, Ansible y Forgejo Actions.



**Arquitectura del Sistema**



El proyecto implementa una arquitectura desacoplada de microservicio con persistencia de datos localizada en el host.



              +-------------------------------------------------------+

              |                  HOST (Servidor App)                  |

              |                                                       |

              |   +-------------------+       +-------------------+   |

              |   |   demo_web        |       |   demo_postgres   |   |

              |   |   (FastAPI)       |------>|   (PostgreSQL 15) |   |

              |   |   Port: 8080      | Net   |   Port: 5432      |   |

              |   +-------------------+       +-------------------+   |

              |             |                           |             |

              +-------------|---------------------------|-------------+

                            |                           |

                      HTTP (Port 8080)             Bind Mount

                            |               (/opt/demo-app/data/postgres)

                            v                           |

                    [Cliente / Nginx]                   v

                                               [Disco del Host]

**Componentes y Estructura del Repositorio**



**demo-cicd-pipeline/**

├── app/                        # Código fuente del microservicio

│   ├── src/                    # Aplicación FastAPI

│   ├── Dockerfile              # Build Multi-Stage optimizado y hardened

│   └── requirements.txt        # Dependencias de Python

├── infra/                      # Infraestructura como Código (IaC)

│   └── ansible/

│       ├── inventory.ini       # Inventario parametrizado para local/remoto

│       ├── playbook.yml        # Playbook de despliegue idempotente

│       └── templates/

│           ├── docker-compose.yml.j2 # Plantilla Jinja2 del stack de servicios

│           └── env.j2                # Plantilla Jinja2 de variables de entorno

└── .forgejo/

   └── workflows/              # Definición de pipelines de CI/CD

       └── deploy.yml



**Estándares y Prácticas de Seguridad Implementadas**



1. Compilación Multi-Stage en Docker: Separación estricta entre la etapa de Build (compiladores, cabeceras) y la etapa de Runtime (solo dependencias mínimas de ejecución).

2. Ejecución como Usuario No Privilegiado (Non-root): La aplicación se ejecuta bajo el usuario appuser (UID 10001), evitando la ejecución con permisos de root dentro del contenedor.

3. Imágenes Ligeras: Uso de imágenes base python:3.11-slim y postgres:15-alpine para reducir la superficie de ataque y optimizar tiempos de descarga.

4. Idempotencia y Gestión de Secretos: Ansible gestiona el aprovisionamiento de las carpetas de datos y la generación restringida (permisos 0600) del archivo .env.

5. Persistencia de Datos: Uso de Bind Mounts en la ruta explícita /opt/demo-app/data/postgres para preservar los datos de la base de datos ante reinicios o despliegues.



**Guía de Ejecución Local (Desarrollo y Pruebas)**



**Requisitos Previos**



* WSL 2 (Ubuntu/Debian) o Linux Native.
* Docker Engine / Docker Compose.
* Ansible (ansible-playbook).



**Pasos para Despliegue Local**



1. **Compilar la imagen localmente:**



docker build -t desarrollo/demo-app:local ./app



**2. Definir variables de entorno temporales:**



export IMAGE_TAG="local"

export DB_PASSWORD="secret_password_test"

export REGISTRY_URL="docker.io"

export IMAGE_NAME="desarrollo/demo-app"



**3. Ejecutar el despliegue con Ansible:**



ansible-playbook -i infra/ansible/inventory.ini infra/ansible/playbook.yml \

&#x20; --extra-vars "image_tag=$IMAGE_TAG db_password=$DB_PASSWORD registry_url=$REGISTRY_URL image_name=$IMAGE_NAME" \

&#x20; -c local



**4. Validar el estado del servicio (Smoke Test):**



# Estado de contenedores

docker ps



# Verificación de salud

curl -i http://localhost:8080/health



**Interfaz e Inspección**



Una vez desplegada la aplicación, se puede acceder a las siguientes interfaces interactivas:

* Documentación interactiva (Swagger UI): http://localhost:8080/docs
* Especificación ReDoc: http://localhost:8080/redoc
* Endpoint de verificación de salud: http://localhost:8080/health



**Variables de Entorno y Secretos para CI/CD (Forgejo)**



Para el despliegue automatizado desde el pipeline de Forgejo, se deben configurar los siguientes Secretos del Repositorio:



**Nombre del Secreto		Descripción**

APP_DOMAIN			Dirección IP o FQDN del servidor de destino.

SSH_PRIVATE_KEY			Clave privada SSH autorizada en el servidor remoto.

REGISTRY_TOKEN			Token de acceso para autenticación y subida de imágenes.

DB_PASSWORD			Contraseña asignada a PostgreSQL en producción.

