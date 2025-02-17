from bd.repository import bdmediclean
from helpers import cimprime
import params

class Inventario(bdmediclean):

    def __init__(self) -> None:
        super().__init__(params.INVENTARIOS)

    def getStockActual(self, columnas: list=None) -> map:
        if columnas and type(columnas) == str:
            columnas = [columnas]
        elif not columnas:
            columnas = list(self.hoja_actual["columnas"].keys())
        datos = super().mapdatos(
                fila="filaStockActual",
                columnas=columnas
                )
        return datos

     def modificaStock(self, elemento: str, modificacion: int) -> bool:
          if elemento not in params.INVENTARIOS["columnas"]:
               return False
          filaStock = self.hoja_actual["filaStockActual"]
          cantidadActual = super().getDato(
               fila=filaStock,
               columna=elemento
          )
          cantidadActual = cantidadActual if cantidadActual else 0
          return super().putDato(
               dato=int(cantidadActual) + modificacion,
               fila=filaStock,
               columna=elemento
          )
          
     def actualizarStock(self, inventario: map) -> bool:
          for columna, valor in inventario.items():
               super().putDato(
                    dato=valor,
                    fila=params.INVENTARIOS["filaStockActual"],
                    columna=columna
                    )
          else:
               return True
          return False
     def obtenerInventario(self, fecha: str) -> map:
          columnas = list(params.INVENTARIOS["columnas"].keys())
          del(columnas["todas"])
          datos = {}
          ubicacion = super().busca_ubicacion(dato=fecha,columna="fecha")
          if not ubicacion:
               return None
          for columna in columnas:
               dato = super().getDato(
                    fila=ubicacion,
                    columna=columna
                    )
               if not dato:
                    dato = 0
               datos[columna] = dato
          else:
               return datos
          return None
