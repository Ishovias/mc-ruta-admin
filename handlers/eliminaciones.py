from bd.repository import bdmediclean
from params import RETIROS_ELIMINADOS, REGISTRO_ELIMINACIONES

class RetirosEliminados(bdmediclean):

     def __init__(self):
          super().__init__(hoja=RETIROS_ELIMINADOS)


class EliminacionRegistros(bdmediclean):
     
     def __init__(self):
          super().__init__(hoja=REGISTRO_ELIMINACIONES)
     
     def registra_eliminacion(self, datos: map) -> bool:
          ubicacion = super().busca_ubicacion(columna="fecha")
          for columna, dato in datos.items():
               super().putDato(
                    dato=dato,
                    fila=ubicacion,
                    columna=columna
               )
          else:
               return True
          return False
          
     def obtener_fechas_eliminadas(self, paquetedatos: list) -> str:
          todasfechas = []
          for fila in paquetedatos:
               todasfechas.append(fila[0])
          fechas = [todasfechas[0]]
          for f in todasfechas:
               if f not in fechas:
                    fechas.append(f)
          texto = "Rutas eliminadas: "
          for x in fechas:
               texto += str(x)
          return texto
     