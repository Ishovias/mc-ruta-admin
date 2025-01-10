from bd.repository import bdmediclean
from datetime import date, timedelta, datetime
from cimprime import cimprime
import params

class Clientes(bdmediclean):

     def __init__(self) -> None:
          super().__init__(params.CLIENTES)
     
     def busca_cliente(self, busqueda: str, filtro: str, retornafilas: bool=False) -> map:
          # Devuelve un listado con encabezados y datos al estilo repository.listar
          filas = super().buscadato(
               dato=busqueda, 
               columna=filtro,
               filtropuntuacion=True, 
               buscartodo=True)
          if retornafilas:
               return filas
          resultados = super().listar(filas=filas) if filas else "Sin resultados"
          return resultados
     
     def nuevo_cliente(self, mapdatos: map) -> bool:
          existencia = super().buscadato(
               dato=mapdatos["id"],
               columna="id",
               exacto=True
               )
          if existencia:
               return False
          fila = super().buscafila(columna="id")
          for campo in mapdatos.keys():
               super().putDato(dato=mapdatos[campo], fila=fila, columna=campo)
          return True
     
     def verifica_existencia(self, dato: str, columna: str="id", retornafila=False) -> bool:
          verificacion = super().buscadato(
               dato=dato,
               columna=columna,
               filtropuntuacion=True
               )
          if verificacion:
               if retornafila:
                    return verificacion
               return True
          return False
     
     def estado_cliente(self, id_cliente: str, estado: str=None) -> bool:
          ubicacion = super().buscadato(
               dato=id_cliente,
               columna="id",
               exacto=True
               )
          if estado:
               super().putDato(
                    dato=estado,
                    fila=ubicacion,
                    columna="estado"
                    )
          else:
               return super().getDato(
                    fila=ubicacion,
                    columna="estado"
                    )
          
     def proximo_retiro(self, id_cliente: str, fecharetiro: str) -> str:
          diascontrato = super().getDato(
               fila=super().buscadato(
                    dato=rut,
                    columna="id"
                    ),
               columna="diascontrato"
               )
          
          if not diascontrato:
               return None
          
          lapso = timedelta(int(diascontrato) + 2)
          
          fecharetiro = datetime.strptime(fecharetiro, params.FORMATO_FECHA)
          fecharetiro += lapso
          proxretiro = datetime.strftime(fecharetiro, params.FORMATO_FECHA)
          
          return proxretiro
