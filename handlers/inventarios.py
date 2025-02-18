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

    def modificaStock(self, columna: str, modificacion: int) -> bool:
        if columna not in params.INVENTARIOS["columnas"]:
            return False
        filaStock = self.hoja_actual["filaStockActual"]
        cantidadActual = super().getDato(
            fila=filaStock,
            columna=columna
            )
        cantidadActual = cantidadActual if cantidadActual else 0
        super().putDato(
            dato=int(cantidadActual) + modificacion,
            fila=filaStock,
            columna=columna
            )
        return True

    def actualizarStock(self, inventario: map) -> bool:
        for columna, valor in inventario.items():
            super().putDato(
                dato=valor["dato"],
                fila=params.INVENTARIOS["filaStockActual"],
                columna=columna
                )
        else:
            return True
        return False

