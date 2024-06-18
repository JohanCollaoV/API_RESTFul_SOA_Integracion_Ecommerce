// Entorno
// const BASE_URL = 'http://172.20.10.2:8000'; // internet Javier
// const BASE_URL = 'http://192.168.1.3:8000'; // oficina Javier
const BASE_URL = 'http://192.168.1.103:8000'; // casa Javier

function enviarRegistro() {
    let url = '${BASE_URL}/api/registro';
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const data = {
        usuario: {
            username: username,
            email: email,
            password: password
        }
    };

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Éxito:', data);
        alert('Registro exitoso! Token: ' + data.token);
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Error en el registro');
    });
}

document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('error-message');

    fetch('${BASE_URL}/api/acceder', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-API-Key': 'tu_clave_api'  // Asegúrate de agregar tu clave API aquí si es necesario
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.token) {
            localStorage.setItem('token', data.token);
            alert('¡Inicio de sesión exitoso!');
            console.log('Acceso exitoso:', data);
            window.location.href = '/listar-producto';

        } else {
            errorMessage.textContent = 'Error en el acceso. Verifica tus credenciales.';
        }
    })
    .catch(error => {
        console.error('Error en la solicitud:', error);
        errorMessage.textContent = 'Error en la conexión al servidor.';
    });
});

function actualizarFooter() {
    $.ajax({
        url: '${BASE_URL}/api/mostrar-carro',
        type: 'GET',
        headers: {
            'Authorization': 'Token ${token}'
        },
        success: function(data) {
            let productosHtml = '';
            let totalCantidad = 0;
            let precioTotal = 0;

            data.productos_carro.forEach(function(producto) {
                productosHtml += `<div>${producto.cantidad}x ${producto.nombre} - $${producto.precio * producto.cantidad}</div>`;
                totalCantidad += producto.cantidad;
                precioTotal += producto.precio * producto.cantidad;
            });

            $('#productos-carro').html(productosHtml);
            $('#resumen-carro').html(`<div>Total de Productos: ${totalCantidad}</div>
                                       <div>Total a Pagar: $${precioTotal}</div>
                                       <button onclick="procesarPago()">Pagar</button>`);

            // Suponiendo que tienes acceso a datos del usuario
            $('#datos-comprador').html(`Usuario: ${data.usuario_nombre}`);
        },
        error: function() {
            alert('Error al cargar el carrito');
        }
    });
}

function procesarPago() {
    // Implementa la lógica para procesar el pago
}

$(document).ready(function() {
    actualizarFooter();
});
