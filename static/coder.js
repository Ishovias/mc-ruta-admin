import { URL_BASE as urlBase } from './config.js'
let temporizador;
document.getElementById('frase').addEventListener('input', (e) => {
    if (e.target.value != "") {
        const tipoCoder = document.getElementById('tipoaccion');
        let coder = '/coder2/frdec?fr=';
        if (tipoCoder.value == "coder1") {
            coder = '/coder1/frcod?fr=';
        } else if (tipoCoder.value == "coder2cod") {
            coder = '/coder2/frcod?fr=';
        }
        const apiUrl = `${urlBase}${coder}${encodeURIComponent(e.target.value)}`;
        clearTimeout(temporizador); // Limpia el temporizador anterior
        temporizador = setTimeout(() => {
            fetch(apiUrl)
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
