from handlers.eliminaciones import RetirosEliminados, EliminacionRegistros
from helpers import constructor_paquete

def empaquetador_disposicion_final(request: object) -> map:
     paquete = constructor_paquete(request,"eliminaciones.html","Registros de eliminaciones")
     with EliminacionRegistros() as elimreg:
          paquete["registrosEliminaciones"] = elimreg.listar(retornostr=True)

     if "detalles" in request.form:
          pass

     return paquete
