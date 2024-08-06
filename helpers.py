from handlers.rutas import RutaActual, RutaRegistros, RutaBD
from handlers.usuarios import Usuariosbd
from handlers.clientes import Clientes
from coder.codexpy2 import codexpy2
from coder.codexpy import codexpy
from enum import Enum
from datetime import datetime
import params

lista_rutas = {
          "login":[
               "logueo"
               ],
          "clientes":[
               "clientes",
               "nuevocliente",
               "buscacliente",
               "guardanuevocliente",
               "aRuta",
               "modificaCliente"
               ],
          "rutaactual":[
               "rutaactual",
               "iniciaruta",
               "finalizaRutaActual",
               "cliente_ruta_confirmar",
               "cliente_ruta_posponer"
               ],
          "rutas":[
               "rutas",
               "detalle_ruta_registro"
               ],
          "codexpy":[
               "codexpy",
               "codpy"
               ],
          "codexpy2":[
               "codexpy2",
               "codpy2",
               "decodpy2"
               ],
          "dineros":[
               "dineros"
               ]
     }

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
               addr = str(request.remote_addr)
               self.__usr[addr] = nombre
          return result
          
     def cierraSesion(self, request: object) -> None:
          addr = str(request.remote_addr)
          del(self.__usr[addr])
          
     def getAutenticado(self, request: object) -> bool:
          addr = str(request.remote_addr)
          if addr in self.__usr:
               return True
          return False
          
     def getUsuario(self, request: object) -> str:
          addr = str(request.remote_addr)
          if addr in self.__usr:
               return self.__usr[addr]
          return None
     
     def getUsersMap(self) -> map:
          return self.__usr
     
     def __exit__(self, exc_type, exc_value, traceback) -> None:
          pass

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
def login(coder: object, request: object, paquete: map) -> map:
     sesion = SessionSingleton()
     resultado = sesion.iniciarSesion(coder,request)
     if resultado:
          usuario = sesion.getUsuario(request)
          paquete["bienvenida"] = f"Bienvenido {usuario} selecciona una accion..."
          paquete["usuario"] = usuario
          paquete["pagina"] = "index.html"
     else:
          paquete["pagina"] = "autorizador.html"
     return paquete

def clientes(request: object, paquete: map) -> map:
     
     paquete ["pagina"] = "clientes.html"

     if "buscacliente" in request.form:
          
          resultados = ""
          with Clientes() as clientesbd:
               nombre = request.form.get("nombre")
               resultados = clientesbd.busca_cliente_lista(nombre)
          
          paquete["listaclientes"] = resultados
          
     elif "nuevocliente" in request.form: 
          paquete["pagina"] = "nuevoCliente.html"
     
     elif "guardanuevocliente" in request.form:
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
          
          with Clientes() as bd:
               if bd.nuevo_cliente(data):
                    paquete["alerta"] = mensajes.CLIENTE_GUARDADO.value
               else:
                    paquete["alerta"] = mensajes.CLIENTE_GUARDADO_ERROR.value
     
     elif "modificaCliente" in request.form:
          
          resultados = ""
          with Clientes() as clientesbd:
               identificador = request.form.get("clienteSeleccion")
               resultados = clientesbd.busca_datoscliente(identificador,"rut")
          
          paquete["modificacion"] = resultados
     
     elif "aRuta" in request.form:
          
          fecha = None
          with RutaActual() as rutaactualbd:
               fecha = rutaactualbd.getFechaRuta()
          
          if not fecha:
               paquete["alerta"] = "Debes crear primero la ruta"
               paquete["nuevaruta"] = True
               paquete["pagina"] = "rutas.html"
          else:
               identificador = request.form.get("aRuta")
               
               cliente = []
               with Clientes() as clientesbd:
                    cliente = clientesbd.busca_datoscliente(identificador,"rut")
                    cliente.remove(cliente[0]) # olculta eliminando el indicador estado del cliente, innecesario para lista de ruta

               aruta = False
               with RutaActual() as rutaactualbd:
                    aruta = rutaactualbd.agregar_a_ruta(fecha, cliente)

               if aruta:
                    paquete["alerta"] = mensajes.CLIENTE_A_RUTA.value
               else:
                    paquete["alerta"] = mensajes.CLIENTE_EN_RUTA.value
                    
     
     elif "darbaja" in request.form:
          dadobaja = False
          guardado = False
          
          with Clientes() as clientesbd:
               identificador = request.form.get("rut")
               dadobaja = clientesbd.estado_cliente(identificador,"de baja")

          if dadobaja and guardado:
               paquete["alerta"] = mensajes.CLIENTE_BAJA.value
          else:
               paquete["alerta"] = mensajes.CLIENTE_BAJA_ERROR.value
               
     
     elif "guardamod" in request.form:
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
          
          guardado = False
          grabado = False
          
          with Clientes() as bd:
               guardado = bd.guardar_modificacion(rut,data)

          if guardado and grabado:
               paquete["alerta"] = mensajes.CLIENTE_GUARDADO.value
          else:
               paquete["alerta"] = mensajes.CLIENTE_GUARDADO_ERROR.value

     return paquete

