from handlers.eliminaciones import RetirosEliminados, EliminacionRegistros
from helpers import constructor_paquete

def empaquetador_eliminaciones(request: object) -> map:
     paquete = constructor_paquete(request,"eliminaciones.html","Registros de eliminaciones")
     