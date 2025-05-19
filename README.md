# Guía de Desarrollo

Esta guía proporciona instrucciones completas para los desarrolladores que trabajan con la aplicación web de backend de CCP. Cubre la configuración del entorno, los procesos de desarrollo local, los procedimientos de prueba y los flujos de trabajo de despliegue. Para documentación específica de la API, consulta la sección correspondiente.

## Tabla de Contenidos

- [Configuración del Entorno](#configuración-del-entorno)
- [Desarrollo Local](#desarrollo-local)
- [Prácticas de Prueba](#prácticas-de-prueba)
- [Proceso de Despliegue](#proceso-de-despliegue)
- [Problemas Comunes y Solución de Problemas](#problemas-comunes-y-solución-de-problemas)

## Configuración del Entorno

Antes de comenzar el desarrollo en el backend de CCP, necesitas configurar tu entorno local con las herramientas y dependencias necesarias.

### Requisitos Previos

- Python 3.11 o superior
- Docker y Docker Compose
- Git
- PostgreSQL (para base de datos local si no se utiliza Docker)
- Postman (para pruebas de API)

### Configuración del Repositorio

1. Clona el repositorio:

   ```bash
   git clone https://github.com/CCP-G18/MISW4502-ProyectoFinal2-Backend-Web.git
   cd MISW4502-ProyectoFinal2-Backend-Web
   ```

2. Crea y activa un entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Configura las variables de entorno: Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

   ```env
   JWT_SECRET_KEY=tu_clave_secreta_jwt
   POSTGRES_DB_URI=postgresql://usuario:contraseña@localhost:5432/ccp_db
   SOCKET_SECRET_KEY=tu_clave_secreta_socket
   ```

## Desarrollo Local

### Ejecución de Servicios Localmente

Puedes ejecutar los servicios de backend directamente con Flask o utilizando Docker Compose.

#### Método 1: Usando Flask (para desarrollo)

1. Navega al directorio del servicio que deseas ejecutar, por ejemplo:

   ```bash
   cd src/orders
   ```

2. Ejecuta la aplicación:

   ```bash
   flask run
   ```

#### Método 2: Usando Docker Compose (recomendado)

1. En la raíz del proyecto, ejecuta:

   ```bash
   docker-compose up --build
   ```

   Esto construirá e iniciará todos los servicios definidos en el archivo `docker-compose.yml`.

### Arquitectura de Microservicios

El backend está estructurado como una colección de microservicios independientes, cada uno responsable de un dominio específico de la aplicación.

### Estructura del Servicio

Cada microservicio sigue una estructura similar para mantener la coherencia en la base de código:

```
src/[nombre_servicio]/
├── app/
│   ├── controllers/       # Endpoints HTTP
│   ├── models/            # Modelos de datos
│   ├── repositories/      # Operaciones de base de datos
│   ├── services/          # Lógica de negocio
│   ├── schemas/           # Serialización/deserialización
│   ├── core/              # Configuración
│   └── extensions.py      # Extensiones de Flask
├── tests/
│   ├── unit/              # Pruebas unitarias
│   └── integration/       # Pruebas de integración
├── Dockerfile             # Definición del contenedor
├── requirements.txt       # Dependencias
├── version                # Número de versión del servicio
└── main.py                # Punto de entrada de la aplicación
```

## Pruebas

### Ejecución de Pruebas

La base de código utiliza `pytest` para las pruebas. Para ejecutar las pruebas de un servicio específico:

1. Navega al directorio del servicio, por ejemplo:

   ```bash
   cd src/orders
   ```

2. Ejecuta las pruebas:

   ```bash
   pytest --cov=app tests/
   ```

### Requisitos de Cobertura

La canalización de integración continua (CI) impone una cobertura mínima de código del 70% para todos los servicios. Esto se verifica automáticamente en cada solicitud de extracción (pull request).

## Proceso de Despliegue

1. Visión General del Despliegue Continuo

   El sistema backend utiliza un flujo de trabajo de GitHub Actions que despliega automáticamente los microservicios cuando se realiza un push al branch principal. Este flujo de trabajo detecta dinámicamente todos los microservicios en el repositorio, construye las imágenes Docker y las despliega en Google Kubernetes Engine (GKE).

2. Proceso de Descubrimiento de Servicios

   La canalización CI/CD identifica automáticamente los microservicios desplegables escaneando la estructura del repositorio en busca de directorios que contengan archivos Dockerfile:

   ```bash
   find src -mindepth 1 -maxdepth 1 -type d -exec test -f "{}/Dockerfile" \; -print
   ```
   Este enfoque permite que nuevos microservicios se incluyan automáticamente en el proceso de despliegue sin modificar la configuración del flujo de trabajo.

3. Construcción y Publicación de Imágenes Docker

   Cada microservicio incluye un archivo de versión que contiene su número de versión semántica. Esta versión se utiliza para etiquetar las imágenes Docker durante el proceso de construcción.

   El flujo de trabajo CI/CD realiza los siguientes pasos para cada servicio:

   1. Lee el número de versión desde el archivo de versión del servicio.
   2. Construye una imagen Docker con etiquetas de versión específica y "latest".
   3. Publica ambas etiquetas en Google Cloud Artifact Registry.

4. Estructura de Despliegue en Kubernetes

   El sistema despliega cada microservicio como un Deployment separado en Kubernetes, con recursos asociados de Service y BackendConfig.

   Cada despliegue de servicio consta de tres recursos clave de Kubernetes:

   1. Deployment: Define la especificación del contenedor, límites de recursos, variables de entorno y conteo de réplicas.
   2. Service: Expone el despliegue internamente y al balanceador de carga.
   3. BackendConfig: Configura las verificaciones de salud y otras configuraciones del balanceador de carga.

5. Componentes de Configuración de Despliegue
   1. La configuración de despliegue de cada microservicio especifica:
      - Límites de recursos (CPU y memoria)
      - Variables de entorno (incluyendo conexión a la base de datos, claves JWT, etc.)
      - Referencia de la imagen del contenedor
      - Configuración de puertos

      Variables de entorno clave se obtienen de secretos de Kubernetes:

      - POSTGRES_DB_URI: Cadena de conexión a la base de datos
      - JWT_SECRET_KEY: Clave de firma de tokens de autenticación
      - ALLOWED_ORIGINS: Configuración de CORS
      - PATH_API_USER: Ruta al servicio de API de usuarios
      - PATH_API_BASE: Ruta base de la API

   2. Configuración de Service
      Los servicios exponen cada despliegue al clúster de Kubernetes y configuran cómo se accede a ellos internamente y a través del balanceador de carga.
   3. Configuración de BackendConfig
      El recurso BackendConfig configura aspectos adicionales del balanceador de carga, como las verificaciones de salud, para garantizar que solo las instancias saludables reciban tráfico.


El recurso BackendConfig configura aspectos adicionales del balanceador de carga, como las verificaciones de salud, para garantizar que solo las instancias saludables reciban tráfico.

## Problemas Comunes y Solución de Problemas

- **Error de conexión a la base de datos**: Verifica que PostgreSQL esté en ejecución y que las credenciales en el archivo `.env` sean correctas.

- **Problemas al instalar dependencias**: Asegúrate de estar utilizando la versión correcta de Python y de que el entorno virtual esté activado.

- **Errores al ejecutar Docker Compose**: Verifica que Docker esté instalado y en ejecución. Revisa los logs para identificar problemas específicos.