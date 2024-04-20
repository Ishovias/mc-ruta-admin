from bd.repository import bdmediclean
import params
import os

class conectorbd:
  
   hojaClientes = params.CLIENTES
   hojaRutaActual = params.RUTA_ACTUAL
   hojaUsuarios = params.USUARIO
   hojaRutabd = params.RUTAS_BD
   hojaGastos = params.GASTOS_BD
   
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
   
   # ------------ Metodos de trabajo en base de datos ----------------
   def comprueba_usuario(self, nombre: str, contrasena: str) -> bool:
      dnombre = self.bd.buscadato(self.hojaUsuarios["filainicial"],1,nombre)
      dcontrasena = self.bd.buscadato(self.hojaUsuarios["filainicial"],2,contrasena)
      if dnombre > 0 and dcontrasena > 0:
         resultado = True
      else:
         resultado = False
      return resultado

   def busca_cliente(self, nombre: str) -> list:
      filainicio = self.hojaActual["filainicio"]
      columna = self.hojaActual["columnas"]["nombre"]
      filas = self.bd.buscapartedato(filainicio,columna,nombre)
      filas.insert(0,1)
      resultados = []
      columnas = self.hojaActual["columnas"]["todas"]
      for fila in filas:
         data = self.bd.extraefila(fila,columnas)
         resultados.append(data)
      
      return resultados
   
   if __name__ == '__main__':
      os.system("clear")
      sheetname = "autorizador"
      bd = bdmediclean(sheetname)
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