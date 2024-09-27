from handlers.sublitote import SublitoteCotizacion, SublitoteCotizacionesReg, SublitoteProductos, SublitoteCotizacionesBD
from helpers import constructor_paquete, formatear_precio
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
        codigo = request.form.get("codigo") if request.form.get("codigo") else request.form.get("cotizar")
        producto = []
        with SublitoteProductos() as stp:
            ubicacionProducto = stp.busca_ubicacion(
                dato=codigo,
                columna="codigo"
                )
            producto = stp.getDato(
                fila=ubicacionProducto,
                columnas=[
                    params.ST_PRODUCTOS["columnas"]["codigo"],
                    params.ST_PRODUCTOS["columnas"]["producto"],
                    params.ST_PRODUCTOS["columnas"]["precioventa"],
                    ]
                )
        if request.form.get("cotizar") == "cotizarenviar":
            precioventa = request.form.get("precioventa")
            cantidad = request.form.get("cantidad")
            precio = request.form.get("precio")
            with SublitoteCotizacion() as stc:
                nuevacotizacion = False
                if not stc.cotizacion_existente():
                    numcotizacion = stc.nueva_cotizacion(retornoid=True)
                    nuevacotizacion = True
                filaCotizacion = stc.busca_ubicacion(columna="item")
                producto[2] = precioventa
                producto.append(cantidad)
                producto.append(precio)
                producto.insert(0,stc.id_item())
                if stc.putDato(datos=producto,fila=filaCotizacion,columna="item"):
                    paquete["alerta"] = f"Producto agregado a nueva cotizacion ({numcotizacion})" if nuevacotizacion else "Producto agregado a cotizacion actual"
                else:
                    paquete["alerta"] = "Error al intentar ingresar producto en cotizacion"
        else:
            paquete["pagina"] = "st_cotizardetalle.html"
            paquete["codigo"] = codigo
            paquete["producto"] = producto[1]
            paquete["precioventa"] = producto[2]
            
    return paquete

def pack_st_cotizacion(request: object) -> map:
    paquete = constructor_paquete(request, "st_cotizacion.html", "Cotizacion")
    
    def mostrar_cotizacion(claseBD: object, paquete: map) -> map:
        paquete["listacotizacion"] = claseBD.listar()
        paquete["numcotizacion"] = claseBD.getDato(identificador="numcotizacion")
        paquete["totalcotizacion"] = formatear_precio(claseBD.obtener_total_cotizacion())
        return paquete
    
    with SublitoteCotizacion() as stc:
        paquete = mostrar_cotizacion(stc,paquete)

    if "creacotizacion" in request.form:
        with SublitoteCotizacion() as stc:
            nuevaCotizacion = stc.nueva_cotizacion(retornoid=True)
            if nuevaCotizacion:
                paquete["alerta"] = f"Nueva cotizacion creada: ID - {nuevaCotizacion}"
                paquete = mostrar_cotizacion(stc,paquete)

    if "eliminacotizacion" in request.form:
        with SublitoteCotizacion() as stc:
            stc.eliminarContenidos()
            stc.putDato(dato="", identificador="numcotizacion")
            paquete["alerta"] = "Cotizacion eliminada"
            paquete = mostrar_cotizacion(stc,paquete)
    
    if "guardacotizacion" in request.form:
        ncotizacion = request.form.get("guardacotizacion")
        descripcion = request.form.get("descripcion")
        with SublitoteCotizacion() as stc:
            datos = stc.listar(solodatos_list=True)
            precio = stc.obtener_total_cotizacion()
            stc.eliminarContenidos()
            stc.putDato(dato="", identificador="numcotizacion")
            paquete = mostrar_cotizacion(stc,paquete)
        with SublitoteCotizacionesBD() as stbd:
            guardado = stbd.guardar_cotizacion(idcotizacion=ncotizacion, datos=datos):
        with SublitoteCotizacionesReg() as stcreg:
             registrado = stcreg.registra(
                  idcotizacion=ncotizacion,
                  descripcion=descripcion,
                  precio=precio
                  )
             if guardado and registrado:
                paquete["alerta"] = f"Cotizacion {ncotizacion} guardada"
            else:
                paquete["alerta"] = f"ERROR no se pudo guardar cotizacion GUARDADO:{ncotizacion} REGISTRADO:{registrado}"

    if "eliminaitem" in request.form:
        item = request.form.get("eliminaitem")
        with SublitoteCotizacion() as stc:
            ubicacion = stc.busca_ubicacion(dato=item,columna="item")
            stc.eliminar(ubicacion)
            stc.id_item(reasignartodo=True)
            paquete = mostrar_cotizacion(stc,paquete)
    
    return paquete