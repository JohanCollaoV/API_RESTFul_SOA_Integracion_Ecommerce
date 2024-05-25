# API de Gestión de Productos

Este proyecto es una API RESTful desarrollada con Django y Django REST Framework para la gestión de productos.

## Instalación

Para instalar y ejecutar este proyecto en tu máquina local, sigue estos pasos:

1. Instala Python y pip.
2. Clona este repositorio.
3. Navega a la carpeta del proyecto y crea un entorno virtual.
4. Activa el entorno virtual y ejecuta `pip install -r requirements.txt` para instalar las dependencias.
5. Crea la base de datos ejecutando `python manage.py migrate`.
6. Opcionalmente, crea un superusuario con `python manage.py createsuperuser`.
7. Ejecuta el servidor local con `python manage.py runserver`.

## Uso de la API

Puedes utilizar la API para realizar las siguientes operaciones:

- Obtener una lista de productos.
- Crear un nuevo producto.
- Obtener detalles de un producto específico.
- Actualizar un producto existente.
- Eliminar un producto.

### Ejemplo de solicitud y respuesta

#### Obtener una lista de productos:

Para obtener una lista de todos los productos disponibles, puedes utilizar el cliente Python proporcionado. Este cliente realiza una solicitud GET al endpoint `/api/productos/` y muestra la respuesta recibida.

```bash
python cliente_api.py

El resultado esperado será una lista de productos en formato JSON, junto con los detalles de cada producto, incluyendo su código, marca, nombre, precio y fecha de creación. Aquí hay un ejemplo de cómo se vería la respuesta:

json

[
    {
        "id": 4,
        "codigo": "BOS-12345",
        "marca": "Bosch",
        "codigo_interno": "BOS-67890",
        "nombre": "Taladro Percutor Bosch",
        "precio": 89990
        "creado_en": "2024-05-22T10:00:00Z"
    },
    {
        "id": 5,
        "codigo": "HAM-67890",
        "marca": "Dewalt",
        "codigo_interno": "DEW-54321",
        "nombre": "Martillo Demoledor Dewalt",
        "precio": 120000.00,
        "creado_en": "2024-05-22T10:05:00Z"
    },
    ...
]

Cada objeto en la lista representa un producto y contiene los siguientes campos:

    id: Identificador único del producto.
    codigo: Código del producto.
    marca: Marca del producto.
    codigo_interno: Código interno del producto.
    nombre: Nombre del producto.
    precio: Precio del producto en CLP.
    creado_en: Fecha y hora de creación del producto.