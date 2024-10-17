from bd.repository import bdmediclean
from helpers import cimprime
import params

class RutaActual(bdmediclean):

     def __init__(self) -> None:
          super().__init__(params.RUTA_ACTUAL, otrolibro=params.LIBRORUTA)
     
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
          verificar = super().busca_ubicacion(datos[0],"rut")
          if verificar:
               return False
          ubicacion = super().busca_ubicacion(columna="cliente")
          idActual = super().idActual("id")
          
          datos.insert(0,idActual)
          datos.insert(0,fecha)

          try:
               super().ingresador(
                    ubicacion,
                    datos,
                    self.hoja_actual["columnas"]["fecha"]
                    )
          except Exception as e:
               print (e)
               return False
          else:
               return True
     
     def importar(self, datos: map) -> bool:
          super().putDato(dato=datos["rutaencurso"],identificador="rutaencurso")
          super().putDato(dato=datos["nombreruta"],identificador="nombreruta")
          super().eliminarContenidos()
          filaubicacion = self.hoja_actual["filainicial"]
          for fila in datos["datos"]:
               super().putDato(datos=fila,fila=filaubicacion,columna="fecha")
               filaubicacion += 1
          else:
               return True
          return False

class RutaRegistros(bdmediclean):
     
     def __init__(self) -> None:
          super().__init__(params.RUTAS_REGISTROS)

     def nuevaRuta(self, fecha: str, ruta: str) -> bool:
          if super().buscadato(
               filainicio=self.hoja_actual["filainicial"],
               columna=self.hoja_actual["columnas"]["fecha"],
               dato=fecha
          ):
               return False
          ingreso = super().putDato(
               datos=[fecha,ruta],
               fila=super().buscafila(),
               columna="fecha"
               )
          if ingreso:
               return True
          else: 
               return False
     
     def registra_importacion(self, datos: map) -> bool:
          finalizada = True
          existente = super().busca_ubicacion(dato=datos["rutaencurso"],columna="fecha")
          if existente:
               finalizada = super().getDato(fila=existente,columna="otros")
          if not existente or not finalizada:
               fila = super().busca_ubicacion(columna="fecha")
               cimprime(titulo="intentando registrar", datos=[datos["rutaencurso"],datos["nombreruta"]],fila=fila)
               super().putDato(datos=[datos["rutaencurso"],datos["nombreruta"]],fila=fila,columna="fecha")
               return True
          return False

class RutaBD(bdmediclean):
     
     kilosItems = {
          "farmaco":0,
          "patologico":0,
          "contaminado":0,
          "cortopunzante":0,
          "otropeligroso":0,
          "liquidorx":0
          }
     
     def __init__(self) -> None:
          super().__init__(params.RUTAS_BD)

     def registraMovimiento(self, datos: list) -> bool:
          try:
               super().ingresador(
                    super().buscafila(),
                    datos,
                    self.hoja_actual["columnas"]["fecha"]
               )
          except Exception as e:
               print(e)
               return False
          else:
               return True
               
     def kgtotales(self, fechainicio: str=None, fechafinal: str=None, filaCliente: int=None) -> str:
          items = {
                    "farmaco":0,
                    "patologico":0,
                    "contaminado":0,
                    "cortopunzante":0,
                    "otropeligroso":0,
                    "liquidorx":0
               }
          if fechainicio and fechafinal:
               filainicio = super().busca_ubicacion(dato=str(fechainicio),columna="fecha")
               filafinal = super().busca_ubicacion(dato=str(fechafinal),columna="fecha")
               for i in range(filafinal, super().getmaxfilas(),1):
                    dato = super().getDato(fila=i,columna="fecha")
                    if str(dato) != str(fechafinal):
                         filafinal = i
                         break
               for item in items:
                    for f in range(filainicio,filafinal,1):
                         dato = super().getDato(fila=f,columna=item)
                         if dato:
                              items[item] += int(dato)
                              self.kilosItems[item] += int(dato)
               return items
          
          if filaCliente:
               for item in items:
                    dato = super().getDato(fila=filaCliente,columna=item)
                    if dato:
                         items[item] += int(dato)
                         self.kilosItems[item] += int(dato)
               return items
          
          return None

     def getKilos(self) -> map:
          return self.kilosItems

     def eliminaKilosRegistrados(self) -> None:
          for item in self.kilosItems:
               self.kilosItems[item] = 0

class RutaImportar(bdmediclean):
     def __init__(self, archivo: str) -> None:
          super().__init__(params.RUTA_ACTUAL, otrolibro=str(archivo))
          self.hoja_actual = params.RUTA_ACTUAL

     def extrae_ruta(self) -> map:
          return {
               "rutaencurso": super().getDato(identificador="rutaencurso", retornostr=True),
               "nombreruta": super().getDato(identificador="nombreruta", retornostr=True),
               "datos":super().listar(retornostr=True, solodatos_list=True)
          }