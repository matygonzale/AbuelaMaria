/*!
* Start Bootstrap - Shop Homepage v5.0.6 (https://startbootstrap.com/template/shop-homepage)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

function agregarAlCarro() {
    var form = document.forms['agregar_al_carro'];
    form.elements['cantidad'].value = document.getElementById('cantidad').value;
    form.submit();
}

function modificarCantidadProductoCarro(id, cantidad)
{
    let ruta="/modificar-cantidad/"+id+"/"+cantidad;
    window.location = ruta;
}

function confirmaAlert(pregunta, ruta) {
    jCustomConfirm(pregunta, 'Tienda', 'Aceptar', 'Cancelar', function(r) {
        if (r) {
            window.location = ruta;
        }
    });
}

function jCustomConfirm(pregunta, titulo, textoAceptar, textoCancelar, callback) {
    // Implementación simulada
    var respuesta = confirm(pregunta);
    callback(respuesta);
}

