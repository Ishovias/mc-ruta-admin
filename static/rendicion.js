
const btnCerrar = document.getElementById("btn-rendicion-cerrar");
btnCerrar.addEventListener('click', function(e){
    const fecha = btnCerrar.value;
    if(fecha != "vigente"){
        
    }
    btnCerrar.textContent = "espere confirmacion...";
    btnCerrar.disabled = true;
    alert(fecha);
    const url = `/gastos/rendir/${fecha}`;
    fetch(url, {
        method:"PATCH"
    })
        .then(response => response.json())
        .then(data => {
            if(!data.resultado){
                alert("Error en backend");
            }
            window.location.href = `/gastos`;
        }).catch(error => {
            alert(`Error en gastos/btnCerrar/fetch: ${error}`);
        });
});

