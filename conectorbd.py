from bd.repository import bdmediclean
from coder.codexpy2 import codexpy2
import params
import os

class conectorbd:

     hojaClientes = params.CLIENTES
     hojaRutaActual = params.RUTA_ACTUAL
     hojaUsuarios = params.USUARIO
     hojaRutabd = params.RUTAS_BD
     hojaRutasRegistros = params.RUTAS_REGISTROS
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
               return False
          else:
               return True

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

     def busca_cliente_lista(self, nombre: str) -> map:
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

     def busca_datoscliente(self, nombre: str, filtro: str="cliente") -> list:
          ubicacion = self.bd.buscadato(
               self.hojaActual["filainicial"],
               self.hojaActual["columnas"][filtro],
               nombre
               )
          if ubicacion == 0:
               return 0
          datos = self.bd.extraefila(
               ubicacion,
               self.hojaActual["columnas"]["todas"]
               )
          return datos
          
     def nuevo_cliente(self, data: list) -> bool:
          existencia = self.busca_datoscliente(data[1])
          if existencia != 0:
               return False
          fila = self.bd.buscafila(
               self.hojaClientes["filainicial"],
               self.hojaClientes["columnas"]["rut"],
               )
          self.bd.ingresador(fila,data,1)
          return True
          
     def busca_ubicacion(self, dato: str, columna: str="cliente") -> int:
          column = self.hojaActual["columnas"][columna]
          filainicial = self.hojaActual["filainicial"]
          if dato == None:
               fila = self.bd.buscafila(filainicial,column)
          else:
               fila = self.bd.buscadato(filainicial,column,dato)
          return fila
          
     def guardar_modificacion(self, rut: str, data: list) -> bool:
          fila = self.busca_ubicacion(rut,"rut")
          try:
               self.bd.ingresador(fila,data,1)
          except:
               return False
          else:
               return True

     def elimina_cliente(self, rut: str) -> bool:
          ubicacion = self.busca_ubicacion(rut,"rut")
          try:
               self.bd.eliminar(ubicacion)
          except:
               return False
          else:
               return True
          

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

     def listar_datos(self) -> map:
          return self.bd.listar(
               self.hojaActual["filainicial"],
               self.hojaActual["columnas"]["todas"],
               self.hojaActual["encabezados"]
          )
          

     def busca_cliente_lista(self, nombre: str) -> map:
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

     def busca_datoscliente(self, nombre: str, filtro: str="cliente") -> list:
          ubicacion = self.bd.buscadato(
               self.hojaActual["filainicial"],
               self.hojaActual["columnas"][filtro],
               nombre
               )
          if ubicacion == 0:
               return 0
          datos = self.bd.extraefila(
               ubicacion,
               self.hojaActual["columnas"]["todas"]
               )
          return datos
          
     def nuevo_cliente(self, data: list) -> bool:
          existencia = self.busca_datoscliente(data[1])
          if existencia != 0:
               return False
          fila = self.bd.buscafila(
               self.hojaClientes["filainicial"],
               self.hojaClientes["columnas"]["rut"],
               )
          self.bd.ingresador(fila,data,1)
          return True
          
     def busca_ubicacion(self, dato: str, columna: str="cliente", filainicio: str="filainicial") -> int:
          column = self.hojaActual["columnas"][columna]
          filainicial = self.hojaActual[filainicio]
          if dato == None:
               fila = self.bd.buscafila(filainicial,column)
               print(f"Buscando fila vacia\nEncontrada en {fila}\nColumna: {filainicial},{columna}")
          else:
               fila = self.bd.buscadato(filainicial,column,dato)
          return fila
          
     def guardar_modificacion(self, rut: str, data: list) -> bool:
          fila = self.busca_ubicacion(rut,"rut")
          try:
               self.bd.ingresador(fila,data,2)
          except:
               return False
          else:
               return True

     def elimina_cliente(self, rut: str) -> bool:
          ubicacion = self.busca_ubicacion(rut,"rut")
          try:
               self.bd.eliminar(ubicacion)
          except:
               return False
          else:
               return True
          
     def estado_cliente(self, rut: str, estado: str) -> bool:
          ubicacion = self.busca_ubicacion(rut,"rut")
          try:
               self.bd.ingresador(
                    ubicacion,
                    [estado],
                    [self.hojaActual["columnas"]["estado"]]
                    )
          except:
               return False
          else:
               return True
               
     def nueva_ruta(self, fecha_nombre: list) -> None:
          if self.busca_ubicacion(fecha_nombre[0], "fecha") != 0:
               print(f"ERROR, fecha preexistente")
               return False
          ubicacion = self.busca_ubicacion(None, "fecha")
          try:
               self.bd.ingresador(
                    ubicacion,
                    fecha_nombre,
                    self.hojaActual["columnas"]["fecha"]
                    )
          except:
               print(f"ERROR\nFila ingresando = {ubicacion} \nFecha: {fecha_nombre[0]} \nNombre: {fecha_nombre[1]}")
               return False
          else:
               return True
          
     def agregar_a_ruta(self, fecha: str, datos: list) -> bool:
          verificar = self.busca_datoscliente(datos[0],"rut")
          if verificar != 0:
               return False
          ubicacion = self.busca_ubicacion(None, "cliente")
          idActual = self.bd.idActual(
               self.hojaActual["filainicial"],
               self.hojaActual["columnas"]["id"],
               id
               )
          
          datos.insert(0,idActual)
          datos.insert(0,fecha)
          
          try:
               self.bd.ingresador(
                    ubicacion,
                    datos,
                    self.hojaActual["columnas"]["fecha"]
                    )
          except:
               return False
          else:
               return True

     def fecha_ruta(self) -> str:
          dato = self.bd.extraefila(
               self.hojaActual["rutaencurso"]["fila"],
               [self.hojaActual["rutaencurso"]["columna"]]
               )
          if dato[0] == None:
               return None
          else:
               return dato[0]
             
if __name__ == '__main__':
     def limpiapantalla(): 
          os.system("clear")
     def pantallamenu():
          print("\n\n*******************\nAdministrador de usuarios\n\n")
          print("** COMANDOS **")
          print("adduser - 'Agrega un usuario nuevo'")
          print("deluser - 'elimina un usuario'")
          print("listuser - 'lista los usuarios existentes'")
          print("mod - modificacion personalizada a bd en el codigo")
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
          
          elif comando == "mod":
               bda = bdmediclean(params.CLIENTES["nombrehoja"])
               encabezados = 1
               columnainicio = 1
               bda.ingresador(
                    encabezados,
                    ["ESTADO",
                    "RUT",
                    "CLIENTE",
                    "DIRECCION",
                    "COMUNA",
                    "TELEFONO",
                    "GPS",
                    "OTRO"],
                    columnainicio
                    )
               limpiapantalla()
               guarda(bda)
               bda.cerrar()

          elif comando == "quit":
               print("\n\nBye!!\n\n")
               break
          
          else:
               print(">> COMANDO ERRONEO <<")
          
     bd.cerrar()
     
     
     
     
     
     