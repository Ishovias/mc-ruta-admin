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

    def modifica_stock(self, columna: str, modificacion: int, sobrescribe: bool=False) -> bool:
        if columna not in self.hoja_actual["columnas"].keys():
            return False
        filaStock = self.hoja_actual["filaStockActual"]
        cantidadActual = super().getDato(
            fila=filaStock,
            columna=columna
            )
        cantidadActual = cantidadActual if cantidadActual else 0
        nuevaCantidad = int(cantidadActual) + modificacion 
        datoainsertar = nuevaCantidad if not sobrescribe else modificacion
        super().putDato(
            dato=datoainsertar,
            fila=filaStock,
            columna=columna
            )
        return True

    def actualizar_stock(self, inventario: map) -> bool:
        for columna, valor in inventario.items():
            super().putDato(
                dato=valor["dato"],
                fila=params.INVENTARIOS["filaStockActual"],
                columna=columna
                )
        else:
            return True
        return False

