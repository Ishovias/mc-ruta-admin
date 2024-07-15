from bd.repository import bdmediclean
import params

class Operaciones(bdmediclean):
     
     def __init__(self, hoja: str) -> None:
          self.hoja_actual = params.hojas_bd[hoja]
          super().__init__(self.hojas_actual["nombrehoja"])
     
     def ingresar_dato_simple(self, dato: str=None, datos: list=None, fila: int=None, columna: str=None, identificador: str=None) -> bool:
          if identificador:
               row = self.hoja_actual[identificador]["fila"]
               column = self.hoja_actual[identificador]["columna"]
          else:
               row = fila
               column = self.hoja_actual["columnas"][columna]
          try:
               if datos:
                    super().ingresador(row,datos,column)
               else:
                    super().ingresador(row,[dato],column)
          except:
               return False
          else:
               return True
               
     def getDato(self, fila: int=None, columna: str=None, columnas: list=None identificador: str=None) -> bool:
          if identificador:
               row = self.hoja_actual[identificador]["fila"]
               column = self.hoja_actual[identificador]["columna"]
          else:
               row = fila
               column = self.hoja_actual["columnas"][columna]
          
          if columnas:    
               datos = self.super().extraefila(row,columnas)
          else:
               datos = self.super().extraefila(row,[column])
               
          return datos
          
     def listarDatos(self) -> list:
          listado = self.super().listar(
               self.hoja_actual["filainicial"],
               self.hoja_actual["columnas"]["todas"],
               self.hoja_actual["encabezados"]
               )
          return listado

class RutaActual(bdmediclean):
     
     hoja_actual = ""

     def __init__(self) -> None:
          self.hoja_actual = params.RUTA_ACTUAL
          self.operacion = Operaciones("hojaRutaActual")
          super().__init__(self.hojas_actual["nombrehoja"])
     
     def listar(self) -> map:
          return self.super().listardatos()
          
     def nuevaRuta(self, fecha: str, ruta: str) -> bool:
          if self.super().getDato(identificador="rutaencurso") == [None]:
               return False
          ingresofecha = self.operacion.ingresar_dato_simple(dato=fecha, identificador="rutaencurso")
          ingresoruta = self.operacion.ingresar_dato_simple(dato=ruta, identificador="nombreruta")
          if ingresofecha and ingresoruta:
               return True
          else: 
               return False
               
     def getData(self, fila: int=None, columna: str=None, columnas: list=None identificador: str=None) -> bool:
          self.super().getDato(fila,columna,columnas,identificador)
          
     def guardarCambios(self) -> bool:
          try:
               self.super().guardar()
          except:
               return False
          else:
               return True
               
     def cierraConexion(self) -> None:
          self.super().cerrar()
     
     def guardaCierra(self) -> bool:
          guardado = self.guardarCambios()
          self.cierraConexion()
          return guardado
     
class RutaRegistros(bdmediclean):
     
     hoja_actual = ""

     def __init__(self) -> None:
          self.hoja_actual = params.RUTA_REGISTROS
          self.operacion = Operaciones("hojaRutaRegistros")
          super().__init__(self.hojas_actual["nombrehoja"])
          
     def listar(self) -> map:
          return self.super().listardatos()
          
     def nuevaRuta(self, fecha: str, ruta: str) -> bool:
          ingreso = self.operacion.ingresar_dato_simple(
               datos=[fecha,ruta],
               fila=self.busca_fila(
                    self.hoja_actual["filainicial"],
                    self.hoja_actual["columnas"]["fecha"]
                    )
               )
          if ingreso:
               return True
          else: 
               return False
     
     def getData(self, fila: int=None, columna: str=None, columnas: list=None identificador: str=None) -> bool:
          self.super().getDato(fila,columna,columnas,identificador)
     
     def guardarCambios(self) -> bool:
          try:
               self.super().guardar()
          except:
               return False
          else:
               return True
               
     def cierraConexion(self) -> None:
          self.super().cerrar()
     
     def guardaCierra(self) -> bool:
          guardado = self.guardarCambios()
          self.cierraConexion()
          return guardado