from bd.repository import bdmediclean
from datetime import date, timedelta
from handlers.rutas import RutaActual
from helpers import mensajes
import params

class Clientes(bdmediclean):

    def __init__(self) -> None:
        super().__init__(params.CLIENTES)

    def busca_cliente_lista(self, nombre: str) -> map:
        filainicio = self.hoja_actual["filainicial"]
        columna = self.hoja_actual["columnas"]["cliente"]
        filas = super().buscapartedato(filainicio,columna,nombre)
        col = self.hoja_actual["columnas"]["todas"]
        resultados = {}
        resultados["encabezados"] = super().extraefila(fila=1,columnas=col)
        resultados["datos"] = []
        for fila in filas:
            data = super().extraefila(fila=fila,columnas=col)
            resultados["datos"].append(data)
        return resultados

    def nuevo_cliente(self, data: list) -> bool:
        existencia = super().busca_datoscliente(data[1])
        if existencia != 0:
            return False
        fila = super().buscafila(
            self.hoja_actual["filainicial"],
            self.hoja_actual["columnas"]["rut"],
            )
        super().ingresador(fila,data,1)
        return True
    
    def busca_datoscliente(self, nombre: str, filtro: str="cliente") -> list:
        ubicacion = super().buscadato(
            self.hoja_actual["filainicial"],
            self.hoja_actual["columnas"][filtro],
            nombre
            )
        if ubicacion == 0:
            return 0
        datos = super().extraefila(
            fila=ubicacion,
            columnas=self.hoja_actual["columnas"]["todas"]
            )
        return datos
    
    def estado_cliente(self, rut: str, estado: str) -> bool:
        ubicacion = super().busca_ubicacion(rut,"rut")
        try:
            super().ingresador(
                ubicacion,
                [estado],
                [self.hoja_actual["columnas"]["estado"]]
                )
        except:
            return False
        else:
            return True
            
    def proximo_retiro(self, rut: str, fecharetiro: str) -> str:
        diascontrato = super().getDato(
            fila=super().busca_ubicacion(
                dato=rut,
                columna="rut"
                ),
            columna="diascontrato"
            )
        
        if not diascontrato:
            return None
        
        try:
            int(diascontrato)
        except Exception as e:
            print(e)
            return None
        else:
            lapso = timedelta(diascontrato + 2)
        
        fecharetiro = date.fromisoformat(fecharetiro)
        proxretiro = date.isoformat(fecharetiro + lapso)
        return proxretiro
        
    def guardar_modificacion(self, rut: str, data: list) -> bool:
        fila = super().busca_ubicacion(rut,"rut")
        try:
            super().ingresador(fila,data,2)
        except:
            return False
        else:
            return True

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
            request.form.get("otros")
            ]
        
        with Clientes() as bd:
            if bd.nuevo_cliente(data):
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