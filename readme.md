Esta API RESTful está desarrollada con Django y Django REST Framework para ofrecer una solución robusta y escalable para la gestión de productos. Está diseñada con una arquitectura orientada a servicios (SOA), lo que facilita la integración y modularidad de los distintos componentes del sistema.

Características

    Arquitectura SOA: Organiza el sistema en servicios independientes para promover la reutilización y escalabilidad.
    Django REST Framework: Utiliza esta poderosa biblioteca para la creación de APIs, facilitando el desarrollo y la administración de endpoints.
    Pruebas con Pytest: Implementa pruebas unitarias y de integración utilizando Pytest para asegurar la calidad y estabilidad del código.
    
Instalación
Para instalar y ejecutar este proyecto en tu máquina local, sigue estos pasos:

Instala Python y pip.
Clona este repositorio usando el comando git clone <URL_del_repositorio>.
Navega a la carpeta del proyecto y crea un entorno virtual usando el comando python -m venv venv en Windows o python3 -m venv venv en sistemas basados en Unix.
Activa el entorno virtual. En Windows, ejecuta venv\Scripts\activate y en sistemas basados en Unix ejecuta source venv/bin/activate.
Ejecuta el comando pip install -r requirements.txt para instalar las dependencias.
Crea la base de datos ejecutando python manage.py migrate.
Opcionalmente, crea un superusuario con python manage.py createsuperuser.
Ejecuta el servidor local con python manage.py runserver.

Uso de la API
Puedes utilizar las APIs para realizar las siguientes operaciones:

Obtener una lista de productos.
Crear un nuevo producto.
Obtener un producto por ID.
Crear un usuario
Iniciar Sesion
Agregar un producto al Carro de comprar una vez iniciada Sesion
Se puede Pagar el carro



Para consultar la Documentacion de la API ir al siguiente LINK :
https://documenter.getpostman.com/view/16268230/2sA3Qs8Wsz
