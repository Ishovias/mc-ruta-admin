
let fecharuta;

function getDatosRutabd() {
    const apiUrl = `/rutas/rutabd/getData`;

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
            fecharuta = this.value;
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

function obtenerTotales(fecharuta) {
    const apiurl = `/rutas/rutabd/getTotales/${fecharuta}`;
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
    const apiurl = `/rutas/rutabd/getRuta/${fecharuta}`;
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
        })
        .catch(error => {
            alert("Error: "+error);
            console.error(error);
        });
}


document.getElementById('buscacliente').addEventListener('input', (e) => {
    let temporizador;
    if (e.target.value != "") {
        const apiUrl = `/rutas/rutabd/buscar?search=${encodeURIComponent(e.target.value)}&filtro=${document.getElementById('filtro').value}`;
        clearTimeout(temporizador); // Limpia el temporizador anterior
        
        temporizador = setTimeout(() => {
            fetch(apiUrl)
                .then(response => response.json())
                .then(data => {
                    const contenedor = document.getElementById('tablaResultados')
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
                            const tdelim = document.createElement('td');
                            tdelim.innerHTML = `<button class="btn-eliminar" data-idy=${fila[fila.length - 1]}>ELIM</button>`;
                            tr.appendChild(tdelim);
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
                })
                .catch(error => {
                    console.error("Error:", error);
                    alert(error)
                    document.getElementById('tablaResultados').innerHTML = "Error al cargar datos";
                });
        }, 1000);
    }
});

getDatosRutabd();
