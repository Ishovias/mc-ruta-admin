from conectorbd import conectorbd
from enum import Enum
import params
import datetime

class mensajes(Enum):
     USUARIO_INCORRECTO = "Usuario o contraseña incorrecto"
     CLIENTE_GUARDADO = "Cliente guardado con éxito"
     CLIENTE_GUARDADO_ERROR = "Error en guardado o cliente preexistente"
     CLIENTE_BORRADO = "Cliente eliminado con éxito"
     CLIENTE_BORRADO_ERROR = "Error al intentar borrar cliente"

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

def comprueba_usuario(coder: object, request: object) -> bool:
     userbd = conectorbd(conectorbd.hojaUsuarios)
     nombre = request.form["user"]
     contrasena = request.form["contrasena"]
     contrasena = coder.encripta(contrasena)
     result = userbd.comprueba_usuario(nombre,contrasena)
     userbd.cierra_conexion()
     return result

def empaquetador(coder: object, request: object, ruta: str="") -> map:
     
     def extrae_rut(clave: str) -> str:
          clave = list(clave)
          rut = []
          for caracter in clave:
             if caracter != " ":
                  rut.append(caracter)
             else:
                  rut = "".join(rut)
                  return rut
     
     paquete = {}
     
     if "aut" in request.args:
          paquete["aut"] = coder.setToken(request.args.get("aut"))
     else:
          paquete["aut"] = coder.getCurrentToken()
     
     paquete["habilitador"] = "enabled"
     
     if ruta == "login":
          paquete["pagina"] = "autorizador.html"
          paquete["habilitador"] = "disabled"
          if "alerta" in request.args:
               paquete["alerta"] = request.args.get("alerta")
     
     elif ruta == "accionesBotones":
          if "clientes" in request.form:
               paquete["pagina"] = "clientes.html"
               
     elif ruta == "clientes":
          paquete["pagina"] = "clientes.html"
     
          if "buscacliente" in request.form:
               clientesbd = conectorbd(conectorbd.hojaClientes)
               nombre = request.form.get("nombre")
               resultados = clientesbd.busca_cliente_lista(nombre)
               clientesbd.cierra_conexion()
               
               paquete["listaclientes"] = resultados
               
          elif "nuevocliente" in request.form:
               paquete["redirect"] = "nuevoCliente"
          
          elif "modifica" in request.form:
               clientesbd = conectorbd(conectorbd.hojaClientes)
               identificador = request.form.get("seleccioncliente")
               rut = extrae_rut(identificador)
               resultados = clientesbd.busca_datoscliente(rut,"rut")
               clientesbd.cierra_conexion()
               
               paquete["modificacion"] = resultados
          
          elif "eliminar" in request.form:
               clientesbd = conectorbd(conectorbd.hojaClientes)
               identificador = request.form.get("seleccioncliente")
               rut = extrae_rut(identificador)
               eliminado = clientesbd.elimina_cliente(identificador)
               guardado = clientesbd.guarda_cambios()
               if eliminado and guardado:
                    paquete["alerta"] = mensajes.CLIENTE_BORRADO.value
               else:
                    paquete["alerta"] = mensajes.CLIENTE_BORRADO_ERROR.value
                    
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
               
     elif ruta == "nuevocliente":
          paquete["pagina"] = "nuevoCliente.html"
          
          if "guarda" in request.form:
               data = [
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
               
     elif ruta == "rutaActual":
          paquete["pagina"] = "rutas.html"     
   
     return paquete
          
