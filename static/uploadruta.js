import { URL_BASE as urlBase } from './config.js';

const form = document.getElementById('uploadForm');

form.addEventListener('submit', function(e) {
    e.preventDefault();
    const apiUrl = `${urlBase}/uploadRuta`;
    const boton = e.target.querySelector('#btn-uploadRuta')
    boton.textContent = "Espere...";
    boton.disabled = true;
    const formData = new FormData();
    const fileInput = document.getElementById('fileInput');
    formData.append('file', fileInput.files[0]);
    fetch(apiUrl, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            if (data.resultado) {
                window.location.href = `${urlBase}/rutas/rutaactual`;
            } 
            boton.textContent = "Upload";
            boton.disabled = false;
        })
        .catch(error => {
            alert("Error en peticion: "+error);
            window.location.href = `${urlBase}/rutas/rutaactual`;
        });
});
