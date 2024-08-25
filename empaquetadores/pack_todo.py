from helpers import privilegios
from handlers.todo import Todo

def empaquetador_todo(request: object) -> map:
     paquete = {"pagina":"todo.html", "aut":request.args.get("aut")}
     privilegio = privilegios(request,paquete,retornaUser=True)
     paquete = privilegio["paquete"]
     usuario = privilegio["usuario"]
     paquete["usuario"] = usuario
     
     with Todo() as td:
          if "agrega" in request.form:
               nuevatarea = request.form.get("ingreso")
               resultado = td.nuevatarea(nuevatarea)
               if not resultado:
                    paquete["alerta"] = "Ya existe una tarea con el mismo nombre"
          elif "completa" in request.form:
               tarea = request.form.get("completa")
               td.accion(tarea,"COMPLETADO")
          elif "encurso" in request.form:
               tarea = request.form.get("encurso")
               td.accion(tarea,"EN CURSO")
          elif "posterga" in request.form:
               tarea = request.form.get("posterga")
               td.accion(tarea,"POSTERGADO")
          elif "elimina" in request.form:
               tarea = request.form.get("elimina")
               td.eliminatarea(tarea)
               
          paquete["resultados"] = td.listar()


     return paquete