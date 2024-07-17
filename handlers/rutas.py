from bd.repository import bdmediclean
import params

class Operaciones(bdmediclean):
     
     current_sheet = ""

     def __init__(self, hoja: object) -> None:
          self.current_sheet = hoja
          super().__init__(self.current_sheet["nombrehoja"])
     
     def ingresar_dato_simple(self, dato: str=None, datos: list=None, fila: int=None, columna: str=None, identificador: str=None) -> bool:
          if identificador:
               row = self.current_sheet[identificador]["fila"]
               column = self.current_sheet[identificador]["columna"]
          else:
               row = fila
               column = self.current_sheet["columnas"][columna]
          try:
               if datos:
                    super().ingresador(row,datos,column)
               else:
                    super().ingresador(row,[dato],column)
          except:
               return False
          else:
               return True
               
     def ubicacion(self, dato: str, columna: str="rut") -> int:
          return super().buscadatos(
               self.current_sheet["filainicio"],
               self.current_sheet["columnas"][columna],
               dato
          )
     
     def getDato(self, fila: int=None, columna: str=None, columnas: list=None, identificador: str=None) -> bool:
          if identificador:
               row = self.current_sheet[identificador]["fila"]
               column = self.current_sheet[identificador]["columna"]
          else:
               row = fila
               column = self.current_sheet["columnas"][columna]
          
          if columnas:    
               datos = super().extraefila(row,columnas)
               return datos
          else:
               datos = super().extraefila(row,[column])
               return datos[0]
               
          
     def listarDatos(self) -> list:
          listado = super().listar(
               self.current_sheet["filainicial"],
               self.current_sheet["columnas"]["todas"],
               self.current_sheet["encabezados"]
               )
          return listado

     def eliminaDatos(self, fila: int) -> bool:
          try:
               super().eliminar(fila)
          except:
               return False
          else:
               return True
          
     def filaLibre(self, columna: str="fecha") -> int:
          return super().buscafila(
               self.current_sheet["filainicial"],
               self.current_sheet["columnas"][columna]
               )

     def guardarCambios(self) -> bool:
          try:
               super().guardar()
          except:
               return False
          else:
               return True
               
     def cierraConexion(self) -> None:
          super().cerrar()

     def guardaCierra(self) -> bool:
          guardado = self.guardarCambios()
          self.cierraConexion()
          return guardado


class RutaActual:
     
     current_sheet = ""

     def __init__(self) -> None:
          self.current_sheet = params.RUTA_ACTUAL
          self.operacion = Operaciones(self.current_sheet)
     
     def listarData(self) -> map:
          return self.operacion.listarDatos()
          
     def ubicacionLibre(self, columna: str="fecha") -> int:
          return self.operacion.filaLibre(columna)

     def ubicar(self, dato: str, columna: str="rut") -> int:
          return self.operacion.ubicacion(dato,columna)

     def nuevaRuta(self, fecha: str, ruta: str) -> bool:
          if self.operacion.getDato(identificador="rutaencurso") != None:
               return False
          try:
               self.operacion.ingresador(
               fila=self.current_sheet["rutaencurso"]["fila"],
               datos=[fecha,ruta],
               columnainicio=self.current_sheet["rutaencurso"]["columna"]
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

     def guardaDatos(self) -> bool:
          return self.operacion.guardarCambios()
               
     def cerrarConexion(self) -> None:
          return self.operacion.cierraConexion()

     def guardarCerrar(self) -> bool:
          return self.operacion.guardaCierra()
     
     def eliminaData(self, fila: int) -> bool:
          return self.operacion.eliminaDatos(fila)

class RutaRegistros:
     
     current_sheet = ""

     def __init__(self) -> None:
          self.current_sheet = params.RUTAS_REGISTROS
          self.operacion = Operaciones(self.current_sheet)
          
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
     
     def ingresoData(self, dato: str=None, datos: list=None, fila: int=None, columna: str=None, identificador: str=None) -> bool:
          resultado = self.operacion.ingresar_dato_simple(dato,datos,fila,columna,identificador)
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
