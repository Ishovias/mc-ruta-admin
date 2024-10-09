from handlers.inventarios import Inventario
from helpers import constructor_paquete

def empaquetador_inventarios(request: object) -> map:
    paquete = constructor_paquete(request,"inventarios.html","Inventarios PDLK-25")
    def defaultPage(paquete: map) -> map:
         with Inventario() as inv:
             paquete["listainventarios"] = inv.listar()
             paquete["ultimoinventario"] = inv.getUltimoInventario()
         return paquete
    
    paquete = defaultPage(paquete)
    
    if "nuevoinventario" in request.form:
         paquete["pagina"] = "nuevoinventario.html"
    
     
    return paquete