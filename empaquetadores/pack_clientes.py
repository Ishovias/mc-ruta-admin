from handlers.clientes import Clientes
from handlers.rutas import RutaActual, RutaBD
from helpers import mensajes, constructor_paquete
from cimprime import cimprime
import params

def empaquetador_clientes(request: object) -> map:
     paquete = constructor_paquete(request, "clientes.html", "Clientes mediclean")
     
     def datos_base():
          campos_filtros = ["id","rut","cliente","direccion","comuna","otro"]
          with Clientes() as clientesbd:
               paquete["filtros_busqueda"] = clientesbd.mapdatos(columnas=campos_filtros)
     
     if "buscacliente" in request.form:
          nombre = request.form.get("dato")
          filtro = request.form.get("filtro")
          with Clientes() as cl:
               paquete["listaclientes"] = cl.busca_cliente(nombre,filtro)
          datos_base()
     
     elif "listarclientes" in request.form:
          pass
     
     elif "nuevocliente" in request.form and priv[usuario]["newclienteEnabled"] == "enabled": 
          pass
     
     elif "guardanuevocliente" in request.form:
          pass
     
     elif "modificaCliente" in request.form and priv[usuario]["modclienteEnabled"] == "enabled":
          pass
     
     elif "aRuta" in request.form  and priv[usuario]["arutaEnabled"] == "enabled":
          pass
     
     elif "bdretiros" in request.form and priv[usuario]["modclienteEnabled"] == "enabled":
          pass
     
     elif "darbaja" in request.form and priv[usuario]["modclienteEnabled"] == "enabled":
          pass
     
     elif "guardamod" in request.form:
          pass
     
     else:
          datos_base()
     
     return paquete
