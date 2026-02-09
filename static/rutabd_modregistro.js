
const form = document.getElementById('modificaRegistroForm')

form.addEventListener('submit', function(e){
    e.preventDefault();
    const formData = new FormData(form);
    const boton = e.target.querySelector('#btnSubmit')
    const idy = boton.value;
    boton.disabled = true;
    boton.textContent = "Espere...";
    const url = `/rutas/rutabd/modregistro/${idy}`;
    fetch(url, {
        "method":"put",
        "body":formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.resultado){
                window.location.href = document.referrer;
            } else {
                alert("Error en servidor o datos");
                boton.textContent = "Modificar";
                boton.disabled = false;
            }
        })
        .catch(error => {
            alert(`Error en fetch: {error} - {error.message}`)
            boton.textContent = "Modificar";
            boton.disabled = false;
        });
});
