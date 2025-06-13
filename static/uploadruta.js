import { URL_BASE as urlBase } from './config.js';

document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const apiUrl = `${urlBase}/uploadRuta`;
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
        })
        .catch(error => {
            alert("Error en peticion: "+error);
        });
});
