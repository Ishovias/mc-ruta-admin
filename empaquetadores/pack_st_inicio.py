from helpers import SessionSingleton, privilegios, constructor_paquete

def pack_st_login(coder: object, request: object) -> map:
     paquete = {}
     sesion = SessionSingleton()
     resultado = sesion.iniciarSesion(coder,request)
     if resultado:
          usuario = sesion.getUsuario(request, token=resultado)
          privilegio = privilegios(request, paquete, retornaUser=True)
          paquete = privilegio["paquete"]
          paquete["bienvenida"] = f"Bienvenid@ {usuario} selecciona una accion..."
          paquete["usuario"] = usuario
          paquete["redirect"] = "st_index.html"
          paquete["pagina"] = "st_index.html"
          paquete["aut"] = resultado
     else:
          paquete["pagina"] = "st_autorizador.html"
          paquete["alerta"] = "Usuario o contraseña invalida"
     return paquete

def pack_st_index(request: object) -> map:
     return constructor_paquete(
          request=request,
          pagina="st_index.html",
          nombrePagina="Bienvenid@"
     )
     