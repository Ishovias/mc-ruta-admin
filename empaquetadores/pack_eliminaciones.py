from handlers.eliminaciones import RetirosEliminados, EliminacionRegistros
from helpers import constructor_paquete

def empaquetador_eliminaciones(request: object) -> map:
     paquete = constructor_paquete(request,"eliminaciones.html","Registros de eliminaciones")
     with EliminacionRegistros() as elimreg:
          paquete["registrosEliminaciones"] = elimreg.listar(retornostr=True)

     return paquete