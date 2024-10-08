from bd.repository import bdmediclean
import params

class Inventario(bdmediclean):
     
     def __init__(self) -> None:
          super().__init__(params.INVENTARIOS)

     def getUltimoInventario(self) -> list:
          ubicacion = super().busca_ubicacion(columna="fecha") - 1
          datos = super().getDato(
               fila=ubicacion,
               columnas=params.INVENTARIOS["columnas"]["todas"]
          )
          return datos
