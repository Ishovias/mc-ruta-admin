from helpers import SessionSingleton, privilegios

def empaquetador_usersactives(request: object) -> map:
     paquete = {"pagina":"usersActives.html", "aut":request.args.get("aut")}
     privilegio = privilegios(request,paquete,retornaUser=True)
     paquete = privilegio["paquete"]
     usuario = privilegio["usuario"]
     paquete["usuario"] = usuario
     
     eliminatoken = None
     
     if "elimina" in request.form:
          eliminatoken = request.form.get("elimina")
     
     with SessionSingleton() as sesion:
          if eliminatoken:
               sesion.delUser(eliminatoken)
          usersMap = sesion.getUsersMap()
          listaUsuarios = []
          for dato in usersMap:
               listaUsuarios.append([usersMap[dato],dato])
          paquete["usuarios"] = listaUsuarios
     
     return paquete