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
          resultado = self.operacion.ingresar_dato_simple(dato,datos,fila,columna,identificador)
          return resultado
     
     def getData(self, fila: int=None, columna: str=None, columnas: list=None, identificador: str=None) -> bool:
          resultado = self.operacion.getDato(fila,columna,columnas,identificador)
          return resultado

class RutaRegistros:
     
     current_sheet = ""

     def __init__(self) -> None:
          self.current_sheet = params.RUTAS_REGISTROS
     super()
          
     def listarData(self) -> map:
          return self.operacion.listarDatos()
          
     def ubicar(self, dato: str, columna: str="rut") -> int:
          return self.operacion.ubicacion(dato,columna)

     def ubicacionLibre(self, columna: str="fecha") -> int:
          return self.operacion.filaLibre(columna)

     def nuevaRuta(self, fecha: str, ruta: str) -> bool:
          ingreso = self.operacion.ingresar_dato_simple(
               datos=[fecha,ruta],
               fila=self.operacion.filaLibre(),
               columna="fecha"
               )
          if ingreso:
               return True
          else: 
               return False
     

class RutaBD:

     current_sheet = ""

     def __init__(self) -> None:
          self.current_sheet = params.RUTAS_BD
          self.operacion = Operaciones(self.current_sheet)
          
     def listarData(self) -> map:
          return self.operacion.listarDatos()
     
     def ubicar(self, dato: str, columna: str="rut") -> int:
          return self.operacion.ubicacion(dato,columna)

     def ubicacionLibre(self, columna: str="fecha") -> int:
          return self.operacion.filaLibre(columna)

     def registraMovimiento(self, datos: list) -> bool:
          try:
               self.operacion.ingresador(
                    self.operacion.filaLibre(),
                    datos,
                    self.current_sheet["fecha"]
               )
          except:
               return False
          else:
               return True
          
     def ingresoData(self, dato: str, ubicacion: str) -> bool:
          resultado = self.operacion.ingresar_dato_simple(
               dato=dato,
               ubicacion=ubicacion
          )
          return resultado

     def getData(self, fila: int=None, columna: str=None, columnas: list=None, identificador: str=None) -> bool:
          resultado = self.operacion.getDato(fila,columna,columnas,identificador)
          return resultado

     def guardaDatos(self) -> bool:
          return self.operacion.guardarCambios()
               
     def cerrarConexion(self) -> None:
          return self.operacion.cierraConexion()

     def guardarCerrar(self) -> bool:
          return self.operacion.guardaCierra()

     def eliminaData(self, fila: int) -> bool:
          return self.operacion.eliminaDatos(fila)
