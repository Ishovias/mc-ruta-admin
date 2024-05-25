from conectorbd import conectorbd
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

# ---------------------- FUNCIONES DE EMPAQUE  --------------------------
def login(request: object, paquete: map) -> map:
     paquete["pagina"] = "autorizador.html"
     paquete["habilitador"] = "disabled"
     if "alerta" in request.args:
          paquete["alerta"] = request.args.get("alerta")
     
     return paquete

def accionesBotones(request: object, paquete: map) -> map:
     if "clientes" in request.form:
          paquete["pagina"] = "clientes.html"
     if "rutaactual" in request.form:
          paquete = rutas(request, paquete)
          
     return paquete

def clientes(request: object, paquete: map) -> map:
     paquete["pagina"] = "clientes.html"

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
     paquete["pagina"] = "rutas.html"

     rutabd = conectorbd(conectorbd.hojaRutaActual)
     paquete["rutaActual"] = rutabd.listar_datos()
     rutabd.cierra_conexion()

     if "iniciaruta" in request.form:
          fecha = request.form.get("fecha")
          ruta = request.form.get("nombreruta")
          rutaactualbd = conectorbd(conectorbd.hojaRutaActual)
          if rutaactualbd.busca_ubicacion(fecha,"fecha") != 0:
               bdrutasregistros = conectorbd(conectorbd.hojaRutasRegistros)
               resultado = bdrutasregistros.nueva_ruta(fecha,ruta)
               if resultado:
                    paquete["alerta"] = "Ruta creada"
               else:
                    paquete["alerta"] = "Error en creacion de ruta"
               bdrutasregistros.cierra_conexion()
               rutaactualbd.cierra_conexion()
          else:
               paquete["alerta"] = mensajes.RUTA_EXISTENTE_ERROR.value
               rutaactualbd.cierra_conexion()
               
          
          
     
     
     return paquete
     

# ------------------- EMPAQUETADOR DE DATOS -------------------------
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
     
     # Creacion del paquete
     paquete = {"habilitador":"enabled"}
     
     if "aut" in request.args:
          paquete["aut"] = coder.setToken(request.args.get("aut"))
     else:
          paquete["aut"] = coder.getCurrentToken()
     
     # EMPAQUETADO DE RUTAS
     if ruta == "login":
          paquete = login(request, paquete)

     elif ruta == "accionesBotones":
          paquete = accionesBotones(request, paquete)
               
     elif ruta == "clientes":
          paquete = clientes(request, paquete)
     
     elif ruta == "nuevocliente":
          paquete = nuevoCliente(request, paquete)
          
     elif ruta == "rutas":
          paquete = rutas(request, paquete)
     
     return paquete
          
