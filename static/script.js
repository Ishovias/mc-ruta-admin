import { URL_BASE as urlBase } from './config.js'
let temporizador;

function enviarARuta(idcliente) {
    const apiUrl = `${urlBase}/clientes/aruta/${idcliente}`;
    fetch(apiUrl)
        .then(response => {
            if (!response.ok) throw new Error("Error en la respuesta");
            return response.json();
        })
        .then(data => {
            alert(data.alerta);
        }).catch(error => {
            alert(`Error durante fetch ${error}`);
        });
}

function escuchadorCoder2() {
    document.getElementById('coder2').addEventListener('input', (e) => {
        const apiUrl = `${urlBase}/coder2/frcod?fr=${encodeURIComponent(e.target.value)}`;
        
        clearTimeout(temporizador); // Limpia el temporizador anterior
        
        temporizador = setTimeout(() => {
            fetch(apiUrl)
                .then(response => {
                    if (!response.ok) throw new Error("Error en la respuesta");
                    return response.json();
                })
                .then(data => {
                    document.getElementById('respuesta').value = data.frproc;
                })
                .catch(error => {
                    console.error("Error:", error);
                    document.getElementById('respuesta').value = "Error al cargar datos";
                });
        }, 750);
    });
}

function procesarFormCliente(elementoId, rutaApi, rutaRedireccion) {
    document.getElementById(elementoId).addEventListener('submit', (e) => {
        e.preventDefault(); // Evitar el envío del formulario por defecto
        console.log(`${elementoId} ${rutaApi} ${rutaRedireccion}`)
        const formData = new FormData(e.target);
        const btnSubmit = document.getElementById('btnSubmit');
        const textoBoton = btnSubmit.textContent;
        btnSubmit.disabled = true;
        btnSubmit.textContent = "Enviando...";
        const apiUrl = `${urlBase}${rutaApi}`;

        fetch(apiUrl ,{
            method: 'POST',
            body: formData
        })
        .then(response => {
            const areaRespuesta = document.getElementById('respuestaServidor')
            areaRespuesta.innerHTML = "";
            const estado = response.status;
            if (estado === 201) {
                areaRespuesta.innerHTML = `<h2>Ok...</h2>`;
            } else if (estado === 400) {
                areaRespuesta.innerHTML = `<h2>API error...</h2>`;
            }
            return response.json();
        })
        .then(data => {
            const btnSubmit = document.getElementById('btnSubmit');
            const areaRespuesta = document.getElementById('respuestaServidor');
            if (data.newClienteOK) {
                areaRespuesta.insertAdjacentHTML('beforeend','<span>Exito!!... redirigiendo</span>');
                setTimeout(() => {
                    window.location.href = `${urlBase}${rutaRedireccion}`;
                },3000);
            } else {
                areaRespuesta.insertAdjacentHTML('beforeend','<span>Error en datos... Reintentar</span>');
                btnSubmit.disabled = false;
                btnSubmit.textContent = textoBoton;
            }
        })
        .catch(error => {
            alert(error);
        });
    });
}

function escuchaBuscaCliente() {
    document.getElementById('buscacliente').addEventListener('input', (e) => {
        if (e.target.value != "") {
            const apiUrl = `${urlBase}/clientes/buscar?search=${encodeURIComponent(e.target.value)}&filtro=${document.getElementById('filtro').value}`;
            clearTimeout(temporizador); // Limpia el temporizador anterior
            
            temporizador = setTimeout(() => {
                fetch(apiUrl)
                    .then(response => {
                        if (!response.ok) throw new Error("Error en la respuesta");
                        return response.json();
                    })
                    .then(data => {
                        contenedor = document.getElementById('respuestaBuscaCliente')
                        contenedor.innerHTML = ''; // Limpiar el contenedor antes de agregar nuevos elementos
                        
                        if (data.encabezados) {
                            const tabla = document.createElement('table');
                            tabla.className = 'table table-striped table-hover table-bordered';
                            const encabezado = document.createElement('thead');
                            const filaEncabezado = document.createElement('tr');
                            
                            const th = document.createElement('th');
                            th.textContent = 'A ruta';
                            filaEncabezado.appendChild(th);
                            
                            data.encabezados.forEach(encabezado => {
                                const th = document.createElement('th');
                                th.textContent = encabezado;
                                filaEncabezado.appendChild(th);
                            });
                            encabezado.appendChild(filaEncabezado);
                            
                            const cuerpo = document.createElement('tbody');
                            data.datos.forEach(fila => {
                                const tr = document.createElement('tr');
                                const td = document.createElement('td');
                                td.innerHTML = `<button class="btn-aruta" data-id=${fila[0]}>A ruta</button>`;
                                tr.appendChild(td);
                                fila.forEach(celda => {
                                    const td = document.createElement('td');
                                    td.textContent = celda;
                                    tr.appendChild(td);
                                });
                                const tdModificar = document.createElement('td');
                                tdModificar.innerHTML = `<button class="btn-modificar" data-id=${fila[0]}>Modificar</button>`;
                                tr.appendChild(tdModificar);
                                const tdEliminar = document.createElement('td');
                                tdEliminar.innerHTML = `<button class="btn-eliminar" data-id=${fila[0]} style="background: red;">Eliminar</button>`;
                                tr.appendChild(tdEliminar);
                                cuerpo.appendChild(tr);
                            });
                            
                            tabla.appendChild(encabezado);
                            tabla.appendChild(cuerpo);
                            tabla.addEventListener('click', (e) => {
                                if(e.target.classList.contains('btn-aruta')) {
                                    const id = e.target.dataset.id;
                                    enviarARuta(id);
                                } else if (e.target.classList.contains('btn-modificar')) {
                                    const id = e.target.dataset.id;
                                    console.log("Boton modificar "+id+" presionado");
                                } else if (e.target.classList.contains('btn-eliminar')) {
                                    const id = e.target.dataset.id;
                                    console.log("Boton eliminar "+id+" presionado");
                                }
                            });
                            contenedor.appendChild(tabla);
                        } else {
                            contenedor.innerHTML = data.sindatos;
                        }
                    })
                    .catch(error => {
                        console.error("Error:", error);
                        document.getElementById('respuestaBuscaCliente').innerHTML = "Error al cargar datos";
                    });
            }, 1000);
        }
    });
}


