from handlers.sublitote import SublitoteCotizacion, SublitoteProductos
from helpers import constructor_paquete
from cimprime import cimprime
import params


def pack_st_productos(request: object) -> map:
    paquete = constructor_paquete(request,"st_productos.html","Lista de productos")
    
    with SublitoteProductos() as stp:
        paquete["listaproductos"] = stp.listar_productos()
    
    if "buscaproducto" in request.form:
        datoBuscado = request.form.get("busqueda")
        with SublitoteProductos() as stp:
            listadoproductos = {
                "encabezados":stp.getDato(
                    fila=params.ST_PRODUCTOS["encabezados"],
                    columnas=params.ST_PRODUCTOS["columnas"]["todas"]
                ),
                "datos":[]
            }
            ubicaciones = stp.buscapartedato(
                filainicio=params.ST_PRODUCTOS["filainicial"],
                columna=params.ST_PRODUCTOS["columnas"]["producto"],
                dato=datoBuscado
            )
            for fila in ubicaciones:
                datosproductos = stp.getDato(
                    fila=fila,
                    columnas=params.ST_PRODUCTOS["columnas"]["todas"],
                    retornostr=True
                )
                listadoproductos["datos"].append(datosproductos)
            items = 0
            for fila in listadoproductos["datos"]:
                items += 1
                fila.insert(0,items)
                
        paquete["listaproductos"] = listadoproductos

    if "nuevoproducto" in request.form:
        with SublitoteProductos() as stp:
            paquete["codigoNuevo"] = stp.nuevo_codigo()
        paquete["pagina"] = "st_nuevoproducto.html"
        paquete["nombreFormulario"] = "Formulario de NUEVO producto"
        paquete["accionproducto"] = "nuevo producto"
        paquete["accionformulario"] = "nuevoproducto"

    if "guardaproducto" in request.form:
        with SublitoteProductos() as stp:
            if request.form.get("guardaproducto") == "nuevoproducto":
                guardadoproducto = stp.nuevo_producto(
                    codigo = request.form.get("codigo"),
                    retornaFila = True,
                    retornaCodigo=True,
                    producto = request.form.get("producto"),
                    preciocosto = request.form.get("preciocosto"),
                    precioventa = request.form.get("precioventa"),
                    existencias = request.form.get("existencias"),
                    observaciones = request.form.get("observaciones")
                    )
            elif request.form.get("guardaproducto") == "modificacion":
                guardadoproducto = stp.modifica_producto(
                    codigo=request.form.get("codigo"),
                    retornaFila=True,
                    producto=request.form.get("producto"),
                    preciocosto=request.form.get("preciocosto"),
                    precioventa=request.form.get("precioventa"),
                    existencias=request.form.get("existencias"),
                    observaciones=request.form.get("observaciones")
                    )
                guardadoproducto = {"codigo":request.form.get("codigo"),"ubicacion":guardadoproducto} if guardadoproducto else None
            msg = f"Producto codigo {guardadoproducto['codigo']} guardado" if guardadoproducto else "ERROR al intentar guardar"
            paquete["alerta"] = msg
            if guardadoproducto:
                productonuevo = {
                    "encabezados":stp.getDato(
                        fila=params.ST_PRODUCTOS["encabezados"],
                        columnas=params.ST_PRODUCTOS["columnas"]["todas"]
                        ),
                    "datos":[stp.getDato(
                        fila=guardadoproducto["ubicacion"],
                        columnas=params.ST_PRODUCTOS["columnas"]["todas"],
                        retornostr=True
                        )]
                }
                productonuevo["datos"][0].insert(0,1)
                paquete["listaproductos"] = productonuevo
                    
    if "modificarproducto" in request.form:
        codigoProducto = request.form.get("modificarproducto")
        paquete["pagina"] = "st_nuevoproducto.html"
        paquete["nombreFormulario"] = "Formulario MODIFICAR cliente"
        paquete["codigoNuevo"] = codigoProducto
        paquete["accionproducto"] = "modificacion"
        paquete["accionformulario"] = "modificacion"
        with SublitoteProductos() as stp:
            ubicacion = stp.busca_ubicacion(dato=codigoProducto,columna="codigo")
            paquete["modproducto"] = {
                "producto":stp.getDato(fila=ubicacion,columna="producto"),
                "preciocosto":stp.getDato(fila=ubicacion,columna="preciocosto"),
                "precioventa":stp.getDato(fila=ubicacion,columna="precioventa"),
                "existencias":stp.getDato(fila=ubicacion,columna="existencias"),
                "observaciones":stp.getDato(fila=ubicacion,columna="observaciones")
            }
    
    if "eliminarproducto" in request.form:
        with SublitoteProductos() as stp:
            codigo = request.form.get("eliminarproducto")
            msg = f"Producto {codigo} eliminado" if stp.elimina_producto(codigo) else f"Error al intentar eliminar producto {codigo}"
            paquete["alerta"] = msg
            paquete["listaproductos"] = stp.listar_productos()

    if "cotizar" in request.form:
        codigo = request.form.get("cotizar")
        with SublitoteCotizacion() as stc:
            nuevacotizacion = False
            if not stc.cotizacion_existente():
                numcotizacion = stc.nueva_cotizacion(retornoid=True)
                nuevacotizacion = True
            with SublitoteProductos() as stp:
                ubicacionProducto = stp.busca_ubicacion(
                    dato=codigo,
                    columna="codigo"
                    )
                producto = stp.getDato(
                    fila=ubicacionProducto,
                    columna=params.ST_PRODUCTOS["columnas"]["todas"]
                    )
            producto.insert(0,stc.id_item())
            if stc.putDato(datos=producto,columna="item"):
                paquete["alerta"] = f"Producto agregado a nueva cotizacion ({numcotizacion})" if nuevacotizacion else "Producto agregado a cotizacion actual"
            else:
                paquete["alerta"] = "Error al intentar ingresar producto en cotizacion"
            paquete["pagina"] = "st_cotizacion.html"

    return paquete

def pack_st_cotizacion(request: object) -> map:
    paquete = constructor_paquete(request, "st_cotizacion.html", "Cotizacion")

    with SublitoteCotizacion() as stc:
        paquete["listacotizacion"] = stc.listar()
        paquete["numcotizacion"] = stc.getDato(identificador="numcotizacion")

    if "creacotizacion" in request.form:
        with SublitoteCotizacion() as stc:
            nuevaCotizacion = stc.nueva_cotizacion(retornoid=True)
            if nuevaCotizacion:
                paquete["alerta"] = f"Nueva cotizacion creada: ID - {nuevaCotizacion}"
                paquete["listacotizacion"] = stc.listar()
                paquete["numcotizacion"] = stc.getDato(identificador="numcotizacion")

    if "eliminacotizacion" in request.form:
        with SublitoteCotizacion() as stc:
            stc.eliminarContenidos()
            stc.putDato(dato="", identificador="numcotizacion")
            paquete["alerta"] = "Cotizacion eliminada"
            paquete["listacotizacion"] = stc.listar()
            paquete["numcotizacion"] = stc.getDato(identificador="numcotizacion")
            
    return paquete