from werkzeug.utils import secure_filename
from flask import request
from datetime import datetime, date
from handlers.clientes import Clientes
from handlers.eliminaciones import RetirosEliminados, EliminacionRegistros
from handlers.rutas import RutaActual, RutaBD, RutaRegistros, RutaImportar, cimprime
from handlers.inventarios import Inventario
from helpers import mensajes, privilegios, constructor_paquete
from cimprime import cimprime
import params
import os

def inicia_ruta(iniciar: bool=False, paquete: map=None, pagina: str=None) -> map:
    if iniciar:
        columnas = ["fecharuta","nombreruta","realizado","pospuesto"]
        with RutaActual() as ra:
            paquete["nuevaruta"] = ra.mapdatos(columnas=columnas)
        paquete["pagina"] = "rutas_nueva.html"
        paquete["pagina_respuesta"] = pagina
    else:
        datos_guardados = False
        with RutaActual() as ra:
            datos_guardados = ra.nueva_ruta(
                fecha=request.form.get("fecharuta"),
                ruta=request.form.get("nombreruta")
            )
        with RutaRegistros() as reg:
            reg.nueva_ruta(
                fecha=request.form.get("fecharuta"),
                ruta=request.form.get("nombreruta")
            )
        paquete["alerta"] = "Ruta creada" if datos_guardados else "Error al crear ruta"
        paquete["pagina"] = pagina if pagina else "rutas.html"
    return paquete

def ruta_existente() -> str:
    with RutaActual() as ra:
        datoexistente = ra.getDato(
            fila=ra.hoja_actual["filadatos"],
            columna="fecharuta"
            )
    return datoexistente

def confpos(datos: map, columnas: list, columnas_inventario: list, confpos: str="realizado") -> map:
    # GRABAR CLIENTE CONF-POS EN BD
    with RutaBD() as rbd:
        bd_ubicacion = rbd.buscafila()
        for columna in list(rbd.hoja_actual["columnas"].keys()):
            if columna in datos:
                rbd.putDato(
                        dato=datos[columna]["dato"],
                        fila=bd_ubicacion,
                        columna=columna
                        )
    # Sumar cliente confirmado o pospuesto a registro
    with RutaRegistros() as reg:
        ubicacion = reg.ubicacion_registro(datos)
        reg.cliente_confpos(ubicacion, confpos)
    # MODIFICAR EL STOCK
    if confpos == "realizado":
        with Inventario() as inv:
            for columna in columnas_inventario:
                stock_descontado = datos[columna]["dato"]
                if stock_descontado:
                    stock_actual = inv.getDato(
                            fila=inv.hoja_actual["filaStockActual"],
                            columna=columna
                            )
                    nuevo_stock = int(stock_actual) - int(stock_descontado)
                    inv.putDato(
                            dato=nuevo_stock,
                            fila=inv.hoja_actual["filaStockActual"],
                            columna=columna
                            )
    cimprime(titulo="LOGICA DE CONFPOS",datos=datos, confpos=confpos)

