import requests

URL_BASE = 'http://localhost:8000/api/productos/'

def obtener_productos():
    respuesta = requests.get(URL_BASE)
    if respuesta.status_code == 200:
        return respuesta.json()
    return None

def crear_producto(codigo, marca, codigo_interno, nombre, precio):
    datos = {
        'codigo': codigo,
        'marca': marca,
        'codigo_interno': codigo_interno,
        'nombre': nombre,
        'precio': precio
    }
    respuesta = requests.post(URL_BASE, data=datos)
    if respuesta.status_code == 201:
        return respuesta.json()
    return None

def obtener_producto(producto_id):
    respuesta = requests.get(f'{URL_BASE}{producto_id}/')
    if respuesta.status_code == 200:
        return respuesta.json()
    return None

def actualizar_producto(producto_id, codigo, marca, codigo_interno, nombre, precio):
    datos = {
        'codigo': codigo,
        'marca': marca,
        'codigo_interno': codigo_interno,
        'nombre': nombre,
        'precio': precio
    }
    respuesta = requests.put(f'{URL_BASE}{producto_id}/', data=datos)
    if respuesta.status_code == 200:
        return respuesta.json()
    return None

def eliminar_producto(producto_id):
    respuesta = requests.delete(f'{URL_BASE}{producto_id}/')
    return respuesta.status_code == 204

if __name__ == '__main__':
    nuevo_producto = crear_producto('FER-12345', 'Bosch', 'BOS-67890', 'Taladro Percutor Bosch', 89090.99)
    print('Nuevo producto creado:', nuevo_producto)

    productos = obtener_productos()
    print('Lista de productos:', productos)

    producto_id = nuevo_producto['id']
    detalles_producto = obtener_producto(producto_id)
    print('Detalles del producto:', detalles_producto)

    producto_actualizado = actualizar_producto(producto_id, 'FER-12345', 'Bosch', 'BOS-67890', 'Taladro Percutor Bosch Actualizado', 90000.00)
    print('Producto actualizado:', producto_actualizado)

    if eliminar_producto(producto_id):
        print('Producto eliminado exitosamente')