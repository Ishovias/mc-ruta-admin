from conectorbd import conectorbd
from handlers.rutas import RutaActual, RutaRegistros, RutaBD
from coder.codexpy2 import codexpy2
from coder.codexpy import codexpy
from enum import Enum

lista_rutas = {
          "login":[
               "logueo"
               ],
          "clientes":[
               "clientes",
               "nuevocliente",
               "buscacliente",
               "guardanuevocliente",
               "aRuta",
               "modificaCliente"
               ],
          "rutaactual":[
               "rutaactual",
               "iniciaruta",
               "finalizaRutaActual",
               "cliente_ruta_confirmar",
               "cliente_ruta_posponer"
               ],
          "rutas":[
               "rutas"
               ],
          "codexpy":[
               "codexpy",
               "codpy"
               ],
          "codexpy2":[
               "codexpy2",
               "codpy2",
               "decodpy2"
               ],
          "dineros":[
               "dineros"
               ]
     }

class mensajes(Enum):
     USUARIO_INCORRECTO = "Usuario o contraseña incorrecto"
     CLIENTE_GUARDADO = "Cliente guardado con éxito"
     CLIENTE_GUARDADO_ERROR = "Error en guardado o cliente preexistente"
     CLIENTE_BORRADO = "Cliente eliminado con éxito"
     CLIENTE_BORRADO_ERROR = "Error al intentar borrar cliente"
     CLIENTE_BAJA = "Cliente dado de baja del sistema"
     CLIENTE_BAJA_ERROR = "Error al intentar dar de baja en BD"
     CLIENTE_A_RUTA = "Cliente agregado a la ruta"
     CLIENTE_EN_RUTA = "Cliente YA existente en ruta o Error en BD"
     RUTA_EXISTENTE_ERROR = "Ruta existente o no finalizada en ruta actual"
     CLIENTE_CONFIRMADO = "Cliente confirmado correctamente"
     CLIENTE_CONFIRMADO_ERROR = "ERROR al intentar confirmar"
     CLIENTE_POSPUESTO = "Cliente POSTERGADO del retiro correctamente"
     CLIENTE_POSPUESTO_ERROR = "ERROR al intentar POSTERGAR"

# ---------------------- SESIONS SINGLETONS  --------------------------

class SessionSingleton:
     
     __instance = None
     __usr = {}

     def __new__(cls):
          if cls.__instance is None:
               cls.__instance = super().__new__(cls)
          return cls.__instance
     
     def iniciarSesion(self, coder: object, request: object) -> bool:
          userbd = conectorbd(conectorbd.hojaUsuarios)
          nombre = request.form["user"]
          contrasena = request.form["contrasena"]
          contrasena = coder.encripta(contrasena)
          result = userbd.comprueba_usuario(nombre,contrasena)
          userbd.cierra_conexion()
          if result:
               addr = str(request.remote_addr)
               self.__usr[addr] = nombre
               print(f"Usuario:{nombre}, Addr:{addr}")
          return result
          
     def cierraSesion(self, request: object) -> None:
          addr = str(request.remote_addr)
          del(self.__usr[addr])
          
     def getAutenticado(self, request: object) -> bool:
          addr = str(request.remote_addr)
          if addr in self.__usr:
               print(f"Conexion: {addr} - {self.__usr[addr]}")
               return True
          return False
          
     def getUsuario(self, request: object) -> str:
          addr = str(request.remote_addr)
          return self.__usr[addr]

# ---------------------- VERIFICATOKEN  --------------------------

def verificatoken(coder: object, request: object) -> bool:
     if request.args:
          if "aut" in request.args:
               aut = request.args.get("aut")
               current_token = coder.getCurrentToken()
               if aut == current_token:
                    return True
               else:
                    return False
          return True
     else:
          return False
     
# ---------------------- FUNCIONES DE EMPAQUE  --------------------------
def login(coder: object, request: object) -> map:
     paquete = {}
     sesion = SessionSingleton()
     resultado = sesion.iniciarSesion(coder,request)
     if resultado:
          paquete["pagina"] = "index.html"
     else:
          paquete["pagina"] = "autorizador.html"
     return paquete

def accionesBotones(request: object, paquete: map) -> map:
     if "clientes" in request.form:
          paquete["pagina"] = "clientes.html"
     if "rutaactual" in request.form:
          paquete = rutas(request, paquete)
     if "cierrasesion" in request.form:
          sesion = SessionSingleton()
          usr = sesion.getUsuario(request)
          paquete["alerta"] = f"Usuario {usr} - sesion cerrada"
          paquete["pagina"] = "autorizador.html"
          sesion.cierraSesion(request)
     return paquete

