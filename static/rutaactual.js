
function getDatos() {
    const apiUrl = `/rutas/rutaactual/getData`;

    fetch(apiUrl, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        const areaResultados = document.getElementById('tablaResultados');
        areaResultados.innerHTML = "";
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
                    if (dato != "None") {
                        td.textContent = dato;
                    } else {
                        td.textContent = "-";
                    }
                    if (/deuda/i.test(dato)){
                        tr.style.backgroundColor = "#d99191";
                    }
                    if (/nuevo/i.test(dato)){
                        tr.style.backgroundColor = "#f2ef46";
                    }
                    tr.appendChild(td);
                });
                const tdobs = document.createElement('td');
                tdobs.innerHTML = `<input class="observaciones" type="text", placeholder="Observaciones">`;
                tr.appendChild(tdobs);
                const td = document.createElement('td');
                td.innerHTML = `<button class="btn-marcar-realizado" data-idy=${fila[10]}>&#x1F44D</button>`;
                tr.appendChild(td);
                const tdposp = document.createElement('td');
                tdposp.innerHTML = `<button class="btn-marcar-pospuesto" data-idy=${fila[10]}>&#x1F44E</button>`;
                tr.appendChild(tdposp);
                const tdelim = document.createElement('td');
                tdelim.innerHTML = `<button class="btn-eliminar" data-idy=${fila[10]}>&#x26D4</button>`;
                tr.appendChild(tdelim);
                const tdmod = document.createElement('td');
                tdmod.innerHTML = `<button class="btn-modificar" data-idy=${fila[10]}>&#x1F4DD</button>`;
                tr.appendChild(tdmod);
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
            const observaciones = fila.querySelector('.observaciones').value
            const ubicacion = e.target.dataset.idy;
            if (e.target.classList.contains('btn-marcar-realizado')) {
                if (fila) {
                    if (fila.style.backgroundColor == "lightgreen") {
                        fila.style.backgroundColor = "";
                    } else {
                        fila.style.backgroundColor = "lightgreen";
                    }
                    confpos(ubicacion,observaciones,"REALIZADO").then(resultado => {
                        if (resultado) {
                            fila.remove();
                        }
                    });
                }
            } else if (e.target.classList.contains('btn-marcar-pospuesto')) {
                if (fila) {
                    if (fila.style.backgroundColor == "red") {
                        fila.style.backgroundColor = "";
                    } else {
                        fila.style.backgroundColor = "red";
                    }
                    confpos(ubicacion,observaciones,"POSPUESTO").then(resultado => {
                        if (resultado) {
                            fila.remove();
                        }
                    });
                }
            } else if (e.target.classList.contains('btn-eliminar')) {
                if (fila) {
                    fila.style.backgroundColor = "gray";
                }
                eliminarCliente(ubicacion).then(response => {
                    if (response) {
                        getDatos();
                        //fila.remove();
                    }
                });
            } else if (e.target.classList.contains('btn-modificar')) {
                    if (fila) {
                        fila.style.backgroundColor = "blue";
                    }
                    window.location.href = `/rutas/rutabd/modregistro/${ubicacion}`;
                }
        });
        areaResultados.appendChild(tabla)

    })
    .catch(error => {
        console.log(error)
    });
}

function confpos(idcliente,observaciones,accion) {
    const apiurl = `/rutas/rutaactual/confpos?idclte=${idcliente}&accion=${accion}&observaciones=${observaciones}`;
    return fetch(apiurl, {
            "method":"post"
        })
            .then(response => {
                if (response.ok) {  
                    return true;
                }
            })
            .catch(error => {
                alert("Error: "+error);
                console.error(error);
                return false;
            });
}

function eliminarCliente(ubicacion) {
    const apiurl = `/rutas/rutaactual/eliminarcliente/${ubicacion}`;
    return fetch(apiurl, {
            "method":"post"
        })
            .then(response => {
                if (response.ok) {
                    return true;
                }
            })
            .catch(error => {
                alert("Error: "+error);
                console.error(error);
                return false;
            });
}

function eliminaRegistro(ubicacion) {
    const apiurl = `/rutas/rutaactual/eliminarcliente/${ubicacion}`;
    return fetch(apiurl, {
            "method":"post"
        })
            .then(response => {
                if (response.ok) {
                    return true;
                }
            })
            .catch(error => {
                alert("Error: "+error);
                console.error(error);
                return false;
            });
}

document.getElementById('btn-movpos').addEventListener('click', function(e) {
    const boton = e.target;
    boton.textContet = "Moviendo...";
    boton.disabled = true;
    const posA = document.getElementById('pos-a');
    const posB = document.getElementById('pos-b');
    const url = `/rutas/rutaactual/movpos/${posA.value}-${posB.value}`;
    fetch(url, {
        "method":"put"
    })
        .then(response => response.json())
        .then(data => {
            if (!data.resultado) {
                alert("Error en servidor");
            }
            boton.textContet = "Mover";
            boton.disabled = false;
            getDatos();
        })
        .catch(error => {
            alert(`Error en fetch: ${error} - ${error.message}`)
        });
});

document.getElementById('form-clte-manual').addEventListener('submit', function(e) {
    e.preventDefault();
    const apiUrl = `/rutas/rutaactual/clientemanual`;
    const formData = new FormData(this);
    fetch(apiUrl, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            this.reset();
            getDatos();
        })
        .catch(error => {
            alert("Error en peticion: "+error);
        });
});

getDatos();