def rutas(request: object, paquete: map) -> map:
     
     def confpos(cliente_rut: str, realizadopospuesto: str, mensaje_ok: str, mensaje_bad: str) -> bool:
          # buscando datos del cliente y eliminando registro de ruta actual
          datos_cliente_confirmado = []
          with RutaActual() as rutaactualbd:
               datos_cliente_confirmado = rutaactualbd.busca_datoscliente(cliente_rut,"rut")
               datos_cliente_confirmado.append(realizadopospuesto)
               datos_cliente_confirmado.append(request.form.get("observacion"))
               rutaactualbd.eliminar(rutaactualbd.busca_ubicacion(cliente_rut,"rut"))
               # incremento indicador de clientes realizados o pospuestos
               cantregistrada = rutaactualbd.getDato(identificador=realizadopospuesto)
               if not cantregistrada:
                    dato = 1
               else:
                    dato = str(int(cantregistrada) + 1)
               rutaactualbd.putDato(
                    dato=dato,
                    identificador=realizadopospuesto
               )
          # Traslado de cliente a BD
          ingresobd = False
          with RutaBD() as rutabd:
               ingresobd = rutabd.registraMovimiento(datos_cliente_confirmado)
          # Anotacion de fecha en hoja clientes y calculo de proximo retiro
          ingresoclientes = False
          if realizadopospuesto == "REALIZADO":
               with Clientes() as clientesbd:
                    fecharetiro = datos_cliente_confirmado[0]
                    rutcliente = datos_cliente_confirmado[2]
                    
                    ubicacioncliente = clientesbd.busca_ubicacion(
                         dato=rutcliente,
                         columna="rut"
                         )
                    
                    ingresoclientes = clientesbd.putDato(
                         dato=fecharetiro,
                         fila=ubicacioncliente,
                         columna="ultimoretiro"
                         )
                    
                    proxfecharetiro = clientesbd.proximo_retiro(
                              rut=rutcliente,
                              fecharetiro=fecharetiro
                              )
                         
                    if proxfecharetiro:
                         proxfecha = clientesbd.putDato(
                              dato=proxfecharetiro,
                              fila=ubicacioncliente,
                              columna="proxretiro"
                              )
                    else:
                         proxfecha = False
          else:
               proxfecha = True
          
          if ingresobd and ingresoclientes and proxfecha:
               paquete["alerta"] = mensaje_ok
          else:
               paquete["alerta"] = mensaje_bad
               
          return paquete
     
     paquete["pagina"] = "rutas.html"
     paquete["nombrePagina"] = "RUTA EN CURSO"
     
     if "iniciaruta" in request.form:
          fecha = request.form.get("fecha").replace("-","")
          ruta = request.form.get("nombreruta")
          
          nueva_rutaActual = False
          nueva_rutaRegistro = False

          with RutaRegistros() as rutaregistros:
               nueva_rutaRegistro = rutaregistros.nuevaRuta(fecha,ruta)
          
          if nueva_rutaRegistro:     
               with RutaActual() as rutaactualbd:
                    nueva_rutaActual = rutaactualbd.nuevaRuta(fecha,ruta)
               
          if nueva_rutaActual and nueva_rutaRegistro:
               paquete["alerta"] = "Ruta creada"
          else:
               paquete["alerta"] = "Error en creacion de ruta o ruta existente no finalizada"
          paquete["pagina"] = "clientes.html"
          return paquete
     
     elif "finalizaRutaActual" in request.form:
          confirmacion = request.form.get("finalizaRutaActual")
          if confirmacion == "REALIZADO_FORM":
               with RutaActual() as rutaactualbd:
                    datosExistentes = rutaactualbd.listar()
               
               if len(datosExistentes["datos"]) > 0:
                    paquete["alerta"] = "ERROR: AUN QUEDAN CLIENTES POR CONFIRMAR O DESCARTAR"
               else:
                    identificadores = [
                         "rutaencurso",
                         "nombreruta",
                         "REALIZADO",
                         "POSPUESTO"
                    ]
                    
                    datos = []
                    fechaexistente = ""
                    
                    with RutaActual() as rutaactualbd:
                         fechaexistente = rutaactualbd.getDato(identificador="rutaencurso")
                         
                         for identificador in identificadores:
                              datos.append(rutaactualbd.getDato(identificador=identificador))
                         datos.append(request.form.get("observacion"))
                         
                         for identificador in identificadores:
                              rutaactualbd.putDato(dato="", identificador=identificador)
                              
                    with RutaRegistros() as rutaregistros:
                         rutaregistros.putDato(
                              datos=datos,
                              fila=rutaregistros.busca_ubicacion(dato=fechaexistente, columna="fecha"),
                              columna="fecha"
                         )
                         
                    paquete["alerta"] = f"Ruta {fechaexistente} finalizada"
          else:
               paquete["pagina"] = "rutaconf.html"
               paquete["nombrePagina"] = "Confirmar termino de ruta"
               paquete["rutaobs"] = f"{datetime.now().isoformat()} RUTA FINALIZADA"
               with RutaActual() as rutaactual:
                    paquete["rutafecha"] = rutaactual.getDato(identificador="rutaencurso")
                    paquete["rutanombre"] = rutaactual.getDato(identificador="nombreruta")
          return paquete
     
     elif "cliente_ruta_confirmar" in request.form:
          confirmacion = request.form.get("cliente_ruta_confirmar")
          if confirmacion == "REALIZADO_FORM":
               confpos(
                    request.form.get("clienterut"),
                    "REALIZADO", 
                    mensajes.CLIENTE_CONFIRMADO.value, 
                    mensajes.CLIENTE_CONFIRMADO_ERROR.value
                    )
          else:
               paquete["pagina"] = "confpos.html"
               paquete["nombrePagina"] = "Confirmar datos de cliente CONFIRMADO"
               paquete["confirmarposponer"] = "Confirmar"
               paquete["propConfPos"] = "cliente_ruta_confirmar"
               paquete["clienterut"] = confirmacion
               with RutaActual() as rutaactual:
                    paquete["clientenombre"] = rutaactual.getDato(
                         fila=rutaactual.busca_ubicacion(
                              dato=confirmacion,
                              columna="rut"
                              ),
                         columna="cliente"
                         )

     elif "cliente_ruta_posponer" in request.form:
          confirmacion = request.form.get("cliente_ruta_posponer")
          if confirmacion == "REALIZADO_FORM":
               confpos(
                    request.form.get("clienterut"),
                    "POSPUESTO", 
                    mensajes.CLIENTE_POSPUESTO.value, 
                    mensajes.CLIENTE_POSPUESTO_ERROR.value
                    )
          else:
               paquete["pagina"] = "confpos.html"
               paquete["nombrePagina"] = "Observaciones para cliente pospuesto"
               paquete["confirmarposponer"] = "Posponer"
               paquete["propConfPos"] = "cliente_ruta_posponer"
               paquete["clienterut"] = confirmacion
               with RutaActual() as rutaactual:
                    paquete["clientenombre"] = rutaactual.getDato(
                         fila=rutaactual.busca_ubicacion(
                              dato=confirmacion,
                              columna="rut"
                              ),
                         columna="cliente"
                         )

     with RutaActual() as ractualbd:
          rutaActiva = ractualbd.getDato(identificador="rutaencurso")
          rutaDatos = ractualbd.listar()
          if rutaActiva:
               paquete["ruta"] = f"Ruta activa: {rutaActiva}"
          else:
               paquete["ruta"] = None
          paquete["rutaLista"] = rutaDatos
     
     return paquete
     
