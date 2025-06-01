import { URL_BASE as urlBase } from './config.js';

function getDatosRutabd() {
    const apiUrl = `${urlBase}/rutas/rutabd/getData`;

    fetch(apiUrl, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        const selectorRutas = document.getElementById('listaRutas');
        selectorRutas.innerHTML = "";
        const selector = document.createElement('select');
        const defaultOption = document.createElement('option');
        defaultOption.selected = true;
        defaultOption.textContent = "--Selecciona ruta--";
        selector.appendChild(defaultOption);
        data.forEach(item => {
            const option = document.createElement('option');
            option.value = item[0];
            option.textContent = `${item[0]} - ${item[1]}`;
            selector.appendChild(option);
        });
        selector.addEventListener('change' , function() {
            const fecharuta = this.value;
            if (fecharuta) {
                muestraRuta(fecharuta);
                obtenerTotales(fecharuta);
            }
        });
        selectorRutas.appendChild(selector);
    })
    .catch(error => {
        console.log(error);
    });
}

function marcarStatus(ubicacion) {
    const apiurl = `${urlBase}/rutas/rutabd/marcarStatus?ubicacion=${ubicacion}&status=enruta`;
    fetch(apiurl, {
        "method":"post"
    })
        .then(response => {
            if (response.ok) {
                getDatosRutabd();
            }
        })
        .catch(error => {
            alert("Error: "+error);
            console.error(error);
        });
}

function obtenerTotales(fecharuta) {
    const apiurl = `${urlBase}/rutas/rutabd/getTotales/${fecharuta}`;
    fetch(apiurl, {
        "method":"post"
    })
        .then(response => response.json())
        .then(data => {
            const resultados = document.getElementById("totales");
            resultados.innerHTML = `<h3>Totales de la ruta</h3>`;
            if (data.totales.length > 0) {
                const lista = document.createElement('ul');
                data.totales.forEach(item => {
                    const elemento = document.createElement('li');
                    elemento.textContent = `${item[0]}===  ${item[1]}`;
                    lista.appendChild(elemento);
                });
                resultados.appendChild(lista);
            } else {
                const comentario = document.createElement('span');
                comentario.textContent = "Sin registros";
                resultados.appendChild(comentario);
            }
        })
        .catch(error => {
            alert("Error: "+error);
            console.error(error);
        });
}

function muestraRuta(fecharuta) {
    const apiurl = `${urlBase}/rutas/rutabd/getRuta/${fecharuta}`;
    fetch(apiurl, {
        "method":"post"
    })
        .then(response => response.json())
        .then(data => {
            const areaResultado = document.getElementById("tablaResultados");
            areaResultado.innerHTML = "";
            const tabla = document.createElement('table');
            const encabezado = document.createElement('thead');
            const filaEncabezado = document.createElement('tr');
            
            data.encabezados.forEach(encabezado => {
                const th = document.createElement('th');
                th.textContent = encabezado;
                filaEncabezado.appendChild(th);
            });

            encabezado.appendChild(filaEncabezado);

            const cuerpo = document.createElement('tbody');
            data.datos.forEach(fila => {
                const tr = document.createElement('tr');
                if (fila[0] != "Sin datos") {
                    fila.forEach(dato => {
                        const td = document.createElement('td');
                        td.textContent = dato;
                        if (/pospuesto/i.test(dato)) {
                            tr.style.backgroundColor = "red";
                        }
                        tr.appendChild(td);
                    });
                    const tdaruta = document.createElement('td');
                    tdaruta.innerHTML = `<button class="btn-aruta" data-idy=${fila[fila.length - 1]}>ARUTA</button>`;
                    tr.appendChild(tdaruta);
                    const tdelim = document.createElement('td');
                    tdelim.innerHTML = `<button class="btn-eliminar" data-idy=${fila[fila.length - 1]}>ELIM</button>`;
                    tr.appendChild(tdelim);
                } else {
                    const td = document.createElement('td');
                    td.innerHTML = "Sin datos";
                    tr.appendChild(td);
                }
                cuerpo.appendChild(tr);
            });
            tabla.appendChild(encabezado);
            tabla.appendChild(cuerpo);
            tabla.addEventListener('click' , (e) => {
                const fila = e.target.closest('tr');
                const ubicacion = e.target.dataset.idy;
                if (e.target.classList.contains('btn-aruta')) {
                    if (fila) {
                        fila.style.backgroundColor = "blue";
                    }
                    marcarStatus(ubicacion);
                }
                if (e.target.classList.contains('btn-eliminar')) {
                    if (fila) {
                        fila.style.backgroundColor = "gray";
                    }
                    eliminarCliente(ubicacion,muestraRuta,fecharuta);
                }
            });
            areaResultado.appendChild(tabla)
        })
        .catch(error => {
            alert("Error: "+error);
            console.error(error);
        });
}

function eliminarCliente(ubicacion, funcionCallback, argumento = null) {
    const apiurl = `${urlBase}/rutas/rutaactual/eliminarcliente/${ubicacion}`;
    fetch(apiurl, {
        "method":"post"
    })
        .then(response => {
            if (response.ok) {
                if (argumento == null) {
                    funcionCallback();
                } else {
                    funcionCallback(argumento);
                }
            }
        })
        .catch(error => {
            alert("Error: "+error);
            console.error(error);
        });
}

getDatosRutabd();
