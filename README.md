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

### 3. **Servicio de Clientes**
  Gestiona la creación y administración de clientes, asegurando la seguridad mediante el uso de tokens JWT.
   - **Principales Endpoints:**
     - `POST /customers`: Registra un nuevo cliente en la base de datos.
     - `GET /customers`: Recupera la lista completa de clientes registrados. Requiere un token JWT válido.
     - `GET /customers/ping`: Verificar la conectividad del servicio.

### 4. **Servicio de Vendedores**
  Gestiona la creación y administración de vendedores, asegurando la seguridad mediante el uso de tokens JWT.
   - **Principales Endpoints:**
     - `POST /sellers`: Registra un nuevo vendedor en la base de datos.
     - `GET /sellers`: Recupera la lista completa de vendedores registrados. Requiere un token JWT válido.
     - `GET /sellers/ping`: Verificar la conectividad del servicio.

### 5. **Servicio de Productos**
   Gestiona la creación, consulta y actualización de productos en el sistema.
   - **Principales Endpoints:**
     - `POST /products/`: Crear un nuevo producto. Requiere autenticación con un token JWT de un usuario administrador.
     - `GET /products/`: Obtener todos los productos registrados.
     - `GET /products/<product_id>`: Obtener un producto por su ID.
     - `PUT /products/<product_id>/quantity`: Actualizar la cantidad de un producto.
     - `GET /products/ping`: Verificar la conectividad del servicio.

### 6. **Servicio de Órdenes**
   Gestiona la creación, consulta y administración de órdenes en el sistema.
   - **Principales Endpoints:**
     - `POST /orders/`: Crear una nueva orden.
     - `GET /orders/<order_id>`: Obtener una orden por su ID.
     - `GET /orders/customer`: Obtener todas las órdenes asociadas a un cliente autenticado.
     - `GET /orders/ping`: Verificar la conectividad del servicio.
 
  
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

A continuación, se describen los recursos disponibles y cómo utilizarlas:

### 1. Colección y Ambientes para usar en Postman

La colección de servicios y los ambientes disponibles se encuentran en el repositorio en la carpeta ```collections``` o en los siguientes enlaces.

| **Recurso**                  | **Enlace**                                              |
|-------------------------------|------------------------------------------------------------------------|
| **Colección de los servicios**      | [Colección de los servicios](https://github.com/CCP-G18/MISW4502-ProyectoFinal2-Backend-Web/blob/253799be3062cd863df541d7dd7d831ec3e6bb95/collections/%5BMISO%5D%20Proyecto%20Final.postman_collection.json)  |
| **Ambiente Local**      | [Ambiente Local](https://github.com/CCP-G18/MISW4502-ProyectoFinal2-Backend-Web/blob/253799be3062cd863df541d7dd7d831ec3e6bb95/collections/MISO%20Proyecto%20Final%20Local.postman_environment.json)     |
| **Ambiente Productivo**      | [Ambiente Local](https://github.com/CCP-G18/MISW4502-ProyectoFinal2-Backend-Web/blob/253799be3062cd863df541d7dd7d831ec3e6bb95/collections/MISO%20Proyecto%20Final%20Production.postman_environment.json)     |

### 2. Importar una Colección en Postman

1. Descarga la colección correspondiente desde los enlaces proporcionados.2. 
3. Abre Postman y selecciona la opción **Importar**.
4. Carga el archivo `.json` de la colección descargada.

### 3. Configurar el entorno en Postman
1. Puedes utilizar dos ambientes para el consumo de los servicios, de manera local o de manera productivo. Debes escoger el archivo listado en el punto 1 y descarga el archivo de entorno de Postman.
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
| Jhon Andrés Parra        | ja.parrar12@uniandes.edu.co  |
