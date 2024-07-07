from conectorbd import conectorbd
from coder.codexpy2 import codexpy2
from coder.codexpy import codexpy
from enum import Enum

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
          paquete["redirect"] = "nuevoCliente"
     
     elif "modificaCliente" in request.form:
          clientesbd = conectorbd(conectorbd.hojaClientes)
          identificador = request.form.get("clienteSeleccion")
          resultados = clientesbd.busca_datoscliente(identificador,"rut")
          clientesbd.cierra_conexion()
          
          paquete["modificacion"] = resultados
     
     elif "aRuta" in request.form:
          rutaactualbd = conectorbd(conectorbd.hojaRutaActual)
          
          verificafecha = rutaactualbd.fecha_ruta()
          
          if verificafecha == None:
               paquete["alerta"] = "Debes crear primero la ruta"
               paquete["nuevaruta"] = True
               paquete["pagina"] = "rutas.html"
               rutaactualbd.cierra_conexion()
          else:
               clientesbd = conectorbd(conectorbd.hojaClientes)
               identificador = request.form.get("aRuta")
               cliente = clientesbd.busca_datoscliente(identificador,"rut")
               cliente.remove(cliente[0]) # Elimina el indicador estado del cliente
               aruta = rutaactualbd.agregar_a_ruta(cliente)
               
               rutaactualbd.guarda_cambios()
               clientesbd.cierra_conexion()
               rutaactualbd.cierra_conexion()
               
               if aruta:
                    paquete["alerta"] = mensajes.CLIENTE_A_RUTAs.value
               else:
                    paquete["alerta"] = mensajes.CLIENTE_EN_RUTA.value
                    
     
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

def nuevoCliente(request: object, paquete: map) -> map:
     paquete["pagina"] = "nuevoCliente.html"
          
     if "guarda" in request.form:
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
          guardado = bd.nuevo_cliente(data)
          grabado = bd.guarda_cambios()
          if guardado and grabado:
               paquete["alerta"] = mensajes.CLIENTE_GUARDADO.value
          else:
               paquete["alerta"] = mensajes.CLIENTE_GUARDADO_ERROR.value
          bd.cierra_conexion()
     return paquete

def rutas(request: object, paquete: map) -> map:
     paquete = {"pagina":"rutas.html"}

     if "iniciaruta" in request.form:
          fecha = request.form.get("fecha").replace("-","")
          ruta = request.form.get("nombreruta")
          rutaactualbd = conectorbd(conectorbd.hojaRutaActual)
          if rutaactualbd.fecha_ruta() == None:
               bdrutasregistros = conectorbd(conectorbd.hojaRutasRegistros)
               nuevaruta = bdrutasregistros.nueva_ruta([fecha,ruta])
               nuevarutaactual = rutaactualbd.fecha_ruta(fecha)
               if nuevaruta and nuevarutaactual:
                    paquete["alerta"] = "Ruta creada"
                    bdrutasregistros.guarda_cambios()
                    rutaactualbd.guarda_cambios()
               else:
                    paquete["alerta"] = "Error en creacion de ruta"
               bdrutasregistros.cierra_conexion()
               rutaactualbd.cierra_conexion()
          else:
               paquete["alerta"] = mensajes.RUTA_EXISTENTE_ERROR.value
               rutaactualbd.cierra_conexion()
               
     rutabd = conectorbd(conectorbd.hojaRutaActual)
     rutaActiva = rutabd.fecha_ruta()
     rutaDatos = rutabd.listar_datos()
     if rutaActiva != None:
          paquete["ruta"] = rutaActiva
     else:
          paquete["ruta"] = None
     paquete["rutaActual"] = rutaDatos
     rutabd.cierra_conexion()
               
     return paquete
     
def codex(coder: object, request: object, paquete: map) -> map:
     paquete = {"pagina":"codexpy.html","urlfor":"codex"}
     if request.form:
          if "codpy2" in request.form:
               frase = request.form["ingreso"]
               paquete["resultado"] = coder.encripta(frase)
          elif "decodpy2" in request.form:
               frase = request.form["ingreso"]
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
     '''
     elif ruta == "nuevocliente":
          paquete = nuevoCliente(request, paquete)
          

     '''  
     return paquete
          
