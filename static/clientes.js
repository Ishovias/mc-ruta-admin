import { URL_BASE as urlBase } from './config.js'
let temporizador;

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
                    const contenedor = document.getElementById('respuestaBuscaCliente')
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
                    alert(error)
                    document.getElementById('respuestaBuscaCliente').innerHTML = "Error al cargar datos";
                });
        }, 1000);
    }
});

function enviarARutaConNombre(id, fecha) {
    const nombreruta = prompt("Ingresa por favor un nombre de ruta: ");
    const apiurl = `${urlBase}/rutas/rutaactual/aruta?idclte=${id}&fecha=${fecha}&nombreruta=${encodeURIComponent(nombreruta)}`;
    fetch(apiurl, {
        "method":"post"
    })
        .then(response => {
            if (response.ok) {
                alert("Cliente enviado a ruta");
            }
        })
        .catch(error => {
            alert("Error en ingreso de ruta con nombre: "+error);
            console.error(error);
            return false;
        });
}

function enviarARuta(id) {
    const fecha = prompt("Ingresa fecha de ruta: ")
    const apiurl = `${urlBase}/rutas/rutaactual/aruta?idclte=${id}&fecha=${fecha}`
    fetch(apiurl, {
        "method":"post"
    })
        .then(response => {
            if (response.status == 200) {
                alert("Cliente enviado a ruta");
            } else if (response.status == 400) {
                enviarARutaConNombre(id, fecha);
            }
        })
        .catch(error => {
            console.error(error);
            alert("Error en fetch: "+error);
        });
}

