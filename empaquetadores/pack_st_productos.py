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
            ubicacion = stp.buscapartedato(
                columna=params.ST_PRODUCTOS["columnas"]["producto"],
                dato=datoBuscado
            )
            paquete["listaproductos"] = stp.getDato(
                fila=ubicacion,
                columna="todas",
                retornostr=True
            )
    
    if "nuevoproducto" in request.form:
        with SublitoteProductos() as stp:
            paquete["codigoNuevo"] = stp.nuevo_codigo()
        paquete["pagina"] = "st_nuevoproducto.html"

    if "guardaproducto" in request.form:
        with SublitoteProductos() as stp:
            guardadoproducto = stp.nuevo_producto(
                 codigo = request.form.get("codigo"),
                 retornaFila = True,
                 retornaCodigo = True,
                 producto = request.form.get("producto"),
                 preciocosto = request.form.get("preciocosto"),
                 precioventa = request.form.get("precioventa"),
                 existencias = request.form.get("existencias"),
                 observaciones = request.form.get("observaciones")
                 )
            msg = f"Nuevo producto guardado con el codigo {guardadoproducto['codigo']}" if guardadoproducto else f"ERROR al intentar guardar nuevo producto"
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
    
    return paquete