def clientes(request: object) -> map:
     
     paquete = {"pagina":"clientes.html"}

     if "buscacliente" in request.form:
          clientesbd = conectorbd(conectorbd.hojaClientes)
          nombre = request.form.get("nombre")
          resultados = clientesbd.busca_cliente_lista(nombre)
          clientesbd.cierra_conexion()
          
          paquete["listaclientes"] = resultados
          
     elif "nuevocliente" in request.form: 
          paquete["pagina"] = "nuevoCliente.html"
     
     elif "guardanuevocliente" in request.form:
          data = [
               "activo",
               request.form.get("rut"),
               request.form.get("nombre"),
               request.form.get("direccion"),
               request.form.get("comuna"),
               request.form.get("telefono"),
               request.form.get("gps"),
               request.form.get("otros")
               ]
          bd = conectorbd(conectorbd.hojaClientes)
          if bd.nuevo_cliente(data) and bd.guarda_cambios():
               paquete["alerta"] = mensajes.CLIENTE_GUARDADO.value
          else:
               paquete["alerta"] = mensajes.CLIENTE_GUARDADO_ERROR.value
          bd.cierra_conexion()
     
     elif "modificaCliente" in request.form:
          clientesbd = conectorbd(conectorbd.hojaClientes)
          identificador = request.form.get("clienteSeleccion")
          resultados = clientesbd.busca_datoscliente(identificador,"rut")
          clientesbd.cierra_conexion()
          
          paquete["modificacion"] = resultados
     
     elif "aRuta" in request.form:
          rutaactualbd = conectorbd(conectorbd.hojaRutaActual)
          
          fecha = rutaactualbd.fecha_ruta()
          
          if fecha == None:
               paquete["alerta"] = "Debes crear primero la ruta"
               paquete["nuevaruta"] = True
               paquete["pagina"] = "rutas.html"
               rutaactualbd.cierra_conexion()
          else:
               clientesbd = conectorbd(conectorbd.hojaClientes)
               identificador = request.form.get("aRuta")
               cliente = clientesbd.busca_datoscliente(identificador,"rut")
               cliente.remove(cliente[0]) # olculta eliminando el indicador estado del cliente, innecesario para lista de ruta
               aruta = rutaactualbd.agregar_a_ruta(fecha, cliente)
               rutaactualbd.fecha
               
               rutaactualbd.guarda_cambios()
               clientesbd.cierra_conexion()
               rutaactualbd.cierra_conexion()
               
               if aruta:
                    paquete["alerta"] = mensajes.CLIENTE_A_RUTA.value
               else:
                    paquete["alerta"] = mensajes.CLIENTE_EN_RUTA.value
                    
          paquete = rutas(request, paquete)
     
     elif "darbaja" in request.form:
          clientesbd = conectorbd(conectorbd.hojaClientes)
          identificador = request.form.get("rut")
          dadobaja = clientesbd.estado_cliente(identificador,"de baja")
          guardado = clientesbd.guarda_cambios()
          if dadobaja and guardado:
               paquete["alerta"] = mensajes.CLIENTE_BAJA.value
          else:
               paquete["alerta"] = mensajes.CLIENTE_BAJA_ERROR.value
               
          clientesbd.cierra_conexion()
     
     elif "guardamod" in request.form:
          bd = conectorbd(conectorbd.hojaClientes)
          rut = request.form.get("rut")
          data = [
               rut,
               request.form.get("nombre"),
               request.form.get("direccion"),
               request.form.get("comuna"),
               request.form.get("telefono"),
               request.form.get("gps"),
               request.form.get("otros")
               ]
          guardado = bd.guardar_modificacion(rut,data)
          grabado = bd.guarda_cambios()
          if guardado and grabado:
               paquete["alerta"] = mensajes.CLIENTE_GUARDADO.value
          else:
               paquete["alerta"] = mensajes.CLIENTE_GUARDADO_ERROR.value
          
          bd.cierra_conexion()

     return paquete

