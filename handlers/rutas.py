from bd.repository import bdmediclean
import params

class RutaActual(bdmediclean):

     def __init__(self) -> None:
          super().__init__(params.RUTA_ACTUAL)
     
     def nuevaRuta(self, fecha: str, ruta: str) -> bool:
          if super().getDato(identificador="rutaencurso") != None:
               return False
          try:
               super().ingresador(
               fila=super().hoja_actual["rutaencurso"]["fila"],
               datos=[fecha,ruta],
               columnainicio=super().hoja_actual["rutaencurso"]["columna"]
               )
          except:
               return False
          else: 
               return True
     
     def ingresoData(self, dato: str=None, datos: list=None, fila: int=None, columna: str=None, identificador: str=None) -> bool:
          return super().ingresar_dato_simple(dato,datos,fila,columna,identificador)
          
     def getData(self, fila: int=None, columna: str=None, columnas: list=None, identificador: str=None) -> bool:
          return super().getDato(fila,columna,columnas,identificador)

class RutaRegistros(bdmediclean):

     def __init__(self) -> None:
          super().__init__(params.RUTAS_REGISTROS)

     def nuevaRuta(self, fecha: str, ruta: str) -> bool:
          ingreso = super().ingresar_dato_simple(
               datos=[fecha,ruta],
               fila=super().filaLibre(),
               columna="fecha"
               )
          if ingreso:
               return True
          else: 
               return False
     

class RutaBD(bdmediclean):

     def __init__(self) -> None:
          super().__init__(params.RUTAS_BD)

     def registraMovimiento(self, datos: list) -> bool:
          try:
               super().ingresador(
                    super().filaLibre(),
                    datos,
                    super().hoja_actual["fecha"]
               )
          except:
               return False
          else:
               return True
