from bd.repository import bdmediclean
from coder.codexpy2 import codexpy2
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

   def busca_cliente(self, nombre: str) -> map:
      filainicio = self.hojaActual["filainicial"]
      columna = self.hojaActual["columnas"]["cliente"]
      filas = self.bd.buscapartedato(filainicio,columna,nombre)
      columnas = self.hojaActual["columnas"]["todas"]
      resultados = {}
      resultados["encabezados"] = self.bd.extraefila(1,columnas)
      resultados["datos"] = []
      for fila in filas:
         data = self.bd.extraefila(fila,columnas)
         resultados["datos"].append(data)
      
      return resultados

if __name__ == '__main__':
     def limpiapantalla(): 
          os.system("clear")
     def pantallamenu():
          print("\n\n*******************\nAdministrador de usuarios\n\n")
          print("** COMANDOS **")
          print("adduser - 'Agrega un usuario nuevo'")
          print("deluser - 'elimina un usuario'")
          print("listuser - 'lista los usuarios existentes'")
          print("----------------------------")
     
     def guarda(bd: object):
          try:
               bd.guardar()
          except:
               print("Error en guardado del libro\n\n")
          else:
               print("Cambios guardados\n\n")
     
     def lista_usuarios() -> None:
          list_users = bd.listar(filainicial,[usuarios],encabezados)
          limpiapantalla()
          print("******** LISTA DE USUARIOS REGISTRADOS ********")
          for usuario in list_users["datos"]:
               print(f">>> {usuario}")
          print("____________________\n\n\n")
     
     bd = bdmediclean(params.USUARIO["nombrehoja"])
     coder = codexpy2()
     
     filainicial = params.USUARIO["filainicial"]
     usuarios = params.USUARIO["columnas"]["usuario"]
     encabezados = params.USUARIO["encabezados"]
     
     limpiapantalla()
     
     while(True):
          
          pantallamenu()
          
          comando = input("COMANDO >> ")
          
          if comando == "adduser":
               usuario = input("Ingresa un nombre de usuario >> ")
               contrasena = input("Ingresa una contrasena >> ")
               if (usuario != "" or usuario != None or
               contrasena != "" or contrasena != None):
                    password = coder.encripta(contrasena)
                    bloquevacio = bd.buscafila(filainicial)
                    bd.ingresador(bloquevacio,[usuario,password,],1)
                    guarda(bd)
                    limpiapantalla()
                    pantallamenu()
               else:
                    print("DEBES INDICAR UN NOMBRE DE USUARIO Y UNA CONTRASENA")
          
          elif comando == "deluser":
               limpiapantalla()
               lista_usuarios()
               usuario = input("Usuario a eliminar >>> ")
               if (usuario != "" or usuario != None):
                    ubicacion = bd.buscadato(filainicial,usuarios,usuario)
                    bd.eliminar(ubicacion)
                    guarda(bd)
               else:
                    print("DEBES INDICAR UN NOMBRE DE USUARIO")
                    
          elif comando == "listuser":
               lista_usuarios()
          
          elif comando == "quit":
               print("\n\nBye!!\n\n")
               break
          
          else:
               print(">> COMANDO ERRONEO <<")
          
     bd.cerrar()
     
     
     
     
     
     