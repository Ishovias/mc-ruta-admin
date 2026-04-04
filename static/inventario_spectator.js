
function getStock() {
    const apiUrl = `/inventario/getstock`;
    fetch(apiUrl)
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
        areaStock.innerHTML += "<br><br><hr><hr><br><br>";
        // LISTA DE STOCK DEL FURGON
        areaStock.innerHTML += "<h3>Stock en Furgon</h3>";
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
        console.log(error);
    });
}

getStock();
