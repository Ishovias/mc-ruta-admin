
function getDatos() {
    const apiUrl = `/rutas/rutaactual/getData`;//{{{
    const areaResultados = document.getElementById('tablaResultados');
    areaResultados.innerHTML = "<h2>Cargando...</h2>";
    fetch(apiUrl, {
        method: 'POST'//{{{
    })
    .then(response => response.json())
    .then(data => {
        areaResultados.innerHTML = "";
        const tarjetas = document.createElement('div');
        data.datos.forEach(fila => {
            if (fila[0] != "Sin datos") {
                const tarjeta = `
                    <div class="card">
                        <div class="card-header">
                            <h3>${fila[4]}</h3>
                            <p class="rut">RUT : ${fila[3]}</p>
                        </div>
                        <hr>
                        <div class="card-body">
                            <div class="info-group location">
                                <p>DIRECCIÓN : <span>${fila[5]}</span></p>
                                <p>COMUNA : <span>${fila[6]}</span></p>
                            </div>
                            <div class="info-group contact">
                                <p>TELÉFONO : <span>${fila[6]}</span></p>
                            </div>
                            <div class="info-group details">
                                <p>FECHA : <span>${fila[0]}</span></p>
                                <p>ID TRANS : <span>${fila[1]}</span></p>
                                <p>CONTRATO : <span>${fila[2]}</span></p>
                                <p>ID CLIENTE : <span>${fila[9]}</span></p>
                                <p>idy : <span>${fila[10]}</span></p>
                            </div>
                        </div>
                        <hr>
                        <div class="card-footer">
                            <p>OBS : <span>${fila[8]}</span></p>
                        </div>
                    </div>
                    <br>
                    `
                tarjetas.innerHTML += tarjeta;
            } else {
                const li = document.createElement('li');
                li.innerHTML = "<p>Sin datos</p>";
            }
        });
        areaResultados.appendChild(tarjetas);
        getSumario();
    })
    .catch(error => {
        console.log(error)//}}}
    });
    getStockFurgon();
}//}}}

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
                    <h3>Clientes con deuda o problema: ${data.postergados}</h3>
                    <h3>Clientes realizados: ${data.realizados}</h3>`;
            } else {
                sumario.innerHTML = `<h3>No hay ruta en curso o ruta finalizada</h3>`;
            }
        })
        .catch(error => {
            alert(`Error en fetch: ${error}`);
        });//}}}
}

function getStockFurgon() {
    const apiUrlStock = `/inventario/getstock`;//{{{
    fetch(apiUrlStock, {
        method: 'GET'//{{{
    })
    .then(response => response.json())
    .then(data => {
        const areaStock = document.getElementById('stock');
        areaStock.innerHTML = "";
        const ulf = document.createElement('ul');
        data.forEach(item => {
            const li = document.createElement('li');
            let color = "#ec7c7cfd";
            if (Number(item[3]) > 0 && Number(item[3]) < 50) {
                color = "#e7da28fd";
            } else if (Number(item[3]) >= 50) {
                color = "#6ab13cfd";
            }
            li.innerHTML = `${item[1]}: <strong style="background-color: ${color};">${item[3]} unids</strong>`;
            ulf.appendChild(li);
        });
        areaStock.appendChild(ulf);
    })
    .catch(error => {
        console.log(error);//}}}
    });//}}}
}

//{{{ En carga de pagina
getDatos();

function recargarDatos() {
    //location.reload();
    getDatos();
}

//window.onload = recargarPagina;

const tiempoEntreRecargas = 60000;
setInterval(recargarDatos, tiempoEntreRecargas);
//}}}

