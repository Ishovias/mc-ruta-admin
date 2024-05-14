from conectorbd import conectorbd
from enum import Enum
import params
import datetime

class mensajes(Enum):
     USUARIO_INCORRECTO = "Usuario o contraseña incorrecto"

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

def comprueba_usuario(request: object) -> bool:
     userbd = conectorbd(conectorbd.hojaUsuarios)
     nombre = request.form["user"]
     contrasena = request.form["contrasena"]
     result = userbd.comprueba_usuario(nombre,contrasena)
     userbd.cierra_conexion()
     return result

def empaquetador(coder: object, request: object, ruta: str) -> map:
     
     paquete = {}
     
     if "aut" in request.args:
          paquete["token"] = coder.setToken(request.args.get("aut"))
     else:
          paquete["token"] = coder.getCurrentToken()
     
     paquete["habilitador"] = "enabled"
     
     if ruta == "login":
          paquete["pagina"] = "autorizador.html"
          paquete["habilitador"] = "disabled"
          
     elif ruta == "inicio":
