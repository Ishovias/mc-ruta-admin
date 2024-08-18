from handlers.clientes import Clientes
from handlers.rutas import RutaActual
from helpers import mensajes

def new_cliente(data: list) -> bool:
    """Funcion para agregar cliente

    Args:
        data (list): Arreglo de datos a guardar, con orden especifico [rut, nombre, direccion, comuna, telefono, gps, otros]

    Returns:
        bool: Verdadero si se ejecuta correctamente el guardado, por el contrario dara Falso
    """
    with Clientes() as bd:
            if bd.nuevo_cliente(data):
                return True
            else:
                return False

def empaquetador_clientes(request: object) -> map:
    paquete = {"pagina":"clientes.html"}

    if "buscacliente" in request.form:
        
        resultados = ""
        with Clientes() as clientesbd:
            nombre = request.form.get("nombre")
            resultados = clientesbd.busca_cliente_lista(nombre)
        
        paquete["listaclientes"] = resultados
        
    elif "nuevocliente" in request.form: 
        paquete["pagina"] = "nuevoCliente.html"
    
    elif "guardanuevocliente" in request.form:
        data = [
            "activo",
            request.form.get("rut"),
            request.form.get("nombre"),
            request.form.get("direccion"),
            request.form.get("comuna"),
            request.form.get("telefono"),
            request.form.get("gps"),
            request.form.get("otros"),
            request.form.get("contrato")
            ]
        
        if new_cliente(data):
            paquete["alerta"] = mensajes.CLIENTE_GUARDADO.value
        else:
            paquete["alerta"] = mensajes.CLIENTE_GUARDADO_ERROR.value

    elif "modificaCliente" in request.form:
        resultados = ""
        with Clientes() as clientesbd:
            identificador = request.form.get("clienteSeleccion")
            resultados = clientesbd.busca_datoscliente(identificador,"rut")
        paquete["modificacion"] = resultados
    
    elif "aRuta" in request.form:
        fecha = None
        with RutaActual() as rutaactualbd:
            fecha = rutaactualbd.getFechaRuta()
        if not fecha:
            paquete["alerta"] = "Debes crear primero la ruta"
            paquete["nuevaruta"] = True
            paquete["pagina"] = "rutas.html"
        else:
            identificador = request.form.get("aRuta")
            
            cliente = []
            with Clientes() as clientesbd:
                cliente = clientesbd.busca_datoscliente(identificador,"rut")
                cliente.remove(cliente[0]) # olculta eliminando el indicador estado del cliente, innecesario para lista de ruta

            aruta = False
            with RutaActual() as rutaactualbd:
                aruta = rutaactualbd.agregar_a_ruta(fecha, cliente)

            if aruta:
                paquete["alerta"] = mensajes.CLIENTE_A_RUTA.value
            else:
                paquete["alerta"] = mensajes.CLIENTE_EN_RUTA.value
                
    
    elif "darbaja" in request.form:
        dadobaja = False
        guardado = False
        
        with Clientes() as clientesbd:
            identificador = request.form.get("rut")
            dadobaja = clientesbd.estado_cliente(identificador,"de baja")

        if dadobaja and guardado:
            paquete["alerta"] = mensajes.CLIENTE_BAJA.value
        else:
            paquete["alerta"] = mensajes.CLIENTE_BAJA_ERROR.value
            
    
    elif "guardamod" in request.form:
        rut = request.form.get("rut")
        data = [
            rut,
            request.form.get("nombre"),
            request.form.get("direccion"),
            request.form.get("comuna"),
            request.form.get("telefono"),
            request.form.get("gps"),
            request.form.get("otros")
            ]
        
        guardado = False
        grabado = False
        
        with Clientes() as bd:
            guardado = bd.guardar_modificacion(rut,data)

        if guardado and grabado:
            paquete["alerta"] = mensajes.CLIENTE_GUARDADO.value
        else:
            paquete["alerta"] = mensajes.CLIENTE_GUARDADO_ERROR.value

    return paquete