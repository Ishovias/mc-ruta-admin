from bd.repository import bdmediclean
import params

class SublitoteProductos(bdmediclean):

    def __init__(self) -> None:
        super().__init__(params.ST_PRODUCTOS)

    def listar_productos(self, nombre: str) -> map:
        filainicio = self.hoja_actual["filainicial"]
        columna = self.hoja_actual["columnas"]["codigo"]
        col = self.hoja_actual["columnas"]["todas"]
        resultados = super().listar()
        for fila in resultados["datos"]:
            data = super().extraefila(fila=fila,columnas=col)
            resultados["datos"].append(data)
        return resultados

    def nuevo_cliente(self, retornoFila: bool=False, **data) -> bool:
        existencia = super().busca_ubicacion(dato=data["cliente"])
        if existencia:
            return False
        fila = super().busca_ubicacion(columna="rut")
        for dato in data.keys():
            super().putDato(dato=data[dato], fila=fila, columna=str(dato))
        if retornoFila:
            return fila
        return True
    
    def verifica_existencia(self, dato: str, columna: str="rut", retornafila=False) -> bool:
        verificacion = super().buscadato(
            self.hoja_actual["filainicial"],
            self.hoja_actual["columnas"][columna],
            dato,
            filtropuntuacion=True
            )
        if verificacion:
            if retornafila:
                return verificacion
            return True
        return False
    
    def busca_datoscliente(self, nombre: str, filtro: str="cliente") -> list:
        ubicacion = super().buscadato(
            self.hoja_actual["filainicial"],
            self.hoja_actual["columnas"][filtro],
            nombre
            )
        if ubicacion == 0:
            return 0
        datos = super().extraefila(
            fila=ubicacion,
            columnas=[
                self.hoja_actual["columnas"]["rut"],
                self.hoja_actual["columnas"]["cliente"],
                self.hoja_actual["columnas"]["direccion"],
                self.hoja_actual["columnas"]["comuna"],
                self.hoja_actual["columnas"]["telefono"],
                self.hoja_actual["columnas"]["diascontrato"],
                self.hoja_actual["columnas"]["otro"]
            ])
        return datos
    
    def estado_cliente(self, rut: str, estado: str) -> bool:
        ubicacion = super().busca_ubicacion(rut,"rut")
        try:
            super().ingresador(
                ubicacion,
                [estado],
                [self.hoja_actual["columnas"]["estado"]]
                )
        except:
            return False
        else:
            return True
            
    def proximo_retiro(self, rut: str, fecharetiro: str) -> str:
        diascontrato = super().getDato(
            fila=super().busca_ubicacion(
                dato=rut,
                columna="rut"
                ),
            columna="diascontrato"
            )
        
        if not diascontrato:
            return None
        
        try:
            int(diascontrato)
        except Exception as e:
            print(e)
            return None
        else:
            lapso = timedelta(diascontrato + 2)
        
        fecharetiro = date.fromisoformat(fecharetiro)
        proxretiro = date.isoformat(fecharetiro + lapso)
        return proxretiro
        
    def guardar_modificacion(self, rut: str, data: list) -> bool:
        fila = super().busca_ubicacion(rut,"rut")
        try:
            super().ingresador(fila,data,2)
        except:
            return False
        else:
            return True
