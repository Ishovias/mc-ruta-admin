from bd.repository import bdmediclean
from helpers import cimprime
import params

class Inventario(bdmediclean):
     
     def __init__(self) -> None:
          super().__init__(params.INVENTARIOS)

     def getUltimoInventario(self) -> list:
          datos = super().getDato(
               fila=params.INVENTARIOS["filaStockActual"],
               columnas=params.INVENTARIOS["columnas"]["todas"]
          )
          return datos
