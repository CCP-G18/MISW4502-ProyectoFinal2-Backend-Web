# Backend - Aplicación Web CCP

Este repositorio contiene el backend de la aplicación web para la compañía comercializadora de productos **CCP**. La aplicación está diseñada para gestionar las funcionalidades de **compra**, **venta** y **logística** de productos de consumo masivo, con presencia en varios países y operaciones en múltiples bodegas.

## Funcionalidades

CCP es una empresa dedicada a la distribución y venta de productos de consumo masivo en más de 5 países. El sistema está orientado a optimizar las operaciones comerciales, de ventas y logística de la compañía, asegurando un control eficiente de inventarios, pedidos y rutas de entrega, con un enfoque en la mejora continua del servicio al cliente.

El backend proporciona las siguientes funcionalidades principales:

- **Compra de productos**: Gestión de registros de fabricantes y productos, optimización de compras y coordinación con el inventario.
- **Ventas**: Gestión de pedidos, vendedores, clientes y cotizaciones.
- **Logística**: Gestión de rutas de entrega, inventarios en tiempo real y optimización de procesos en bodegas.

## Servicios del Proyecto

El proyecto está compuesto por varios servicios independientes que trabajan en conjunto para proporcionar las funcionalidades principales. A continuación, se describen brevemente:

### 1. **Servicio de Usuarios**
   Gestiona la creación, consulta, actualización y autenticación de usuarios en el sistema.
   - **Principales Endpoints:**
     - `POST /users/`: Crear un nuevo usuario.
     - `GET /users/`: Obtener todos los usuarios.
     - `GET /users/<id>`: Obtener un usuario por ID.
     - `PATCH /users/`: Actualizar el estado de un usuario.
     - `GET /users/ping`: Verificar la conectividad del servicio.

### 2. **Servicio de Autenticación**
   Maneja el inicio de sesión y la verificación de usuarios mediante tokens JWT.
   - **Principales Endpoints:**
     - `POST /login`: Iniciar sesión y obtener un token JWT.
     - `GET /verify`: Verificar la validez del token JWT y el estado del usuario.
    
## Despliegue de los servicios

### 1. Despliegue Local
Para ejecutar el servicio de usuarios en tu máquina local, sigue estos pasos:

#### 1.1 Clonar el repositorio:
```bash
git clone https://github.com/CCP-G18/MISW4502-ProyectoFinal2-Backend-Web.git
cd MISW4502-ProyectoFinal2-Backend-Web
```

#### 1.2 Crear un entorno virtual de Python:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

#### 1.3 Instalar las dependencias:
```bash
pip install -r requirements.txt
```

#### 1.4 Configurar las variables de entorno: 
Crea un archivo .env en la raíz del proyecto y configura correctamente las variables necesarias, como JWT_SECRET_KEY y las conexiones a la base de datos.

#### 1.5 Iniciar el servidor:
```bash
flask run
```

El servicio estará disponible en http://localhost:5000. 

### 2. Despliegue con Docker

Para ejecutar el servicio utilizando Docker (asegurarse de tener docker instalado), sigue estos pasos:

#### 2.1 Construir y levantar los contenedores
Ejecuta el siguiente comando en la raíz del proyecto para construir y levantar los servicios definidos en el archivo docker-compose.yml:
  ```bash
  docker-compose up --build
  ```

#### 2.2 Verificar que el servicio está corriendo
Una vez que los contenedores estén en ejecución, el servicio estará disponible en: http://localhost:5000

#### 2.4 Construir y levantar los contenedores
Para detener los contenedores y liberar los recursos, ejecuta:
  ```bash
  docker-compose down
  ```
## Ejecución de Tests

### 1. Ejecutar los tests
Para ejecutar los tests, utiliza el siguiente comando en la raíz del proyecto:
  ```bash
  pytest
   ```

### 2. Generar reporte de cobertura de código 
Para verificar la cobertura de código, utiliza los siguientes comandos:
  ```bash
  coverage run -m pytest
  coverage report -m
  coverage html
  ```

## Documentación de API (Colecciones de Postman)

Cada servicio del backend tiene su propia colección de Postman para facilitar las pruebas y el uso de los endpoints. A continuación, se describen las colecciones disponibles y cómo utilizarlas:

### 1. Colecciones de Postman por Servicio

| **Servicio**                  | **Enlace a la Colección**                                              |
|-------------------------------|------------------------------------------------------------------------|
| **Servicio de Usuarios**      | [Colección de Usuarios](https://uniandes-my.sharepoint.com/:u:/g/personal/ja_parrar12_uniandes_edu_co/Eb7SZvuf0DlMicGvcv9OJscBa58NhxP9wuE1kIWuz16Szw?e=mOZnvi)     |
| **Servicio de Autenticación** | [Colección de Autenticación](https://uniandes-my.sharepoint.com/personal/ja_parrar12_uniandes_edu_co/_layouts/15/download.aspx?UniqueId=ac08fdbdd0fe49f68912ac038082604f&e=z9VEkF)|

### 2. Importar una Colección en Postman

1. Descarga la colección correspondiente desde los enlaces proporcionados.2. 
3. Abre Postman y selecciona la opción **Importar**.
4. Carga el archivo `.json` de la colección descargada.

### 3. Configurar el entorno en Postman
1. Descarga el archivo de entorno de Postman desde el siguiente enlace: [Entorno de Postman](https://uniandes-my.sharepoint.com/:u:/g/personal/ja_parrar12_uniandes_edu_co/EejSz_pXINVAq0nN778OMRgBv2Q8hNz7QR2Se7GRaZ4ohg?e=LmOP5C)
2. Importa el archivo de entorno en Postman desde la pestaña **Environments**.

### 4. Probar los endpoints
- Usa los endpoints disponibles en la colección para realizar pruebas.
- Asegúrate de iniciar sesión primero para obtener el token JWT y almacenarlo en la variable `jwt_token`

## Colaboradores

| **Nombre**               | **Correo Electrónico**       |
|--------------------------|------------------------------|
| Jeniffer Corredor        | j.corredore@uniandes.edu.co  | 
| Juan Diego García        | j.garcia55@uniandes.edu.co   |
| Brayan Ricardo García    | br.garciam1@uniandes.edu.co  |
| Jhon Andrés Parra        |  ja.parrar12@uniandes.edu.co |
