from handlers.sublitote import SublitoteProductos
from helpers import constructor_paquete


def pack_st_productos(request: object) -> map:
    paquete = constructor_paquete(request,"st_productos.html","Lista de productos")

    with SublitoteProductos() as stp:
        paquete["listaproductos"] = stp.listar_productos()
    
    return paquete