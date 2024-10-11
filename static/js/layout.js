function alerta(mensaje){
    alert(mensaje)
};

function calcula_inventario(idValorActual, idValorSumando) {
    event.preventDefault();

    const valorActual = document.getElementById(idValorActual);
    const valorSumando = document.getElementById(idValorSumando);
    
    const sumando = parseInt(valorSumando.value);
    const cantidadactual = parseInt(valorActual.value);
    const calculo = cantidadactual + sumando;
    return calculo;
};