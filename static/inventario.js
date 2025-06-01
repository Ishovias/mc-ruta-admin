import { URL_BASE as urlBase } from './config.js';

function getStock() {
    const apiUrl = `${urlBase}/inventario/getstock`;

    fetch(apiUrl, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        const areaStock = document.getElementById('stock');
        areaStock.innerHTML = "";
        const ul = document.createElement('ul');
        data.forEach(item => {
            const li = document.createElement('li');
            let color = "#ec7c7cfd";
            if (Number(item[2]) > 0 && Number(item[2]) < 50) {
                color = "#e7da28fd";
            } else if (Number(item[2]) >= 50) {
                color = "#6ab13cfd";
            }
            li.innerHTML = `${item[1]}: <strong style="background-color: ${color};">${item[2]} unids</strong>`;
            ul.appendChild(li);
        });
        areaStock.appendChild(ul);
    })
    .catch(error => {
        console.log(error);
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

getStock();
