from handlers.clientes import Clientes
from handlers.rutas import RutaActual, RutaBD
from empaquetadores.pack_rutas import inicia_ruta, ruta_existente
from helpers import mensajes, constructor_paquete, VariablesCompartidas
from cimprime import cimprime
import params

def empaquetador_clientes(request: object) -> map:
     paquete = constructor_paquete(request, "clientes.html", "Clientes mediclean")
     vc = VariablesCompartidas()

     def datos_base():
          campos_filtros = ["id","rut","cliente","direccion","comuna","telefono","otro"]
          with Clientes() as clientesbd:
               paquete["filtros_busqueda"] = clientesbd.mapdatos(columnas=campos_filtros)

     if "buscacliente" in request.form or "cliente_a_ruta" in vc.variables:
          busqueda_guardada = False
          if "cliente_a_ruta" in vc.variables:
               ubicacion_cliente = vc.get_variable("cliente_a_ruta")
               busqueda_guardada = True
               vc.del_variable("cliente_a_ruta")
          else:
               nombre = request.form.get("dato")
               filtro = request.form.get("filtro")
          with Clientes() as cl:
               paquete["listaclientes"] = cl.busca_cliente(nombre,filtro,idy=True) if not busqueda_guardada else cl.listar(filas=[ubicacion_cliente],idy=True)
               paquete["pagina"] = "clientes_busqueda.html"
          datos_base()
     
     elif "nuevocliente" in request.form: 
          accion = request.form.get("nuevocliente")
          with Clientes() as cl:
               if accion == "nuevocliente":
                    datos = cl.mapdatos()
                    for campo in datos.keys():
                         datos[campo] = request.form.get(campo)
                    cl.nuevo_cliente(datos)
               else:
                    form_nuevousuario = cl.mapdatos()
                    form_nuevousuario["id"]["dato"] = int(cl.get_id()) + 1
                    paquete["form_nuevousuario"] = form_nuevousuario
                    paquete["pagina"] = "clientes_nuevo.html"
          if accion == "nuevocliente":
               with Clientes() as cl:
                    paquete["listaclientes"] = cl.busca_cliente(datos["id"],"id",idy=True)
          datos_base()
     
     elif "modificacliente" in request.form:
          ubicacion = request.form.get("modificacliente")
          with Clientes() as cl:
               if ubicacion == "formulario_modificado" and request.form.get("idy"):
                    ubicacion = request.form.get("idy")
                    datos = cl.mapdatos()
                    for campo in datos.keys():
                         datos[campo] = request.form.get(campo)
                    cl.nuevo_cliente(datos, modificacion=int(ubicacion))
               else:
                    datos = cl.mapdatos(fila=int(ubicacion),idy=True)
                    paquete["form_modcliente"] = datos
                    paquete["pagina"] = "clientes_modifica.html"

          if request.form.get("modificacliente") == "formulario_modificado":
               with Clientes() as cl:
                    paquete["listaclientes"] = cl.busca_cliente(datos["id"],"id",idy=True)
          datos_base()

     elif "aRuta" in request.form:
          ubicacion_cliente = int(request.form.get("aRuta"))
          if not ruta_existente():
               paquete = inicia_ruta(iniciar=True,paquete=paquete,pagina="clientes.html")
               vc.put_variable(cliente_a_ruta=ubicacion_cliente)
          else:

               with Clientes() as cl:
                    columnas_datos = ["contrato","id","rut","cliente","direccion","comuna","telefono","otro"]
                    datos = cl.mapdatos(fila=ubicacion_cliente,columnas=columnas_datos)
               with RutaActual() as ra:
                    datos["indice"] = {"dato":ra.id_ruta() + 1}
                    agregado = ra.agregar_a_ruta(datos)
               paquete["alerta"] = "Cliente agregado a ruta" if agregado else "Cliente ya en ruta"
               datos_base()

     elif "bdretiros" in request.form:
          ubicacion = request.form.get("bdretiros")
          with Clientes() as cl:
               codigo_cliente = cl.getDato(fila=ubicacion, columna="id")
          with RutaBD() as rbd:
               filas = rbd.buscadato(dato=codigo_cliente,columna="id",exacto=True,buscartodo=True)
               retiros = rbd.listar(filas=filas,idy=True)

     elif "darbaja" in request.form:
          ubicacion = request.form.get("darbaja")
          with Clientes() as cl:
               cl.putDato(fila=ubicacion,
               columna="estado",
               dato="DE BAJA"
               )
               
     else:
          datos_base()
     
     return paquete
