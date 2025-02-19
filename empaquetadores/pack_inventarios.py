from handlers.inventarios import Inventario
from helpers import constructor_paquete, cimprime
import params

def empaquetador_inventarios(request: object) -> map:
    paquete = constructor_paquete(request,"inventarios.html","Inventarios PDLK-25")

    def datos_base():
        with Inventario() as inv:
            paquete["listainventarios"] = inv.listar()
            stock = inv.mapdatos(fila=inv.hoja_actual["filaStockActual"])
            del stock["fecha"]
            paquete["stockActual"] = stock

    if "nuevoinventario" in request.form:
        with Inventario() as inv:
            if request.form.get("nuevoinventario") == "formulario_respuesta":
                ubicacion = inv.busca_ubicacion(columna="fecha")
                actualizacionInv = {}
                for columna in params.INVENTARIOS["columnas"].keys():
                    dato = request.form.get(columna)
                    inv.putDato(dato=dato,fila=ubicacion,columna=columna)
                    actualizacionInv[columna] = dato
                if inv.actualizar_stock(actualizacionInv):
                    paquete["alerta"] = "Inventario grabado y Stock actualizado"
                datos_base()
            else:
                elementos = inv.mapdatos()
                del elementos["fecha"]
                paquete["elementos"] = elementos
                paquete["pagina"] = "nuevoinventario.html"

    elif "actualiza_stock_insummo" in request.form:
        cantidad = int(request.form.get("ajuste_stock"))
        columna = request.form.get("insumo")
        with Inventario() as inv:
            modificado = inv.modifica_stock(
                    columna=columna,
                    modificacion=cantidad,
                    sobrescribe=True
                    )
        cimprime(cantidad=cantidad,columna=columna,modificado=modificado)
        datos_base()

    else:
        datos_base()

    return paquete
