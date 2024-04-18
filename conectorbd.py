from bd.repository import bdmediclean
import params
import os

class conectorbd:
  
  hojaDatos = params.CLIENTES
  hojaActividad = params.RUTA_ACTUAL
  hojaAsistencia = params.USUARIO
  
  hojaActual = None
  
  def __init__ (self,hoja: str) -> None:
    self.hojaActual = hoja
    self.bd = bdmediclean(hoja["nombrehoja"])
    
  def set_hoja(self, hoja: str) -> None:
    self.bd.hojaActual = hoja
    self.bd = bdmediclean(hoja["nombrehoja"])
  
  def getHojaActual(self) -> str:
    return self.bd.hojaActual
  
  def guarda_cambios(self) -> str:
    try:
      self.bd.guardar()
    except:
      resultado = "ERROR al intentar guardar, verifica que no este abierto el libro excel"
    else:
      resultado = "Datos guardados exitosamente"
      
    return resultado
  
  def cierra_conexion(self) -> None:
    self.bd.cerrar()
    
  
  if __name__ == '__main__':
    os.system("clear")
    sheetname = "autorizador"
    bd = pysecretario(sheetname)
    filadisponible = bd.buscafila(1)
    fila = filadisponible
    datos = ["iberoiza","1234"]
    columnainicio = 1
    bd.ingresador(fila,datos,columnainicio)
    
    try:
      bd.guardar()
    except:
      print("Error en guardado del libro\n\n")
    else:
      print("Cambios guardados\n\n")
    finally:
      bd.cerrar()