
function getFechas() {
    const select = document.getElementById('fechas-almacenadas');//{{{
    select.innerHTML = '<option value="" default selected>Cargando fechas ...</option>'
    const url = `${urlBase}/gastos/getFechas`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('fechas-almacenadas');
            select.innerHTML = '';
            const defaultOption = document.createElement('option');
            defaultOption.selected = true;
            defaultOption.hidden = true;
            defaultOption.textContent = "- Selecciona -";
            select.appendChild(defaultOption);
            if (data.fechas.length > 0) {
                data.fechas.forEach(fecha => {
                    const option = document.createElement('option');
                    option.value = fecha[0];
                    option.textContent = fecha[1];
                    select.appendChild(option);
                });
            } else {
                const sinDatos = document.createElement('option');
                sinDatos.value = "";
                sinDatos.textContent = "- Sin datos aun -";
                select.appendChild(sinDatos);
            }
            const botonFormulario = document.getElementById('btn-add-gasto');
            botonFormulario.textContent = "Agregar gasto";
            botonFormulario.disabled = false;
        })
        .catch(error => {
            alert(`Error en fetch: ${error} - ${error.message}`)
        });//}}}
}

function getDatos(fecha="vigente") {
    const areaTotales = document.getElementById('totales');//{{{
    areaTotales.innerHTML = '<h3>Cargando totales...</h3>';
    const areaResultados = document.getElementById('tablaResultados');
    areaResultados.innerHTML = '<h3>Cargando...</h3>';
    const url = `${urlBase}/gastos/getData/${fecha}`;
    fetch(url)
    .then(response => response.json())
    .then(data => {
        areaResultados.innerHTML = '';
        const tabla = document.createElement('table');
        // HEAD TABLA
        const thead = document.createElement('thead');
        data.encabezados.forEach(encabezado =>{
            if (encabezado != data.encabezados[data.encabezados.length-1]) {
                const th = document.createElement('th');
                th.textContent = encabezado;
                thead.appendChild(th);
            }
        });
        // BODY TABLA
        const tbody = document.createElement('tbody');
        if (data.datos != "-- Sin datos --"){
            data.datos.forEach(fila => {
                const tr = document.createElement('tr');
                fila.forEach(dato => {
                    if (dato != fila[fila.length-1]) { 
                        const td = document.createElement('td');
                        td.textContent = dato;
                        tr.appendChild(td);
                    }
                });
                const botonera = document.createElement('td');
                botonera.innerHTML = `<button class="btn-eliminar" style="background: #CFA39B;" data-idy=${fila[fila.length-1]}>&#x1F6AB</button>`;
                tr.appendChild(botonera);
                tbody.appendChild(tr);
            });
        } else {
            tbody.innerHTML = "<tr><td>Sin datos</td></tr>"
        }
        tabla.appendChild(thead);
        tabla.appendChild(tbody);
        tabla.addEventListener('click', function(e){
            const ubicacion = e.target.dataset.idy;
            const fila = e.target.closest('tr');
                fila.style.background = "red";
                if (e.target.classList.contains('btn-eliminar')){
                    eliminarRegistro(ubicacion,fila);
                }
        });
        areaResultados.appendChild(tabla);
        // AREA TOTALES
        insertarSumarioRendir(areaTotales,data,fecha);
    })
    .catch(error => {
        console.error(error);
        alert(`Error: ${error}-${error.message}`);
    });//}}}
}

const formIngreso = document.getElementById('form-gasto');
formIngreso.addEventListener('submit', (e) => {
    e.preventDefault();//{{{
    const boton = document.getElementById('btn-add-gasto');
    boton.textContent = "Espere...";
    boton.disabled = true;
    const formData = new FormData(formIngreso);
    const fecha = document.getElementById('fecha').value;
    const url = `/gastos/addGasto`
    fetch(url, {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (!data.resultado) {
            alert("Error en backend");
        } else {
            formIngreso.reset();
            getFechas();
            getDatos();
        }
        boton.textContent = "Agregar gasto";
        boton.disabled = false;
    })
    .catch(error => {
        console.error(error);
        alert(`Error: ${error}-${error.message}`);
        boton.textContent = "Agregar gasto";
        boton.disabled = false;
    });//}}}
});

const selectFecha = document.getElementById('fechas-almacenadas');
selectFecha.addEventListener('change', (e) => {
    const fecha = e.target.value;//{{{
    getDatos(fecha);//}}}
});

function eliminarRegistro(ubicacion,filahtml) {
    const url = `/gastos/eliminar/${ubicacion}`;//{{{
    fetch(url,{
        method:"DELETE"
    })
    .then(response => response.json())
    .then(data => {
        if(data.resultado == false){
            alert("Error en servidor, registro no eliminado");
        } else {
            filahtml.remove();
            actualizarTotales();
        }
    })
    .catch(error => {
        alert(`Error en fetch gastos/eliminarRegistro:${error}`);
        console.log(error);
    });//}}}
}

function actualizarTotales(fecha="vigente"){
    const areaTotales = document.getElementById('totales');//{{{
    areaTotales.innerHTML = '<h3>Cargando totales...</h3>';
    const url = `/gastos/totales/${fecha}`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            insertarSumarioRendir(areaTotales,data,fecha);
        }).catch(error => {
            alert(`Error en gastos/actualizarTotales: ${error}`);
        });
}

function insertarSumarioRendir(areaInsertar,data,fecha){
    //{{{
    areaInsertar.innerHTML = `<br><hr><br><h3>Depositado (abonos): ${data.totales.abonos}</h3>
        <h3>Gastos: ${data.totales.gastos}</h3>
        <h3>Diferencia anterior: ${data.totales.diferencia_anterior}</h3>
        <h2 style="color: red;">Diferencia: ${data.totales.diferencia}</h2>
        `;
    areaInsertar.innerHTML += `<button id="btn-rendir" value="${fecha}">Generar rendicion</button>`;
    // ACCIONES BOTON RENDIR
    const botonRendir = document.getElementById('btn-rendir');
    botonRendir.addEventListener('click', (e) => {
        window.location.href = `/gastos/rendir/${fecha}`;
    });//}}}
}

document.addEventListener('DOMContentLoaded', function() {
    getFechas();
    getDatos();
});
