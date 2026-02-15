from bd.repository import bdmediclean
from cimprime import cimprime
import params

class Inventario(bdmediclean):

    def __init__(self) -> None:
        super().__init__(params.INVENTARIOS)

    def get_stock(self) -> list:
        columnas = list(self.hoja_actual["columnas"].keys())# {{{
        columnas.remove("fecha")
        columnas.remove("id")
        resultado = []
        for columna in columnas:
            resultado.append([
                columna,
                self.hoja_actual["columnas"][columna]["encabezado"],
                super().getDato(
                    fila=self.hoja_actual.get("filaStockActual"),
                    columna=columna
                    )
                ])
        return resultado# }}}

    def registra_movimiento(self, datos: dict) -> None:
        columnas = self.hoja_actual["columnas_ruta"].copy()# {{{
        fila = super().buscafila()
        fila_stock = self.hoja_actual.get("filaStockActual")
        for columna in columnas:
            if columna in datos.keys():
                dato = datos.get(columna)
                super().putDato(
                        dato=dato,
                        fila=fila,
                        columna=columna
                        )
                modificacion_stock = super().getDato(
                        fila=fila_stock,
                        columna=columna
                        )
                if modificacion_stock:
                    modificacion_stock = int(modificacion_stock) - int(dato)
                else:
                    modificacion_stock = 0
                super().putDato(
                        dato=modificacion_stock,
                        fila=fila_stock,
                        columna=columna
                        )
        for columna in ["fecha","id"]:
            super().putDato(
                    dato=datos.get(columna),
                    fila=fila,
                    columna=columna
                    )# }}}

    def modifica_stock(self, cantidad: str, columna: str) -> None:
        super().putDato(# {{{
                dato=int(cantidad),
                fila=self.hoja_actual.get("filaStockActual"),
                columna=columna
                )# }}}

    def reversa_stock(self, fecha: str, id_cliente: str) -> None:
        filas = super().buscadato(# {{{
                dato=fecha,
                columna="fecha",
                buscartodo=True
                )
        fila.reverse()
        for fila in filas:
            idleido = super().getDato(
                    fila=fila,
                    columna="id"
                    )
            if idleido == id_cliente:
                columnas = self.hoja_actual.get("columnas_ruta")
                fila_stock = self.hoja_actual.get("filaStockActual")
                for columna in columnas:
                    dato = super().getDato(
                        fila=fila,
                        columna=columna
                        )
                    if dato:
                        stock_actual = super().getDato(
                            fila=fila_stock,
                            columna=columna
                            )
                        stock_actual = int(stock_actual) + int(dato)# }}}
