from bd.repository import bdmediclean
from datetime import date, timedelta, datetime
from cimprime import cimprime
from utils import fecha_formato, fecha_actual, formato_moneda
import params


class Gastos(bdmediclean):

    def __init__(self) -> None:
        super().__init__(params.GASTOS_BD)# {{{
        self.fechacodigo_actual = fecha_actual()
        self.fecha_buscada = None
        self.filas_halladas = None# }}}

    def get_campos(self) -> dict:
        campos = self.hoja_actual["columnas"].copy()# {{{
        del campos["vigencia"]
        del campos["diferencia"]
        return campos# }}}

    def get_filas_fecha(self, fecha: str=None) -> list:
        columna = "fecha" if fecha else "vigencia"# {{{
        fecha = fecha if fecha else "vigente"
        return super().buscadato(
                dato=fecha,
                columna=columna,
                buscartodo=True
                )# }}}

    def get_data(self, fecha: str=None) -> dict:
        filas = self.get_filas_fecha(fecha)#{{{
        if filas == []:
            return None
        columnas_mostrar = self.hoja_actual["ncolumnas_mostrar"]
        datos = super().listar(filas=filas, columnas=columnas_mostrar, idy=True)
        fechas_halladas = []
        for fila in datos["datos"]:
            ubicacion = columnas_mostrar.index("monto")
            fila[ubicacion] = formato_moneda(fila[ubicacion])
            fecha_hallada = fila[columnas_mostrar.index("fecha")]
            if fecha_hallada not in fechas_halladas:
                fechas_halladas.append(fecha_hallada)
        self.fecha_buscada = fechas_halladas
        return datos# }}}

    def get_diferencia_anterior(self, fecha: str=None, filas_halladas: list=None) -> str:
        if filas_halladas:# {{{
            fila_ant = filas_halladas[0]-1
            if fila_ant < self.hoja_actual.get("filainicial"):
                return None
            return super().getDato(fila=fila_ant,columna="diferencia")
        if not fecha and not self.fecha_buscada:
            return None
        fecha = fecha if fecha else self.fecha_buscada
        if filas_halladas:
            filas = filas_halladas
        else:
            filas = self.filas_halladas \
                    if self.filas_halladas \
                    else super().buscadato(
                            dato=fecha,
                            columna="fecha",
                            buscartodo=True
                            )
        return super().getDato(fila=filas[0]-1,columna="diferencia")# }}}

    def get_totales(self, fecha: str=None) -> str:
        filas = self.get_filas_fecha(fecha)#{{{
        gastos = 0
        abonos = 0
        for fila in filas:
            dato = int(super().getDato(fila=fila,columna="monto"))
            if dato > 0:
                abonos += dato
            elif dato < 0:
                gastos += dato
        dif = self.get_diferencia_anterior(filas_halladas=filas)
        diff = 0 if not dif else dif
        diferencia_anterior = formato_moneda(diff)
        diferencia = formato_moneda(abonos + gastos + diff)
        return {
                "gastos":formato_moneda(gastos),
                "abonos":formato_moneda(abonos),
                "diferencia":diferencia,
                "diferencia_anterior":diferencia_anterior
                }# }}}

    def get_fechas(self, filas: list=None, data: list=None, formatear: bool=True) -> list:
        data = super().listar(# {{{
                filas=filas,
                columnas=["fecha"],
                solodatos=True
                ) if not data else data
        recoleccion = []
        recoleccion_formateada = []
        for fila in data:
            if fila[0] not in recoleccion:
                if formatear:
                    date = fecha_formato(fila[0],"codigo","vista")
                    recoleccion_formateada.append([fila[0],date])
                recoleccion.append(fila[0])
        return recoleccion if not formatear else recoleccion_formateada# }}}

    def add_gasto(self, datos: dict, fila: int=None) -> bool:
        columnas = self.hoja_actual["columnas"]# {{{
        fila = fila if fila else super().buscafila()
        try:
            for columna in columnas:
                dato = datos.get(columna)
                if columna == "fecha":
                    dato = fecha_formato(dato,"explorador","codigo")
                if dato:
                    super().putDato(
                            dato=dato,
                            columna=columna,
                            fila=fila
                            )
            super().putDato(
                    dato="vigente",
                    fila=fila,
                    columna="vigencia"
                    )
        except Exception as e:
            cimprime(titulo="Error en add_gasto:", error=e)
            return False
        else:
            return True# }}}

    def verificar_rendido(self, fecha: str) -> bool:
        self.fecha_buscada = fecha# {{{
        filas = super().buscadato(
                dato=fecha,
                columna="fecha",
                buscartodo=True
                )
        dato = super().getDato(
                fila=filas[0],
                columna="vigencia"
                )
        if dato == "rendido":
            return True
        self.filas_halladas = filas
        return False# }}}

    def rendir(self, fecha: str=None, cerrar: bool=True) -> list:
        filas = self.get_filas_fecha(fecha) #{{{
        if cerrar:
            try:
                for fila in filas:
                    super().putDato(
                            fila=fila,
                            columna="vigencia",
                            dato="rendido"
                            )
            except Exception as e:
                print(f"Error al cerrar rendicion (handlers/gastos/rendir): {e}")
                return False
            else:
                super().putDato(
                        dato=self.get_totales(fecha).get("diferencia"),
                        fila=filas[-1],
                        columna="diferencia"
                        )
                return True
        self.datos_buscados = super().listar(filas=filas,
                columnas=self.hoja_actual.get("ncolumnas_mostrar"),
                solodatos=True
                )
        return self.datos_buscados# }}}


