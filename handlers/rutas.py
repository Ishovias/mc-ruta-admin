from datetime import datetime
from bd.repository import bdmediclean
from handlers.clientes import Clientes
from helpers import mensajes
import params

class RutaActual(bdmediclean):

     def __init__(self) -> None:
          super().__init__(params.RUTA_ACTUAL)
     
     def nuevaRuta(self, fecha: str, ruta: str) -> bool:
          if super().getDato(identificador="rutaencurso") != None:
               return False
          try:
               super().ingresador(
               fila=self.hoja_actual["rutaencurso"]["fila"],
               datos=[fecha,ruta],
               columnainicio=self.hoja_actual["rutaencurso"]["columna"]
               )
          except:
               return False
          else: 
               return True
     
     def getFechaRuta(self) -> str:
          return super().getDato(identificador="rutaencurso")

     def agregar_a_ruta(self, fecha: str, datos: list) -> bool:
          verificar = super().busca_datoscliente(datos[0],"rut")
          if verificar != 0:
               return False
          ubicacion = super().busca_ubicacion(None, "cliente")
          idActual = super().idActual(
               self.hoja_actual["filainicial"],
               self.hoja_actual["columnas"]["id"],
               "ID"
               )
          
          datos.insert(0,idActual)
          datos.insert(0,fecha)

          try:
               super().ingresador(
                    ubicacion,
                    datos,
                    self.hoja_actual["columnas"]["fecha"]
                    )
          except Exception as e:
               print (e)
               return False
          else:
               return True

class RutaRegistros(bdmediclean):

     def __init__(self) -> None:
          super().__init__(params.RUTAS_REGISTROS)

     def nuevaRuta(self, fecha: str, ruta: str) -> bool:
          if super().buscadato(
               filainicio=self.hoja_actual["filainicial"],
               columna=self.hoja_actual["columnas"]["fecha"],
               dato=fecha
          ):
               return False
          ingreso = super().putDato(
               datos=[fecha,ruta],
               fila=super().buscafila(),
               columna="fecha"
               )
          if ingreso:
               return True
          else: 
               return False
     
class RutaBD(bdmediclean):

     def __init__(self) -> None:
          super().__init__(params.RUTAS_BD)

     def registraMovimiento(self, datos: list) -> bool:
          try:
               super().ingresador(
                    super().buscafila(),
                    datos,
                    self.hoja_actual["columnas"]["fecha"]
               )
          except Exception as e:
               print(e)
               return False
          else:
               return True

# ------------- EMPAQUETADORES --------------------------
def empaquetador_rutaactual(request: object) -> map:
     
     paquete = {"pagina":"rutas.html"}

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
     
def empaquetador_registros_rutas(request: object) -> map:

     paquete = {"pagina":"rutasRegistros.html"}

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

