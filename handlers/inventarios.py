from bd.repository import bdmediclean
from helpers import cimprime
import params

class Inventario(bdmediclean):
     
     def __init__(self) -> None:
          super().__init__(params.INVENTARIOS)

     def getStockActual(self) -> map:
          datos = {}
          
          columnasSeleccionadas = list(params.INVENTARIOS["columnas"].keys())
          columnasSeleccionadas.remove(columnasSeleccionadas[0])
          columnasSeleccionadas.remove(columnasSeleccionadas[-1])

          nombresColumnas = params.INVENTARIOS["encabezados_nombre"].copy()
          nombresColumnas.remove(nombresColumnas[0])
          nombresColumnas.remove(nombresColumnas[0])
          
          for columna in columnasSeleccionadas:
               dato = super().getDato(
                    fila=params.INVENTARIOS["filaStockActual"],
                    columna=columna
               )
               i = columnasSeleccionadas.index(columna)
               datos[nombresColumnas[i]] = {"stock":dato,"columna":columna}

          return datos

     def modificaStock(self, elemento: str, modificacion: int) -> bool:
          if elemento not in params.INVENTARIOS["columnas"]:
               return False
          filaStock = self.hoja_actual["filaStockActual"]
          cantidadActual = super().getDato(
               fila=filaStock,
               columna=elemento
          )
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