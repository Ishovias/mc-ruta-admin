from handlers.sublitote import SublitoteProductos
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
                 guardadoproducto = {"codigo":request.form.get("codigo"),"ubicacion":guardadoproducto}
            msg = f"Producto codigo {guardadoproducto["codigo"]} guardado " if guardadoproducto else f"ERROR al intentar guardar"
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
    
    return paquete