def empaquetador_rutaactual(request: object) -> map:
    paquete = constructor_paquete(request,"rutas.html","RUTA EN CURSO")

    def datos_base():
        with RutaActual() as ractual:
            paquete["rutaLista"] = ractual.listar(
                    columnas=["indice","id_ruta","contrato","rut","cliente","direccion","comuna","telefono","otro"],
                    idy=True
                    )
            rutaactual = ractual.mapdatos(
                    fila=ractual.hoja_actual["filadatos"],
                    columnas=["fecharuta","nombreruta"]
                    )
        if rutaactual["fecharuta"]["dato"]:
            paquete["ruta"] = f" {rutaactual['fecharuta']['dato']} - {rutaactual['nombreruta']['dato']}"
        else:
            paquete["pagina"] = "rutas_nueva.html"

    def form_confpos(confpos: str):
        columnas = ["fecha","id_ruta","id","contrato","rut","cliente","direccion","comuna","telefono","otro"]
        columnas_inventario = params.INVENTARIOS["insumos_ruta"]
        bdrutas = False
        with Inventario() as inv:
            inventario_actual = inv.mapdatos(
                    columnas=columnas_inventario
                    )
        # EXTRACCION DE DATOS E INSUMOS DEL CLIENTE
        with RutaActual() as ra:
            if ubicacion == "formulario_respuesta":
                ubicacion_cliente_ra = int(request.form.get("idy"))
                datos = ra.mapdatos(fila=ubicacion_cliente_ra)
                datos["fecharuta"] = ra.getDato(
                        fila=ra.hoja_actual["filadatos"],
                        columna=["fecharuta"]
                        )
                datos["nombreruta"] = ra.getDato(
                        fila=ra.hoja_actual["filadatos"],
                        columna=["nombreruta"]
                        )
                datos["detalleretiro"] = request.form.get("detalleretiro")
                if confpos == "realizado":
                    for columna in columnas_inventario:
                        datos[columna] = {"dato":request.form.get(columna)}
                confpos(datos,columnas,columnas_inventario,confpos)
            else:
                datos = ra.mapdatos(fila=int(ubicacion), columnas=columnas,idy=True)
                if confpos == "realizado":
                    for clave, valor in inventario_actual.items():
                        datos[clave] = valor 
                datos["detalleretiro"] = {"encabezado":"Detalle del retiro"}
                paquete[f"formulario_confpos"] = datos
                if confpos == "realizado":
                    paquete["botonconfpos"] = "CONFIRMAR CLIENTE"
                else:
                    paquete["botonconfpos"] = "POSPONER CLIENTE"
                paquete["nombrePagina"] = f"Formulario de cliente {confpos}"
                paquete["pagina"] = "rutas_confpos.html"

    if "iniciaruta" in request.form:
        if "pagina_respuesta" in request.form:
            paginarespuesta = request.form.get("pagina_respuesta")
            paquete = inicia_ruta(paquete=paquete, pagina=paginarespuesta)
        elif request.form.get("nombreruta"):
            paquete = inicia_ruta(paquete=paquete)
            datos_base()
        else:
            paquete = inicia_ruta(iniciar=True,paquete=paquete)
            datos_base()
        return paquete

    elif "finalizaRutaActual" in request.form:
        pass

    elif "reubicar" in request.form:
        pass

    elif "cliente_ruta_confirmar" in request.form:
        ubicacion = request.form.get("cliente_ruta_confirmar")
        form_confpos(confpos="realizado")

    elif "cliente_ruta_posponer" in request.form:
        ubicacion = request.form.get("cliente_ruta_posponer")
        form_confpos(confpos="posponer")

    elif "cliente_ruta_eliminar" in request.form:
        ubicacion = int(request.form.get("cliente_ruta_eliminar"))
        with RutaActual() as ra:
            ra.eliminar(ubicacion)
        datos_base()

    elif "agregaclientemanual" in request.form:
        pass

    elif "enCamino" in request.form:
        pass

    else:
        datos_base()

    return paquete

def empaquetador_registros_rutas(request: object) -> map:
    paquete = constructor_paquete(request,"rutas_registros.html","REGISTRO DE RUTAS")
    
    def datos_base():
        with RutaRegistros() as rutaregistros:
            paquete["rutaLista"] = rutaregistros.listar()

    if "detalle_ruta_registro" in request.form:
        fecharuta = request.form.get("detalle_ruta_registro")
        with RutaBD() as rbd:
            ubicaciones = rbd.buscadato(
                    dato = fecharuta,
                    columna = "fecha",
                    buscartodo = True
                    )
            paquete["rutaResultado"] = rbd.listar(filas=ubicaciones,idy=True)

    elif "agrega_eliminacion" in request.form:
        pass

    elif "lista_eliminacion" in request.form:
        pass

    elif "eliminar_desechos" in request.form:
        pass

    elif "cancelar_eliminacion" in request.form:
        pass

    elif "eliminar_ruta" in request.form:
        pass

    else:
        datos_base()

    return paquete

def empaquetador_carga_ruta(request: object, app: object) -> map:
    paquete = constructor_paquete(request,"cargaruta.html","CARGA DE RUTA POR XLSX")
    
    def fichero_permitido(archivo: str) -> bool:
        return "." in archivo and archivo.rsplit(".",1)[1].lower() in params.EXTENSIONES_PERMITDAS
    
    if "archivo" in request.files:
        if "archivo" not in request.files:
            paquete["alerta"] = "ERROR 1, por favor, reintente"
            return paquete
        file = request.files["archivo"]
        if file.filename == "":
            paquete["alerta"] = "ERROR no se ha ingresado un archivo"
            return paquete
        if file and fichero_permitido(file.filename):
            filename = secure_filename(file.filename)
            archivo_cargado = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(archivo_cargado)
            with RutaImportar(archivo_cargado) as ri:
                datos = ri.extrae_ruta()
            os.system(f"rm {archivo_cargado}")
            with RutaRegistros() as rr:
                if not rr.registra_importacion(datos):
                    paquete["alerta"] = "ERROR fecha de ruta ya esta trabajada"
                    return paquete
            with RutaActual() as ra:
                if not ra.importar(datos):
                    paquete["alerta"] = "ERROR al intentar importar los datos extraidos del archivo"
                    return paquete
            paquete["alerta"] = "Archivo cargado con exito"
        else:
            paquete["alerta"] = "Tipo de archivo no permitido"
    
    return paquete

