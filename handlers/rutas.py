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
               fila=self.hoja_actual["rutaencurso"]["fila"],
               datos=[fecha,ruta],
               columnainicio=self.hoja_actual["rutaencurso"]["columna"]
               )
          except:
               return False
          else: 
               return True
     
     def getFechaRuta(self) -> str:
          return super().getDato(identificador="rutaencurso")

     def agregar_a_ruta(self, fecha: str, datos: list) -> bool:
          verificar = super().busca_datoscliente(datos[0],"rut")
          if verificar != 0:
               return False
          ubicacion = super().busca_ubicacion(None, "cliente")
          idActual = super().idActual(
               self.hoja_actual["filainicial"],
               self.hoja_actual["columnas"]["id"],
               "ID"
               )
          
          datos.insert(0,idActual)
          datos.insert(0,fecha)
          
          try:
               self.bd.ingresador(
                    ubicacion,
                    datos,
                    self.hoja_actual["columnas"]["fecha"]
                    )
          except:
               return False
          else:
               return True

class RutaRegistros(bdmediclean):

     def __init__(self) -> None:
          super().__init__(params.RUTAS_REGISTROS)

     def nuevaRuta(self, fecha: str, ruta: str) -> bool:
          ingreso = super().putDato(
               datos=[fecha,ruta],
               fila=super().buscafila(),
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
                    self.hoja_actual["fecha"]
               )
          except:
               return False
          else:
               return True
