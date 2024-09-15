from helpers import SessionSingleton
import params


def pack_st_login(coder: object, request: object) -> map:
     paquete = {}
     sesion = SessionSingleton()
     resultado = sesion.iniciarSesion(coder,request)
     if resultado:
          usuario = sesion.getUsuario(request, token=resultado)
          paquete["bienvenida"] = f"Bienvenid@ {usuario} selecciona una accion..."
          paquete["usuario"] = usuario
          paquete["redirect"] = "st_index.html"
          paquete["aut"] = resultado
     else:
          paquete["pagina"] = "st_autorizador.html"
          paquete["alerta"] = "Usuario o contraseña invalida"
     return paquete