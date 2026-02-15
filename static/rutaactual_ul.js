
function getDatos() {
    const apiUrl = `/rutas/rutaactual/getData`;//{{{
    const areaResultados = document.getElementById('tablaResultados');
    areaResultados.innerHTML = "<h2>Cargando...</h2>";

    fetch(apiUrl, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        areaResultados.innerHTML = "";
        const listado = document.createElement('ul');
        data.datos.forEach(fila => {
            const li = document.createElement('li');
            if (fila[0] != "Sin datos") {
                const datosCliente = document.createElement('p');
                let indexEncabezado = 0;
                let item = "";
                fila.forEach(dato => {
                    const encabezado = data.encabezados[indexEncabezado];
                    if (dato != "None") {
                        item = item + encabezado + " : " + "<strong>" + dato + "</strong>" + "<br>"
                    } else {
                        item.concat(" ", encabezado, " : ", "-", "<br>");
                    }
                    if (/deuda/i.test(dato)){
                        li.style.backgroundColor = "#d99191";
                    }
                    if (/nuevo/i.test(dato)){
                        li.style.backgroundColor = "#f2ef46";
                    }
                    indexEncabezado += 1;
                });
                datosCliente.innerHTML = item;
                const botonera = document.createElement('div');
                botonera.innerHTML = `<br><input class="observaciones" type="text", placeholder="Observaciones"><br><br>
                    <button class="btn-marcar-realizado" data-idy=${fila[10]}>&#x1F44D</button>
                    <button class="btn-marcar-pospuesto" data-idy=${fila[10]}>&#x1F44E</button>
                    <button class="btn-eliminar" data-idy=${fila[10]}>&#x26D4</button>
                    <button class="btn-modificar" data-idy=${fila[10]}>&#x1F4DD</button>
                    <br><br><hr><br>`
                li.appendChild(datosCliente);
                li.appendChild(botonera);
            } else {
                const li = document.createElement('li');
                li.innerHTML = "<p>Sin datos</p>";
            }
            listado.appendChild(li);
        });
        listado.addEventListener('click' , (e) => {
            const li = e.target.closest('li');
            const observaciones = li.querySelector('.observaciones').value
            const ubicacion = e.target.dataset.idy;
            if (e.target.classList.contains('btn-marcar-realizado')) {
                if (li) {
                    if (li.style.backgroundColor == "lightgreen") {
                        li.style.backgroundColor = "";
                    } else {
                        li.style.backgroundColor = "lightgreen";
                    }
                    confpos(ubicacion,observaciones,"REALIZADO").then(resultado => {
                        if (resultado) {
                            li.remove();
                            getSumario();
                        }
                    });
                }
            } else if (e.target.classList.contains('btn-marcar-pospuesto')) {
                if (li) {
                    if (li.style.backgroundColor == "red") {
                        li.style.backgroundColor = "";
                    } else {
                        li.style.backgroundColor = "red";
                    }
                    confpos(ubicacion,observaciones,"POSPUESTO").then(resultado => {
                        if (resultado) {
                            li.remove();
                            getSumario();
                        }
                    });
                }
            } else if (e.target.classList.contains('btn-eliminar')) {
                if (li) {
                    li.style.backgroundColor = "gray";
                }
                eliminarCliente(ubicacion).then(response => {
                    if (response) {
                        getDatos();
                        //li.remove();
                    }
                });
            } else if (e.target.classList.contains('btn-modificar')) {
                    if (li) {
                        li.style.backgroundColor = "blue";
                    }
                    window.location.href = `/rutas/rutabd/modregistro/${ubicacion}`;
                }
        });
        areaResultados.appendChild(listado);
        getSumario();
    })
    .catch(error => {
        console.log(error)
    });//}}}
}

function getSumario() {
    const url = `/rutas/sumario/rutaactual`;//{{{
    const sumario = document.getElementById('sumario');
    sumario.innerHTML = "<h3>Cargando sumario...</h3>";
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if ('realizados' in data) {
                sumario.innerHTML = `
                    <h3>Clientes restantes: ${data.enruta}</h3>
                    <h3>Clientes postergados: ${data.postergados}</h3>
                    <h3>Clientes realizados: ${data.realizados}</h3>`;
            } else {
                sumario.innerHTML = `<h3>No hay ruta en curso</h3>`;
            }
        })
        .catch(error => {
            alert(`Error en fetch: ${error}`);
        });//}}}
}

function confpos(idcliente,observaciones,accion) {
    const apiurl = `/rutas/rutaactual/confpos?idclte=${idcliente}&accion=${accion}&observaciones=${observaciones}`;//{{{
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
            });//}}}
}

function eliminarCliente(ubicacion) {
    const apiurl = `/rutas/rutaactual/eliminarcliente/${ubicacion}`;//{{{
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
            });//}}}
}

function eliminaRegistro(ubicacion) {
    const apiurl = `/rutas/rutaactual/eliminarcliente/${ubicacion}`;//{{{
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
            });//}}}
}

document.getElementById('btn-movpos').addEventListener('click', function(e) {
    const boton = document.getElementById('btn-movpos');//{{{
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
            posA.value = "";
            posB.value = "";
            getDatos();
        })
        .catch(error => {
            alert(`Error en fetch: ${error} - ${error.message}`)
        });//}}}
});

document.getElementById('form-clte-manual').addEventListener('submit', function(e) {
    e.preventDefault();//{{{
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
        });//}}}
});

getDatos();
