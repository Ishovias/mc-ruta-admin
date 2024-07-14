from bd.repository import bdmediclean
import params

class Operaciones(bdmediclean):
     
     def __init__(self, hoja: str) -> None:
          self.hoja_actual = params.hojas_bd[hoja]
          super().__init__(self.hojas_actual["nombrehoja"])
     
     def ingresar_dato_simple(self, dato: str, fila: int=None, columna: str=None, identificador: str=None) -> bool:
          if identificador:
               row = self.hoja_actual[identificador]["fila"]
               column = self.hoja_actual[identificador]["columna"]
          else:
               row = fila
               column = self.hoja_actual["columnas"][columna]
          try:
               super().ingresador(row,[dato],column)
          except:
               return False
          else:
               return True

class RutaActual(bdmediclean):
     
     hoja_actual = ""

     def __init__(self) -> None:
          self.hoja_actual = params.RUTA_ACTUAL
          self.operacion = Operaciones("hojaRutaActual")
          super().__init__(self.hojas_actual["nombrehoja"])
          
     def nuevaRuta(self, fecha: str, ruta: str) -> bool:
          ingresofecha = self.operacion.ingresar_dato_simple(fecha, identificador="rutaencurso")
          ingresoruta = self.operacion.ingresar_dato_simple(ruta, identificador="nombreruta")
          if ingresofecha and ingresoruta:
               return True
          else: 
               return False
               

class RutaRegistros(bdmediclean):
     
     hoja_actual = ""

     def __init__(self) -> None:
          self.hoja_actual = params.RUTA_REGISTROS
          self.operacion = Operaciones("hojaRutaRegistros")
          super().__init__(self.hojas_actual["nombrehoja"])
          
     def nuevaRuta(self, fecha: str, ruta: str) -> bool:
          ingresofecha = self.operacion.ingresar_dato_simple(
               fecha,
               fila=self.busca_fila(
                    self.hoja_actual["filainicial"],
                    self.hoja_actual["columnas"]["fecha"]
                    )
               )
          ingresoruta = self.operacion.ingresar_dato_simple(ruta, identificador="nombreruta")
          if ingresofecha and ingresoruta:
               return True
          else: 
               return False
     
     
     