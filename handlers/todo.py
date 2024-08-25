from bd.repository import bdmediclean
from datetime import date
import params

class Todo(bdmediclean):

     def __init__(self) -> None:
          super().__init__(params.TODO, otrolibro=params.LIBROTODO)

     def nuevatarea(self, tarea: str) -> str:
          if super().busca_ubicacion(dato=tarea, columna="descripcion"):
               return False
          filalibre = super().buscafila()
          datos = [
               date.today(),
               tarea,
               "PENDIENTE"
               ]
          return super().putDato(datos=datos, fila=filalibre, columna="fecha")
     
     def accion(self, identificador: str, accion: str) -> None:
          fila = super().busca_ubicacion(dato=identificador, columna="descripcion")
          super().putDato(dato=accion, fila=fila, columna="completado")
          if accion == "COMPLETADO":
               super().putDato(dato=date.today(), fila=fila, columna="fechacompletado")
          
     def eliminatarea(self, tarea: str) -> None:
          fila = super().busca_ubicacion(dato=tarea, columna="descripcion")
          super().eliminar(fila)