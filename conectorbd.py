from bd.repository import pysecretario
import params
import os

class conectorbd:
  
  hojaDatos = params.HOJA_DATOS
  hojaActividad = params.HOJA_ACTIVIDAD
  hojaAsistencia = params.HOJA_ASISTENCIA
  hojaInformes = params.HOJA_INGRESO_INFORME
  hojaDatosNormados = params.HOJA_DATOS_NORMADOS
  hojaUsuarios = params.HOJA_AUTORIZADORA
  
  hojaActual = None
  
  def __init__ (self,hoja: str) -> None:
    self.hojaActual = hoja
    self.bd = pysecretario(hoja["nombrehoja"])
    
  def set_hoja(self, hoja: str) -> None:
    self.bd.setHoja = hoja
  
  def getHojaActual(self) -> str:
    return self.bd.hoja_actual
  
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
    
  def listarhermanos(self, columnas_seleccionadas: list, activos: str=None) -> list:
    nombres_hermanos = self.bd.listar(
        params.HOJA_DATOS["filainicial"],
        columnas_seleccionadas,
        params.HOJA_DATOS["encabezados"]
        )
    
    if activos == "activo":
        hermanos_activos = []
        for hermano in nombres_hermanos["datos"]:
            if hermano[1].lower() == "activo":
                hermanos_activos.append(hermano[0])
    else:
      hermanos_activos = []
      for hermano in nombres_hermanos["datos"]:
        hermanos_activos.append(hermano[0])
  
    hermanos_activos.sort()
    
    return hermanos_activos
  
  def ingresar_asistencia(self,data: list) -> str:
    self.bd.ingresador(
      self.bd.buscafila(params.HOJA_ASISTENCIA["filainicial"],2),
      data,2
      )
      
    resultado = self.guarda_cambios()
    
    return resultado
    
  def elimina_asistencia(self, anomes: str, dia: str) -> str:
    fila_anomes = self.bd.buscadato(
        params.HOJA_ASISTENCIA["filainicial"],
        params.HOJA_ASISTENCIA["columnas"]["anomes"],
        anomes)
    fila_dia = self.bd.buscadato(
        fila_anomes,
        params.HOJA_ASISTENCIA["columnas"]["dia"],
        dia)
  
    self.bd.eliminar(fila_dia)
  
    resultado = self.guarda_cambios()
    
    return resultado
        
  def registros_asistencia(self) -> map:
    data = self.bd.listar(
      params.HOJA_ASISTENCIA["filainicial"],
      params.HOJA_ASISTENCIA["columnas"]["todas"],
      params.HOJA_ASISTENCIA["encabezados"]
      )
    
    return data
  
  def informe_hermano(self, fechainicio: str, fechatermino: str, nombrehermano: str) -> map:
    listafechas = self.bd.rangofechas(fechainicio, fechatermino)
    informesrecoletados = self.bd.reportehermano(nombrehermano,listafechas)    
    data = informesrecoletados
    
    return data
    
  def lista_ingresos_informes(self) -> map:
    data = self.bd.listar(
      params.HOJA_INGRESO_INFORME["filainicial"],
      params.HOJA_INGRESO_INFORME["columnas"]["todas"],
      params.HOJA_INGRESO_INFORME["encabezados"]
      )
    
    return data
  
  def confirmar_informes(self, data: map) -> list:
    ok = False
    for informe in data["datos"]:
      fila = self.bd.buscafila(params.HOJA_ACTIVIDAD["filainicial"])
      self.bd.ingresador(fila,informe,1)
    else:
      ok = True
    if ok:
      self.guarda_cambios()
      resultado = [True,"Mes cerrado e informes almacenados"]
    else:
      resultado = [False,"Error en grabado de BD"]
    
    return resultado
  
  def limpiar_hoja_informes(self) -> str:
    fila_inicial = params.HOJA_INGRESO_INFORME["filainicial"]
    cantidad_filas = self.bd.contarfilas(fila_inicial)
    self.bd.eliminarContenidos(cantidad_filas, fila_inicial)
    self.guarda_cambios()
    
  def lista_nombres_informados(self) -> list:
    data = self.bd.listar(
      params.HOJA_INGRESO_INFORME["filainicial"],
      [params.HOJA_INGRESO_INFORME["columnas"]["nombre"]],
      params.HOJA_INGRESO_INFORME["encabezados"]
      )
    listado = []
    for nombre in data["datos"]:
      listado.append(nombre[0])
    
    return listado
  
  def elimina_ingresados(self, listahermanos: list) -> list:
    informeslistos = self.lista_nombres_informados()
    informes_faltantes = []
    for nombre in listahermanos:
      if nombre not in informeslistos:
        informes_faltantes.append(nombre)
    
    return informes_faltantes
    
  def ingresa_informe(self, data: list) -> str:
    fila = self.bd.buscafila(
      params.HOJA_INGRESO_INFORME["filainicial"],
      params.HOJA_INGRESO_INFORME["columnas"]["nombre"],
      )
    self.bd.ingresador(
      fila,
      data,
      params.HOJA_INGRESO_INFORME["columnas"]["nombre"]
      )
    
    resultado = self.guarda_cambios()
    return resultado
    
  def extraeinfo(self, nombre: str, columnas: list) -> list:
    fila = self.bd.buscadato(
      params.HOJA_DATOS["filainicial"],
      params.HOJA_DATOS["columnas"]["nombre"],
      nombre
      )
    if fila != 0:
      data = self.bd.extraefila(fila, columnas)
    else:
      data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    return data
  
  def listado_privilegios(self) -> list:
    data = self.bd.listar(
      params.HOJA_DATOS_NORMADOS["filainicial"],
      [params.HOJA_DATOS_NORMADOS["columnas"]["privilegio"]],
      params.HOJA_DATOS_NORMADOS["encabezados"]
      )
    privilegios = []
    for privilegio in data["datos"]:
      privilegios.append(privilegio[0])
    
    return privilegios
  
  def elimina_informe(self, nombre: str) -> str:
    fila = self.bd.buscadato(
      params.HOJA_INGRESO_INFORME["filainicial"],
      params.HOJA_INGRESO_INFORME["columnas"]["nombre"],
      nombre
      )
    self.bd.eliminar(fila)
    self.guarda_cambios()
    resultado = f"Informe de: {nombre} ha sido eliminado"
    
    return resultado
    
  def actualiza_datos(self, nombre: str, data: list) -> str:
    fila = self.bd.buscadato(
      params.HOJA_DATOS["filainicial"],
      params.HOJA_DATOS["columnas"]["nombre"],
      nombre
      )
    self.bd.ingresador_columnas(fila,data,params.HOJA_DATOS["columnas"]["todas"])
    resultado = self.guarda_cambios()
    
    return resultado
  
  def ingresa_nuevo_registro(self, data: list) -> str:
    filainicial = self.hojaActual["filainicial"]
    columnanombre = self.hojaActual["columnas"]["nombre"]
    
    existente = self.bd.buscadato(filainicial,columnanombre,data[0])
    
    if existente == 0:
      fila = self.bd.buscafila(filainicial,columnanombre)
      self.bd.ingresador(fila,data,columnanombre)
      resultado = self.guarda_cambios()
      return resultado
    else:
      resultado = "Registro de hermano existente"
      return resultado
  
  def elimina_registro(self, nombre: str) -> str:
    filainicial = self.hojaActual["filainicial"]
    columnanombre = self.hojaActual["columnas"]["nombre"]
    
    filaRegistro = self.bd.buscadato(filainicial,columnanombre,nombre)
    self.bd.eliminar(filaRegistro)
    resultado = self.guarda_cambios()
    return resultado
     
  def comprueba_usuario(self, nombre: str, contrasena: str) -> bool:
    filainicial = self.hojaActual["filainicial"]
    colusuario = self.hojaActual["columnas"]["usuario"]
    colpasswd = self.hojaActual["columnas"]["contrasena"]
    resultadoNombre = self.bd.buscadato(filainicial,colusuario,nombre)
    resultadoPassword = self.bd.buscadato(filainicial,colpasswd,contrasena)
    if resultadoNombre > 0 and resultadoPassword > 0:
      return True
    else:
      return False
  
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