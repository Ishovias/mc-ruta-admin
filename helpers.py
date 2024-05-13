from conectorbd import conectorbd

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

def empaquetador(coder: object, request: object, ruta: str) -> map:
     
     paquete = {}
     
     if "aut" in request.args:
          paquete["token"] = coder.setToken(request.args.get("aut"))
     else:
          paquete["token"] = coder.getCurrentToken()
     
     paquete["habilitador"] = "enabled"
     
     if ruta == "login":
          paquete["pagina"] = "autori"

