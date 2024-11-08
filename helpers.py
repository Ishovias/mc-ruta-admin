from handlers.usuarios import Usuariosbd
from coder.codexpy import codexpy
from enum import Enum

# ---------------------- MENSAJES PREDEFINIDOS ----------------------
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
     
     def __enter__(self) -> object:
          return self
     
     def iniciarSesion(self, coder: object, request: object) -> bool:
          nombre = request.form["user"]
          contrasena = request.form["contrasena"]
          contrasena = coder.encripta(contrasena)
          with Usuariosbd() as userbd:
               result = userbd.comprueba_usuario(nombre,contrasena)
          if result:
               token = coder.gtoken()
               self.__usr[token] = nombre
               with Usuariosbd() as ubd:
                    ubd.registra_token(usuario=nombre,token=token)
               return token
          return result
          
     def cierraSesion(self, request: object) -> None:
          token = request.args.get("aut")
          with Usuariosbd() as ubd:
               ubd.elimina_token(token)
          del(self.__usr[token])
          
     def getAutenticado(self, request: object) -> bool:
          token = request.args.get("aut")
          if token in self.__usr:
               return True
          elif request.args.get("aut"): # Comprobacion token largo plazo
               with Usuariosbd() as ubd:
                    usuario = ubd.token_existente(request.args.get("aut"))
                    if usuario:
                         self.__usr[token] = usuario
                         return True
                    else:
                         return False
          return False
          
     def getUsuario(self, request: object, token: str=None) -> str:
          if not token:
               token = request.args.get("aut")
          if token in self.__usr:
               return self.__usr[token]
          return None
     
     def getUsersMap(self) -> map:
          return self.__usr
     
     def delUser(self, tokenEliminar: str, tokenUsuarioActual: str) -> bool:
          if tokenEliminar != tokenUsuarioActual:
               with Usuariosbd() as ubd:
                    ubd.elimina_token(tokenEliminar)
               del(self.__usr[tokenEliminar])
               return True
          return False
     
     def __exit__(self, exc_type, exc_value, traceback) -> None:
          pass

# ---------------------- VERIFICATOKEN  --------------------------
def verificatoken(request: object) -> bool:
     if request.args:
          if "aut" in request.args:
               with SessionSingleton() as sesion:
                    if sesion.getAutenticado(request):
                         return True
                    else:
                         return False
     else:
          return False

# ---------------------- RETORNO DE PRIVILEGIOS ----------------------
priv = {
     "iberoiza":{
          "cpEnabled":"enabled",
          "finEnabled":"enabled",
          "inirutaEnabled":"enabled",
          "newclienteEnabled":"enabled",
          "arutaEnabled":"enabled",
          "modclienteEnabled":"enabled",
          "reubicarEnabled":"enabled"
     },
     "mjose":{
          "cpEnabled":"enabled",
          "finEnabled":"disabled",
          "inirutaEnabled":"disabled",
          "newclienteEnabled":"disabled",
          "arutaEnabled":"disabled",
          "modclienteEnabled":"disabled",
          "reubicarEnabled":"enabled"
     },
     "invitado":{
          "cpEnabled":"disabled",
          "finEnabled":"disabled",
          "inirutaEnabled":"disabled",
          "newclienteEnabled":"disabled",
          "arutaEnabled":"disabled",
          "modclienteEnabled":"disabled",
          "reubicarEnabled":"enabled"
     }
}

def privilegios(request: object, paquete: map, retornaUser: bool=False) -> map:
     with SessionSingleton() as sesion:
          usuario = sesion.getUsuario(request)
     if usuario in priv:
          for boton in priv[usuario]:
               paquete[boton] = priv[usuario][boton]
     if retornaUser:
          return {"paquete":paquete, "usuario":usuario}
     return paquete

# ---------------------- FUNCIONES DE EMPAQUE  --------------------------
def empaquetador_login(coder: object, request: object) -> map:
     paquete = {}
     sesion = SessionSingleton()
     resultado = sesion.iniciarSesion(coder,request)
     if resultado:
          usuario = sesion.getUsuario(request, token=resultado)
          paquete["bienvenida"] = f"Bienvenido {usuario} selecciona una accion..."
          paquete["usuario"] = usuario
          paquete["redirect"] = "index.html"
          paquete["aut"] = resultado
     else:
          paquete["pagina"] = "autorizador.html"
          paquete["alerta"] = "Usuario o contraseña invalida"
     return paquete

def empaquetador_codex2(coder: object, request: object) -> map:
     paquete = {"pagina":"codexpy.html", "aut":request.args.get("aut")}
     privilegio = privilegios(request,paquete,retornaUser=True)
     paquete = privilegio["paquete"]
     usuario = privilegio["usuario"]
     paquete["usuario"] = usuario
     paquete["urlfor"] = "codex"

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

def empaquetador_codex1(request: object) -> map:
     coder = codexpy()
     
     paquete = {"pagina":"codexpy.html", "aut":request.args.get("aut")}
     privilegio = privilegios(request,paquete,retornaUser=True)
     paquete = privilegio["paquete"]
     usuario = privilegio["usuario"]
     paquete["usuario"] = usuario
     paquete["urlfor"] = "codex1"
     
     if request.form:
          if "codpy" in request.form:
               frase = request.form["ingreso"]
               paquete["resultado"] = coder.procesa(frase)
     else:
          paquete["resultado"] = ""
     return paquete

def cimprime(**kwargs) -> None:
     if "titulo" in kwargs.keys():
          print(kwargs["titulo"])
     else:
          print("VARIABLES MONITOREADAS")
     print("--------------------------")
     for llave in kwargs.keys():
          if llave != "titulo":
               print(f"{llave}: {kwargs[llave]}")
     print("--------------------------\n")

def constructor_paquete(request: object, pagina: str, nombrePagina: str=None) -> map:
     paquete = {"pagina":pagina,"aut":request.args.get("aut"), "nombrePagina":nombrePagina}
     privilegio = privilegios(request, paquete, retornaUser=True)
     paquete = privilegio["paquete"]
     paquete["usuario"] = privilegio["usuario"]
     return paquete
     
def formatear_precio(precio: int) -> int:
     precio = "{:,}".format(precio)
     precio = list(precio)
     precio.insert(0,"$")
     return "".join(precio)

def seleccionar_conjunto_elementos(hoja: map, nombreDesde: str, nombreHasta: str) -> list:
     desde = False
     listaItems = []
     for elemento in hoja["columnas"].keys():
          if nombreDesde == elemento:
               desde = True
               listaItems.append(elemento)
          elif nombreHasta == elemento:
               listaItems.append(elemento)
               break
          elif desde:
               listaItems.append(elemento)
     return listaItems

