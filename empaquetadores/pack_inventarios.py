from handlers.inventarios import Inventario
from helpers import constructor_paquete

def empaquetador_inventarios(request: object) -> map:
    paquete = constructor_paquete(request,"inventarios.html","Inventarios PDLK-25")
    with Inventario() as inv:
        paquete["listainventarios"] = inv.listar()
        paquete["ultimoinventario"] = inv.getUltimoInventario()
    
    return paquete