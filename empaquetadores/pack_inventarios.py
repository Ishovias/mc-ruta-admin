from handlers.inventarios import Inventario
from helpers import constructor_paquete, cimprime
import params

def empaquetador_inventarios(request: object) -> map:
     paquete = constructor_paquete(request,"inventarios.html","Inventarios PDLK-25")
     def defaultPage(paquete: map) -> map:
          with Inventario() as inv:
               paquete["listainventarios"] = inv.listar()
               if paquete["listainventarios"]["encabezados"][0] == None:
                    columnasNombres = params.INVENTARIOS["encabezados_nombre"].copy()
                    columnasNombres.remove(columnasNombres[0])
                    paquete["listainventarios"]["encabezados"] = columnasNombres
               paquete["stockActual"] = inv.getStockActual()
          return paquete
     
     if "nuevoinventario" in request.form:
          elemento = list(params.INVENTARIOS["columnas"])
          itemsNombres = params.INVENTARIOS["encabezados_nombre"].copy()
          
          elemento.remove(elemento[0])
          elemento.remove(elemento[-1])
          itemsNombres.remove(itemsNombres[0])
          itemsNombres.remove(itemsNombres[0])
          
          elementos = {}
          for e in elemento:
               i = elemento.index(e)
               elementos[e] = itemsNombres[i]
          
          paquete["pagina"] = "nuevoinventario.html"
          paquete["elementos"] = elementos
     
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
     
     paquete = defaultPage(paquete)
     
     return paquete