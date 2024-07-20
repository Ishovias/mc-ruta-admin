from bd.repository import bdmediclean
import params

class Clientes(bdmediclean):

    def __init__(self) -> None:
        super().__init__(params.CLIENTES)

    def busca_cliente_lista(self, nombre: str) -> map:
        filainicio = super().hoja_actual["filainicial"]
        columna = super().hoja_actual["columnas"]["cliente"]
        filas = super().buscapartedato(filainicio,columna,nombre)
        columnas = super().hoja_actual["columnas"]["todas"]
        resultados = {}
        resultados["encabezados"] = super().extraefila(1,columnas)
        resultados["datos"] = []
        for fila in filas:
            data = super().extraefila(fila,columnas)
            resultados["datos"].append(data)
        return resultados

    def nuevo_cliente(self, data: list) -> bool:
        existencia = super().busca_datoscliente(data[1])
        if existencia != 0:
            return False
        fila = super().buscafila(
            super().hoja_actual["filainicial"],
            super().hoja_actual["columnas"]["rut"],
            )
        super().ingresador(fila,data,1)
        return True
    
    def busca_datoscliente(self, nombre: str, filtro: str="cliente") -> list:
        ubicacion = super().buscadato(
            super().hoja_actual["filainicial"],
            super().hoja_actual["columnas"][filtro],
            nombre
            )
        if ubicacion == 0:
            return 0
        datos = super().extraefila(
            ubicacion,
            super().hoja_actual["columnas"]["todas"]
            )
        return datos
    
    def estado_cliente(self, rut: str, estado: str) -> bool:
        ubicacion = super().busca_ubicacion(rut,"rut")
        try:
            super().ingresador(
                ubicacion,
                [estado],
                [super().hoja_actual["columnas"]["estado"]]
                )
        except:
            return False
        else:
            return True
        
    def guardar_modificacion(self, rut: str, data: list) -> bool:
        fila = super().busca_ubicacion(rut,"rut")
        try:
            super().ingresador(fila,data,2)
        except:
            return False
        else:
            return True

