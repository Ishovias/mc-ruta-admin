
function getStock() {
        const apiUrl = `/inventario/getstock`;
        fetch(apiUrl, {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => {
            const areaStock = document.getElementById('stock');
            areaStock.innerHTML = "";
            // Area stock general
            const ul = document.createElement('ul');
            data.forEach(item => {
                const li = document.createElement('li');//{{{
                li.innerHTML = `
                    ${item[1]}: <strong>${item[2]} unids</strong><br>
                    <input id="modificador-a${item[1]}" type="number" value="${item[2]}" style="width: 90px;">
                    <button class="btn-mod-inv-a" data-col="${item[0]}">MOD</button>
                    <input id="sumador-a-${item[1]} "type="number" style="width: 90px;">
                    <button class="btn-suma-a">+</button><hr><br>
                    `;
                ul.appendChild(li);
            });
            ul.addEventListener('click', (e) => {
                const inputMod = e.target.closest('li').querySelector('[id*="modificador-a"]');
                if (e.target.classList.contains('btn-mod-inv-a')) {
                    const columna = e.target.dataset.col;
                    const btnMod = e.target.closest('li').querySelector('.btn-mod-inv-a');
                    if (inputMod) {
                        modificaStock(columna, Number(inputMod.value));
                        btnMod.style.backgroundColor = "#8cf48cfd";
                    }
                } else if (e.target.classList.contains('btn-suma-a')) {
                    const inputSum = e.target.closest('li').querySelector('[id*="sumador-a"]');
                    if (inputSum) {
                        if (inputMod.value == null) {
                            inputMod.value = 0
                        }
                        inputMod.value = Number(inputMod.value) + Number(inputSum.value);
                        inputMod.style.backgroundColor = "#8cf48cfd";
                        inputSum.value = null;
                    }
                }//}}}
            });
            areaStock.appendChild(ul);
            // Area stock FURGON
            const areaFurgon = document.getElementById('stock-furgon');
            areaFurgon.innerHTML = "<h3>Stock Furgon</h3>";
            const ulf = document.createElement('ul');
            data.forEach(item => {
                const li = document.createElement('li');//{{{
                li.innerHTML = `
                    ${item[1]}: <strong>${item[3]} unids</strong><br>
                    <input id="modificador${item[1]}" type="number" value="${item[3]}" style="width: 90px;">
                    <button class="btn-mod-inv" data-col="${item[0]}">MOD</button>
                    <input id="sumador-${item[1]} "type="number" style="width: 90px;">
                    <button class="btn-suma">+</button><hr><br>
                    `;
                ulf.appendChild(li);
            });
            ulf.addEventListener('click', (e) => {
                const inputMod = e.target.closest('li').querySelector('[id*="modificador"]');
                if (e.target.classList.contains('btn-mod-inv')) {
                    const columna = e.target.dataset.col;
                    const btnMod = e.target.closest('li').querySelector('.btn-mod-inv');
                    if (inputMod) {
                        modificaStock(columna, Number(inputMod.value), true);
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
                }//}}}
            });
            areaFurgon.appendChild(ulf);
        })
        .catch(error => {
            console.log(error);
        });
}

function modificaStock(columna, cantidad, furgon = false) {
    let apiurl = `/inventario/modifica?col=${columna}&cant=${cantidad}`;
    if(furgon) {
        apiurl = `/inventario/modifica?col=${columna}&cant=${cantidad}&furgon=True`;
    }
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
    const apiurl = `/rutas/rutaactual/eliminarcliente/${ubicacion}`;
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
