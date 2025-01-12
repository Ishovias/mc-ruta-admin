from handlers.clientes import Clientes
from handlers.rutas import RutaActual, RutaBD
from helpers import mensajes, constructor_paquete
from cimprime import cimprime
import params

def empaquetador_clientes(request: object) -> map:
     paquete = constructor_paquete(request, "clientes.html", "Clientes mediclean")
     
     def datos_base():
          campos_filtros = ["id","rut","cliente","direccion","comuna","telefono","otro"]
          with Clientes() as clientesbd:
               paquete["filtros_busqueda"] = clientesbd.mapdatos(columnas=campos_filtros)
     
     if "buscacliente" in request.form:
          nombre = request.form.get("dato")
          filtro = request.form.get("filtro")
          with Clientes() as cl:
               paquete["listaclientes"] = cl.busca_cliente(nombre,filtro,idy=True)
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
          pass
     
     elif "bdretiros" in request.form:
          pass
     
     elif "darbaja" in request.form:
          pass
     
     elif "guardamod" in request.form:
          pass
     
     else:
          datos_base()
     
     return paquete
