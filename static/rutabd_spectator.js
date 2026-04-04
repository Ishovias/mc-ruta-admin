
let fecharuta;
const mensajeCargaServidor = '<h3>Solicitando datos al servidor...</h3>';
const mensajeErrorServidor = '<h3 style="background: red;">Error en respuesta del servidor, reintente</h3>';
const mensajeCargaLista = '** Cargando lista rutas **';
const mensajeCargaListaError = 'X ERROR EN SERVER X';

// Carga lista desplegable de rutas almacenadas
function getDatosRutabd() {
    const apiUrl = `/rutas/rutabd/getData`;//{{{
    const selector = document.getElementById('select-ruta');
    selector.innerHTML = `<option value=null selected>${mensajeCargaLista}</option>`;
    return fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
        selector.innerHTML = "";
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
            fecharuta = this.value;
            if (fecharuta) {
                muestraRuta(fecharuta).then(obtenerTotales(fecharuta));
            }
        });
        return data
    })
    .catch(error => {
        selector.innerHTML = `<option value=null selected>${mensajeCargaListaError}</option>`;
        console.log(error);
    });
}//}}}

// Carga Totales de ruta seleccionada
function obtenerTotales(fecharuta) {
    const apiurl = `/rutas/rutabd/getTotales/${fecharuta}`;//{{{
    const resultados = document.getElementById("totales");
    resultados.innerHTML = mensajeCargaServidor;
    return fetch(apiurl)
        .then(response => response.json())
        .then(data => {
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
            return data;
        })
        .catch(error => {
            areaResultado.innerHTML = mensajeErrorServidor;
            console.error(error);
        });
}//}}}

// Carga Datos de ruta seleccionada
function muestraRuta(fecharuta) {
    const apiurl = `/rutas/rutabd/getRuta/${fecharuta}?c=rutabd_busquedas_viewer`;//{{{
    const areaResultado = document.getElementById("tablaResultados");
    areaResultado.innerHTML = mensajeCargaServidor;
    return fetch(apiurl)
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
                            tr.style.backgroundColor = "rgba(255,0,0,0.5)";
                        }
                        if (/enruta/i.test(dato)) {
                            tr.style.backgroundColor = "rgba(0,255,0,0.5)";
                        }
                        tr.appendChild(td);
                    });
                } else {
                    const td = document.createElement('td');
                    td.innerHTML = "Sin datos";
                    tr.appendChild(td);
                }
                cuerpo.appendChild(tr);
            });
            tabla.appendChild(encabezado);
            tabla.appendChild(cuerpo);
            areaResultado.appendChild(tabla)
            return data;
        })
        .catch(error => {
            areaResultado.innerHTML = mensajeErrorServidor;
            console.error(error);
        });
}//}}}

function muestraResultadoBusqueda(apiUrl, contenedor) {
    return fetch(apiUrl)//{{{
        .then(response => response.json())
        .then(data => {
            contenedor.innerHTML = ''; // Limpiar el contenedor antes de agregar nuevos elementos
            console.log(data);
            if (data.encabezados) {
                const tabla = document.createElement('table');
                tabla.className = 'table table-striped table-hover table-bordered';
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
                    fila.forEach(celda => {
                        const td = document.createElement('td');
                        if (celda != "None") {
                            td.textContent = celda;
                        } else {
                            td.textContent = "-";
                        }
                        if (/pospuesto/i.test(celda)) {
                            tr.style.backgroundColor = "rgba(255,0,0,0.5)";
                        }
                        if (/enruta/i.test(celda)) {
                            tr.style.backgroundColor = "rgba(0,255,0,0.5)";
                        }
                        tr.appendChild(td);
                    });
                    cuerpo.appendChild(tr);
                });
                tabla.appendChild(encabezado);
                tabla.appendChild(cuerpo);
                contenedor.appendChild(tabla);
            } else {
                contenedor.innerHTML = data.sindatos;
            }
            return data;
        })
        .catch(error => {
            contenedor.innerHTML = mensajeErrorServidor;
        });//}}}
}

function ejecutarBusqueda(input) {
    const apiUrl = `/rutas/rutabd/buscar?search=${encodeURIComponent(input.value)}&filtro=${document.getElementById('filtro').value}&c=rutabd_busquedas_viewer`;//{{{
    const contenedor = document.getElementById('tablaResultados')
    const totales = document.getElementById('totales');
    contenedor.innerHTML = mensajeCargaServidor; // Limpiar el contenedor antes de agregar nuevos elementos
    totales.innerHTML = ''; // Limpiar totales, no los usaremos en estos resultados
    muestraResultadoBusqueda(apiUrl, contenedor);//}}}
}

// EventListener de buscador de clientes
const buscacliente = document.getElementById('buscacliente');
buscacliente.addEventListener('keypress', (e) => {
    if (e.target.value != "" && e.key == 'Enter') {
        ejecutarBusqueda(buscacliente);
    }
});

const botonbuscar = document.getElementById('botonBuscar');
botonbuscar.addEventListener('click', (e) => {
    ejecutarBusqueda(buscacliente);
});

getDatosRutabd();
