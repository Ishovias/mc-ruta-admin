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
                li.innerHTML = `
                    ${item[1]}: <strong>${item[2]} unids</strong><br>
                    <input id="modificador${item[1]}" type="number" value="${item[2]}" style="width: 90px;">
                    <button class="btn-mod-inv" data-col="${item[0]}">MOD</button>
                    <input id="sumador-${item[1]} "type="number" style="width: 90px;">
                    <button class="btn-suma">+</button><hr><br>
                    `;
                ul.appendChild(li);
            });
            ul.addEventListener('click', (e) => {
                const inputMod = e.target.closest('li').querySelector('[id*="modificador"]');
                if (e.target.classList.contains('btn-mod-inv')) {
                    const columna = e.target.dataset.col;
                    const btnMod = e.target.closest('li').querySelector('.btn-mod-inv');
                    if (inputMod) {
                        modificaStock(columna, Number(inputMod.value));
                        btnMod.style.backgroundColor = "#8cf48cfd";
                    }
                } else if (e.target.classList.contains('btn-suma')) {
                    const inputSum = e.target.closest('li').querySelector('[id*="sumador"]');
                    if (inputSum) {
                        if (inputMod.value == null) {
                            inputMod.value = 0
                        }
                        inputMod.value = Number(inputMod.value) + Number(inputSum.value);
                        inputMod.style.backgroundColor = "#8cf48cfd";
                        inputSum.value = null;
                    }
                }

            });
            areaStock.appendChild(ul);
        })
        .catch(error => {
            console.log(error);
        });
}

function modificaStock(columna, cantidad) {
    const apiurl = `${urlBase}/inventario/modifica?col=${columna}&cant=${cantidad}`;
    fetch(apiurl, {
        "method":"post"
    })
        .then(response => {
            if (response.ok) {
                getStock();
            }
        })
        .catch(error => {
            alert("Error: "+error);
            console.error(error);
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
