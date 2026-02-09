let temporizador;
document.getElementById('frase').addEventListener('input', (e) => {
    if (e.target.value != "") {
        const datos = {
            frase: e.target.value,
            clave: document.getElementById('clave').value
        };
        const apiUrl = `/enicod`;
        clearTimeout(temporizador); // Limpia el temporizador anterior
        temporizador = setTimeout(() => {
            fetch(apiUrl, {
                "method": "post",
                "headers": {
                    'Content-Type':'application/json'
                },
                "body": JSON.stringify(datos)
            })
                .then(response => response.json())
                .then(data => {
                    const contenedor = document.getElementById('frproc');
                    contenedor.textContent = data.frproc;
                })
                .catch(error => {
                    console.error("Error:", error);
                    alert(error)
                    document.getElementById('frproc').textContent = "Error en datos";
                });
        }, 1000);
    }
});
