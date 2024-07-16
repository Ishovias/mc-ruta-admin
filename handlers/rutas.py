from bd.repository import bdmediclean
import params

class Operaciones(bdmediclean):
     
     hoja_actual = ""

     hojas_bd = {
          "hojaClientes":params.CLIENTES,
          "hojaUsuarios":params.USUARIO,
          "hojaRutaActual":params.RUTA_ACTUAL,
          "hojaRutasBD":params.RUTAS_BD,
          "hojaRutasRegistros":params.RUTAS_REGISTROS,
          "hojaGastosBD":params.GASTOS_BD
     }

     def __init__(self, hoja: str) -> None:
          self.hoja_actual = self.hojas_bd[hoja]
          super().__init__(self.hoja_actual["nombrehoja"])
     
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
               
     def ubicacion(self, dato: str, columna: str="rut") -> int:
          return super().buscadatos(
               self.hoja_actual["filainicio"],
               self.hoja_actual["columnas"][columna],
               dato
          )
     
     def getDato(self, fila: int=None, columna: str=None, columnas: list=None, identificador: str=None) -> bool:
          if identificador:
               row = self.hoja_actual[identificador]["fila"]
               column = self.hoja_actual[identificador]["columna"]
          else:
               row = fila
               column = self.hoja_actual["columnas"][columna]
          
          if columnas:    
               datos = super().extraefila(row,columnas)
          else:
               datos = super().extraefila(row,[column])
               
          return datos
          
     def listarDatos(self) -> list:
          listado = super().listar(
               self.hoja_actual["filainicial"],
               self.hoja_actual["columnas"]["todas"],
               self.hoja_actual["encabezados"]
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
               self.hoja_actual["filainicial"],
               self.hoja_actual["columnas"][columna]
               )

class RutaActual(bdmediclean):
     
     hoja_actual = ""

     def __init__(self) -> None:
          self.hoja_actual = params.RUTA_ACTUAL
          self.operacion = Operaciones("hojaRutaActual")
          super().__init__(params.RUTA_ACTUAL["nombrehoja"])
     
     def listarData(self) -> map:
          return self.operacion.listarDatos()
          
     def ubicacionLibre(self, columna: str="fecha") -> int:
          return self.operacion.filaLibre(columna)

     def ubicar(self, dato: str, columna: str="rut") -> int:
          return self.operacion.ubicacion(dato,columna)

     def nuevaRuta(self, fecha: str, ruta: str) -> bool:
          if self.operacion.getDato(identificador="rutaencurso") == [None]:
               return False
          ingresofecha = self.operacion.ingresar_dato_simple(dato=fecha, identificador="rutaencurso")
          ingresoruta = self.operacion.ingresar_dato_simple(dato=ruta, identificador="nombreruta")
          if ingresofecha and ingresoruta:
               return True
          else: 
               return False
               
     def ingresoData(self, dato: str=None, datos: list=None, fila: int=None, columna: str=None, identificador: str=None) -> bool:
          resultado = self.operacion.ingresar_dato_simple(dato,datos,fila,columna,identificador)
          return resultado

     def getData(self, fila: int=None, columna: str=None, columnas: list=None, identificador: str=None) -> bool:
          resultado = self.operacion.getDato(fila,columna,columnas,identificador)
          return resultado

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
     
     def eliminaData(self, fila: int) -> bool:
          return self.operacion.eliminaDatos(fila)
     
class RutaRegistros(bdmediclean):
     
     hoja_actual = ""

     def __init__(self) -> None:
          self.hoja_actual = params.RUTA_REGISTROS
          self.operacion = Operaciones("hojaRutaRegistros")
          super().__init__(self.hoja_actual["nombrehoja"])
          
     def listarData(self) -> map:
          return self.operacion.listarDatos()
          
     def ubicar(self, dato: str, columna: str="rut") -> int:
          return self.operacion.ubicacion(dato,columna)

     def ubicacionLibre(self, columna: str="fecha") -> int:
          return self.operacion.filaLibre(columna)

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
     
     def ingresoData(self, dato: str=None, datos: list=None, fila: int=None, columna: str=None, identificador: str=None) -> bool:
          resultado = self.operacion.ingresar_dato_simple(dato,datos,fila,columna,identificador)
          return resultado

     def getData(self, fila: int=None, columna: str=None, columnas: list=None, identificador: str=None) -> bool:
          resultado = self.operacion.getDato(fila,columna,columnas,identificador)
          return resultado
     
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

     def eliminaData(self, fila: int) -> bool:
          return self.operacion.eliminaDatos(fila)

class RutaBD(bdmediclean):

     hoja_actual = ""

     def __init__(self) -> None:
          self.hoja_actual = params.RUTAS_BD
          self.operacion = Operaciones("hojaRutasBD")
          super().__init__(self.hoja_actual["nombrehoja"])
          
     def listarData(self) -> map:
          return self.operacion.listarDatos()
     
     def ubicar(self, dato: str, columna: str="rut") -> int:
          return self.operacion.ubicacion(dato,columna)

     def ubicacionLibre(self, columna: str="fecha") -> int:
          return self.operacion.filaLibre(columna)

     def registraMovimiento(self, datos: list) -> bool:
          try:
               super().ingresador(
                    super().buscafila(self.hoja_actual["filainicial"],1),
                    datos,
                    self.hoja_actual["fecha"]
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

     def eliminaData(self, fila: int) -> bool:
          return self.operacion.eliminaDatos(fila)
