import { URL_BASE as urlBase } from './config.js';

function getDatos() {
    const apiUrl = `${urlBase}/rutas/rutaactual/getData`;

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
            } else {
                const td = document.createElement('td');
                td.innerHTML = "Sin datos";
                tr.appendChild(td);
            }
            cuerpo.appendChild(tr);
        });
        tabla.appendChild(encabezado);
        tabla.appendChild(cuerpo);
        areaResultados.appendChild(tabla)
    })
    .catch(error => {
        console.log(error)
    });
}

getDatos();