def registros_rutas(request: object, paquete: map) -> map:

     paquete["pagina"] = "rutasRegistros.html"

     if "detalle_ruta_registro" in request.form:
          fecha = request.form.get("detalle_ruta_registro")
          paquete["fecha"] = f"Ruta seleccionada: {fecha}"
          
          data: list = []
          
          with RutaBD() as rutabd:
               encabezados = rutabd.extraefila(
                    fila=params.RUTAS_BD["encabezados"],
                    columnas=params.RUTAS_BD["columnas"]["todas"]
               )
               paquete["encabezados"] = encabezados
               maxfilas = rutabd.getmaxfilas()
               fila = params.RUTAS_BD["filainicial"]
               filasEncontradas = []
               
               while(fila <= maxfilas):
                    filadatos = rutabd.buscadato(
                         filainicio=fila,
                         columna=params.RUTAS_BD["columnas"]["fecha"],
                         dato=fecha
                         )
                    if filadatos:
                         filasEncontradas.append(filadatos)
                         fila = filadatos + 1
                    else:
                         break
               
               for f in filasEncontradas:
                    recopilado = rutabd.extraefila(
                         fila=f,
                         columnas=params.RUTAS_BD["columnas"]["todas"]
                         )
                    data.append(recopilado)

          paquete["rutaResultado"] = data
               
     with RutaRegistros() as rutaregistros:
          paquete["rutaLista"] = rutaregistros.listar()

     return paquete

def codex(coder: object, request: object, paquete: map) -> map:
     paquete["pagina"] = "codexpy.html"
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

def codex1(request: object, paquete: map) -> map:
     coder = codexpy()
     
     paquete["pagina"] = "codexpy.html"
     paquete["urlfor"] = "codex1"
     
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
     with SessionSingleton() as sesion:
          paquete["usuarios"] = sesion.getUsuario(request)
          
     # EMPAQUETADO DE DATOS PARA PLANTILLA
     if destino == "index":
          paquete["pagina"] = "index.html"
     
     elif destino == "login":
          paquete = login(coder,request,paquete)
     
     elif destino == "clientes":
          paquete = clientes(request,paquete)
          
     elif destino == "rutaactual":
          paquete = rutas(request, paquete)
     
     elif destino == "codexpy":
          paquete = codex1(request, paquete)

     elif destino == "codexpy2":
          paquete = codex(coder, request, paquete)
          
     elif destino == "rutas":
          paquete = registros_rutas(request, paquete)
          
     return paquete