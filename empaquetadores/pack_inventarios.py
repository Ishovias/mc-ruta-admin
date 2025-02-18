from handlers.inventarios import Inventario
from helpers import constructor_paquete, cimprime
import params

def empaquetador_inventarios(request: object) -> map:
    paquete = constructor_paquete(request,"inventarios.html","Inventarios PDLK-25")

    def datos_base():
        with Inventario() as inv:
            paquete["listainventarios"] = inv.listar()
            stock = inv.mapdatos()
            del stock["fecha"]
            paquete["stockActual"] = stock

    if "nuevoinventario" in request.form:
        with Inventario() as inv:
            elementos = inv.mapdatos()
            del elementos["fecha"]
            paquete["elementos"] = elementos
        paquete["pagina"] = "nuevoinventario.html"

    elif "enviarinventario" in request.form:
        with Inventario() as inv:
            nuevaUbicacion = inv.busca_ubicacion(columna="fecha")
            actualizacionInv = {}
            for columna in params.INVENTARIOS["columnas"].keys():
                if columna == "todas":
                    break
                dato = request.form.get(columna)
                inv.putDato(dato=dato,fila=nuevaUbicacion,columna=columna)
                actualizacionInv[columna] = dato
            if inv.actualizarStock(actualizacionInv):
                paquete["alerta"] = "Inventario grabado y Stock actualizado"

    else:
        datos_base()

    return paquete