def rutas(request: object, paquete: map) -> map:
          
     paquete = {"pagina":"rutas.html", "nombrePagina":"RUTA EN CURSO"}
     
     def iniciaRuta(paquete: map) -> map:
          rutaactualbd = RutaActual()
          rutaregistros = RutaRegistros()
          
          fecha = request.form.get("fecha").replace("-","")
          ruta = request.form.get("nombreruta")
          nueva_rutaActual = rutaactualbd.nuevaRuta(fecha,ruta)
          rutaactualbd.guardarCerrar()
          nueva_rutaRegistro = rutaregistros.nuevaRuta(fecha,ruta)
          rutaregistros.guardarCerrar()
          print(f"RutaActualOK:{nueva_rutaActual} - RutaRegistroOK:{nueva_rutaRegistro}")
          if nueva_rutaActual and nueva_rutaRegistro:
               paquete["alerta"] = "Ruta creada"
          else:
               paquete["alerta"] = "Error en creacion de ruta o ruta existente no finalizada"
          
          return paquete
     
     def finalizaRutaActual(paquete: map) -> map:
          rutaactualbd = RutaActual()
          rutaregistros = RutaRegistros()
          
          datosExistentes = rutaactualbd.listar()
          if len(datosExistentes["datos"]) > 0:
               paquete["alerta"] = "ERROR: AUN QUEDAN CLIENTES POR CONFIRMAR O DESCARTAR"
          else:
               fechaexistente = rutaactualbd.getData(identificador="rutaencurso")
               
               identificadores = [
                    "rutaencurso",
                    "nombreruta",
                    "REALIZADO",
                    "POSPUESTO",
                    "DEUDA"
               ]
               
               datos = []
               for identificador in identificadores:
                    datos.append(rutaactualbd.getData(identificador=identificador))
               datos.append("RUTA FINALIZADA")

               rutaregistros.ingresoData(
                    datos=datos,
                    fila=rutaregistros.ubicacionLibre(),
                    columna="fecha"
               )
               for identificador in identificadores:
                    rutaactualbd.ingresoData(dato="", identificador=identificador)
               
               paquete["alerta"] = f"Ruta {fechaexistente} finalizada"
               
               rutaactualbd.guardaDatos()
               rutaregistros.guardaDatos()

          rutaactualbd.cerrarConexion()
          rutaregistros.cerrarConexion()
          
          return paquete

     def clienteRutaConfPos(paquete: map, confpos: str) -> map:
          
          def confpos(realizadopospuesto: str, mensaje_ok: str, mensaje_bad: str) -> bool:
               
               rutabd = RutaBD()
               rutaregistros = RutaRegistros()
               rutaactualbd = RutaActual()
               
               cliente_rut = request.form.get("cliente_ruta_confirmar")
               datos_cliente_confirmado = rutaactualbd.busca_datoscliente(cliente_rut,"rut")
               datos_cliente_confirmado.append(realizadopospuesto)
               # Traslado de cliente a BD
     
               ingresobd = rutabd.registraMovimiento(datos_cliente_confirmado)
     
               # incremento indicador de clientes realizados o pospuestos
               cantregistrada = rutaregistros.getData(identificador=realizadopospuesto)
               rutaregistros.ingresoData(
                    str(int(cantregistrada) + 1),
                    identificador=realizadopospuesto
               )
               # 
               rutaactualbd.eliminaData(rutaactualbd.ubicar(cliente_rut,"rut"))
               if ingresobd and rutabd.guardarCerrar() and rutaactualbd.guardarCerrar():
                    paquete["alerta"] = mensaje_ok
               else:
                    paquete["alerta"] = mensaje_bad
                    
               return paquete
          
          if confpos == "REALIZADO":
               paquete = confpos(
                    "REALIZADO", 
                    mensajes.CLIENTE_CONFIRMADO.value, 
                    mensajes.CLIENTE_CONFIRMADO_ERROR
                    )
          elif confpos == "POSPUESTO":
               paquete = confpos(
                    "POSPUESTO", 
                    mensajes.CLIENTE_POSPUESTO.value, 
                    mensajes.CLIENTE_POSPUESTO_ERROR.value
                    )
          
          return paquete

     def listarRutaActual(paquete: map) -> map:
          ractualbd = RutaActual()
     
          rutaActiva = ractualbd.getData(identificador="rutaencurso")
          rutaDatos = ractualbd.listarData()
          if rutaActiva:
               paquete["ruta"] = f"Ruta activa: {rutaActiva}"
          else:
               paquete["ruta"] = None
          paquete["rutaLista"] = rutaDatos["datos"]
          
          ractualbd.cerrarConexion()
          return paquete
          
     return paquete
     
def registros_rutas(request: object, paquete: map) -> map:
     rutabd = conectorbd(conectorbd.hojaRutabd)
     rutaregistros = conectorbd(conectorbd.hojaRutasRegistros)
     
     paquete = {"pagina":"rutasRegistros.html"}
     
     paquete["rutaLista"] = rutaregistros.listar_datos()
     
     
     
     rutabd.cierra_conexion()
     rutaregistros.cierra_conexion()
     return paquete

def codex(coder: object, request: object, paquete: map) -> map:
     paquete = {"pagina":"codexpy.html","urlfor":"codex"}
     if request.form:
          if "codpy2" in request.form:
               frase = request.form.get("ingreso")
               paquete["resultado"] = coder.encripta(frase)
          elif "decodpy2" in request.form:
               frase = request.form.get("ingreso")
               paquete["resultado"] = coder.desencripta(frase)
     else:
          paquete["resultado"] = ""
     return paquete

def codex1(request: object, paquete: map) -> map:
     coder = codexpy()
     paquete = {"pagina":"codexpy.html","urlfor":"codex1"}
     if request.form:
          if "codpy" in request.form:
               frase = request.form["ingreso"]
               paquete["resultado"] = coder.procesa(frase)
     else:
          paquete["resultado"] = ""
     return paquete

# ------------------- EMPAQUETADOR DE DATOS -------------------------
def empaquetador(coder: object, request: object, destino: str) -> map:
     
     paquete = {}
     
     # EMPAQUETADO DE DATOS PARA PLANTILLA
     if destino == "index":
          paquete["pagina"] = "index.html"
     
     elif destino == "login":
          paquete = login(coder,request)
     
     elif destino == "clientes":
          paquete = clientes(request)
          
     elif destino == "rutaactual":
          paquete = rutas(request, paquete)
     
     elif destino == "codexpy":
          paquete = codex1(request, paquete)

     elif destino == "codexpy2":
          paquete = codex(coder, request, paquete)
          
     elif destino == "rutas":
          paquete = registros_rutas(request, paquete)

     return paquete
          
