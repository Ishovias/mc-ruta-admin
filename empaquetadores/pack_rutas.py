from werkzeug.utils import secure_filename
from flask import request
from datetime import datetime, date
from handlers.clientes import Clientes
from handlers.eliminaciones import RetirosEliminados, EliminacionRegistros
from handlers.rutas import RutaActual, RutaBD, RutaRegistros, RutaImportar 
from handlers.inventarios import Inventario
from helpers import mensajes, privilegios, constructor_paquete, VariablesCompartidas,formato_fecha
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
        ruta = request.form.get("nombreruta")
        fecha = formato_fecha(request.form.get("fecharuta"))
        with RutaActual() as ra:
            datos_guardados = ra.nueva_ruta(fecha=fecha,ruta=ruta)
        with RutaRegistros() as reg:
            reg.nueva_ruta(fecha=fecha,ruta=ruta)
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

def confpos(datos: map, columnas: list, columnas_inventario: list=None, confpos_accion: str="realizado") -> map:
    with Clientes() as cl:
        datos_cliente = {"cliente":None,"estado":"activo"}
        for dato in ["contrato","rut","cliente","direccion","comuna","telefono","otro"]:
            datos_cliente[dato] = dato[dato]["dato"]
        verif_ncliente = cl.nuevo_cliente(datos_cliente, datoeval="rut")
        if verif_ncliente:
            cimprime(titulo="Nuevo cliente a bd",agregado_a_bd=f"Cliente {datos_cliente['cliente']} agregado a BD")
        else:
            cimprime(titulo="Cliente en bd",agregado_a_bd=f"Cliente {datos_cliente['cliente']} ya en BD")
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
    # MODIFICAR EL STOCK
    if confpos_accion == "realizado":
        with Inventario() as inv:
            for columna in columnas_inventario:
                stock_descontado = datos[columna]["dato"]
                if stock_descontado:
                    stock_descontado = int(stock_descontado)
                    inv.modifica_stock(
                            columna=columna,
                            modificacion=-stock_descontado
                            )
        with RutaBD() as rbd:
            fecharuta = datos["fecharuta"]
            kgtotales = rbd.kgtotales(fecharuta)
            # Mensaje en confirmacion de usuario con resumen de insumos
            detalle_retiro = rbd.getDato(
                    fila=bd_ubicacion,
                    columna="detalleretiro"
                    )
            rbd.putDato(
                    dato=f"{detalle_retiro} INSUMOS:{rbd.resumen_insumos(filaCliente=bd_ubicacion)}",
                    fila=bd_ubicacion,
                    columna="detalleretiro"
                    )
            resumen_insumos_general = rbd.resumen_insumos(fecharuta)
        with RutaRegistros() as reg:
            ubicacion = reg.ubicacion_registro(datos)
            for columna, dato in kgtotales.items(): # Registrar los kilos que van hasta este momento
                reg.putDato(
                        dato=dato,
                        fila=ubicacion,
                        columna=columna
                        )
            # Registrar mensaje con resumen de insumos usados
            reg.putDato(
                    dato=resumen_insumos_general,
                    fila=ubicacion,
                    columna="insumos_usados"
                    )

def empaquetador_rutaactual(request: object) -> map:
    paquete = constructor_paquete(request,"rutas.html","RUTA EN CURSO")

    def datos_base():
        with RutaActual() as ractual:
            paquete["rutaLista"] = ractual.listar_rutaactual(
                    columnas=["id_ruta","rut","cliente","direccion","comuna","telefono","otro","id","contrato"],
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

    def form_confpos(confpos_accion: str):
        columnas = ["fecha","id_ruta","id","contrato","rut","cliente","direccion","comuna","telefono","otro"]
        columnas_inventario = params.INVENTARIOS["insumos_ruta"]
        columnas_retirokgs = params.RUTAS_BD["retirokgs"]
        bdrutas = False
        with Inventario() as inv:
            inventario_actual = inv.mapdatos(
                    columnas=columnas_inventario
                    )
        with RutaBD() as rbd:
            detallekgs = rbd.mapdatos(
                    columnas=columnas_retirokgs
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
                datos["detalleretiro"] = {"dato":request.form.get("detalleretiro")}
                if confpos_accion == "realizado":
                    for columna in columnas_inventario:
                        datos[columna] = {"dato":request.form.get(columna)}
                    for columna in columnas_retirokgs:
                        datos[columna] = {"dato":request.form.get(columna)}
                datos["status"] = {"dato":confpos_accion}
                confpos(datos,columnas,columnas_inventario,confpos_accion)
                ra.eliminar(ubicacion_cliente_ra)
            else:
                datos_cliente = ra.mapdatos(fila=int(ubicacion), columnas=columnas,idy=True)
                datos_cliente["detalleretiro"] = {"encabezado":"Detalle del retiro"}
                paquete[f"formulario_confpos_cliente"] = datos_cliente
                if confpos_accion == "realizado":
                    paquete[f"formulario_confpos_inventario"] = inventario_actual
                    paquete[f"formulario_confpos_kilos"] = detallekgs
                    paquete["botonconfpos"] = "CONFIRMAR CLIENTE"
                else:
                    paquete["botonconfpos"] = "POSPONER CLIENTE"
                paquete["confpos"] = confpos_accion
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

    elif "agrega_cliente_manual" in request.form:
        accion = request.form.get("agrega_cliente_manual")
        columnas=["contrato","rut","cliente","direccion","comuna","telefono","otro"]
        if accion == "to_form":
            with RutaActual() as ra:
                clte_manual = ra.mapdatos(columnas=columnas)
            for dato, tipo, requerido in [
                    ("contrato","number","required"),
                    ("rut","number","required"),
                    ("cliente","text","required"),
                    ("direccion","text","required"),
                    ("comuna","text","required"),
                    ("telefono","number","required"),
                    ("otro","text","")
                    ]:
                clte_manual[dato]["tipodato"] = tipo
                clte_manual[dato]["required"] = requerido
            paquete["pagina"] = "rutas_clienteman.html"
            paquete["clte_manual"] = clte_manual
        else:
            datos = {}
            for columna in columnas:
                datos[columna] = {"dato":request.form.get(columna)}
            with RutaActual() as ra:
                ra.agregar_a_ruta(datos)
        datos_base()

    elif "finalizaRutaActual" in request.form:
        clientes_posponer = []
        finalizar_ruta = False

        # Verificaciones previas
        with RutaActual() as ra:
            verificacion = ra.verifica_ruta_completa()
            cimprime(verificacion=verificacion,verif=True if verificacion else False)
            if verificacion >= 0:
                finalizar_ruta = True
                if verificacion > 0:
                    clientes = ra.listar(solodatos=True,columnas=["cliente"],idy=True)
                    for cliente in clientes:
                        datacliente = ra.mapdatos(fila=cliente[-1])
                        datacliente["detalleretiro"] = {"dato":"DEUDA"}
                        datacliente["status"] = {"dato":"pospuesto"}
                        clientes_posponer.append(datacliente)
            else:
                paquete["alerta"] = "Aun quedan clientes por confirmar o posponer antes de finalizar ruta"
            datos_ruta = ra.mapdatos(
                    fila=ra.hoja_actual["filadatos"],
                    columnas=["fecharuta","nombreruta"]
                    )

        # SECUENCIA DE FINALIZACION DE RUTA
        if finalizar_ruta:
            # Secuencia de CONFPOS
            if clientes_posponer != []:
                for data_cliente in clientes_posponer:
                    confpos(datos=data_cliente,confpos_accion="pospuesto")

            with RutaRegistros() as reg:
                ubicacion_registro = reg.ubicacion_registro(
                        datos={
                            "fecharuta":datos_ruta["fecharuta"]["dato"],
                            "nombreruta":datos_ruta["nombreruta"]["dato"]
                            })
                if ubicacion_registro:
                    reg.putDato(
                        dato="RUTA FINALIZADA",
                        fila=ubicacion_registro,
                        columna="otros"
                        )

            # Limpia de datos la hoja de ruta luego de terminar de trabajar en ella
            with RutaActual() as ractual:
                ractual.eliminarContenidos()
                for col in ["fecharuta","nombreruta"]:
                    ractual.putDato(
                            dato=None,
                            fila=ractual.hoja_actual["filadatos"],
                            columna=col
                            )
        datos_base()

    elif "cancelaRutaActual" in request.form:
        with RutaActual() as ra:
            datosruta = ra.mapdatos(
                    fila=ra.hoja_actual["filadatos"],
                    columnas=["fecharuta","nombreruta"]
                    )
            ra.eliminarContenidos()
            for col in ["fecharuta","nombreruta"]:
                ra.putDato(
                        dato=None,
                        fila=ra.hoja_actual["filadatos"],
                        columna=col
                        )
        with RutaRegistros() as reg:
            ubicacion_fecharuta = reg.buscadato(
                    dato=datosruta["fecharuta"]["dato"],
                    columna="fecharuta"
                    )
            reg.eliminar(ubicacion_fecharuta)
        datos_base()

    elif "reubicar" in request.form:
        with RutaActual() as ra:
            origen = int(request.form.get("uboriginal")) + (ra.hoja_actual["filainicial"] - 1)
            destino = int(request.form.get("ubdestino")) + (ra.hoja_actual["filainicial"] - 1)
            datosfila = ra.listar(filas=[origen],columnas=ra.hoja_actual["ncolumnas_todas"],solodatos=True)[0]
            ra.eliminar(origen)
            ra.insertar_fila(destino)
            columnas = ra.hoja_actual["ncolumnas_todas"]
            for dato in datosfila:
                ra.putDato(
                        dato=dato,
                        fila=destino,
                        columna=columnas[datosfila.index(dato)]
                        )
        datos_base()

    elif "cliente_ruta_realizado" in request.form:
        ubicacion = request.form.get("cliente_ruta_realizado")
        form_confpos(confpos_accion="realizado")
        datos_base()

    elif "cliente_ruta_pospuesto" in request.form:
        ubicacion = request.form.get("cliente_ruta_pospuesto")
        form_confpos(confpos_accion="pospuesto")
        datos_base()

    elif "cliente_ruta_eliminar" in request.form:
        ubicacion = int(request.form.get("cliente_ruta_eliminar"))
        with RutaActual() as ra:
            ra.eliminar(ubicacion)
        datos_base()

    elif "enCamino" in request.form:
        pass

    else:
        datos_base()

    return paquete

def empaquetador_registros_rutas(request: object) -> map:
    paquete = constructor_paquete(request,"rutas_registros.html","REGISTRO DE RUTAS")

    def datos_base():
        columnas = ["fecharuta","nombreruta"]
        with RutaRegistros() as rutaregistros:
            ruta_lista = rutaregistros.listar(columnas=columnas, solodatos=True, idy=True)
            ruta_lista.reverse()
            paquete["rutas_lista"] = ruta_lista

    def buscar_registros(ubicacion: int, solo_ubicaciones: bool=False) -> list:
        with RutaRegistros() as reg:
            nombreruta = reg.getDato(
                    fila=int(ubicacion),
                    columna="nombreruta"
                    )
            fecharuta = reg.getDato(
                    fila=int(ubicacion),
                    columna="fecharuta"
                    )
            datosruta = reg.listar(
                    filas=[int(ubicacion)],
                    columnas=["fecharuta","nombreruta","realizado","pospuesto"]
                    )
        with RutaBD() as rbd:
            ubicaciones = rbd.buscadato(
                    dato = fecharuta,
                    columna = "fecha",
                    exacto=True,
                    buscartodo = True
                    )
            if solo_ubicaciones:
                return ubicaciones
            else:
                total_confpos = rbd.total_clientes_confpos(fecharuta)
                paquete["rutaResultado"] = rbd.listar(filas=ubicaciones,idy=True) if ubicaciones else None
                if paquete["rutaResultado"]:
                    paquete["itemskg"] = rbd.kgtotales(fechainicio=fecharuta,fechafinal=fecharuta)
                else:
                    paquete["itemskg"] = rbd.kgtotales()
                paquete["insumos_usados"] = rbd.resumen_insumos(fecharuta,fecharuta,retorna_map=True)
        if not solo_ubicaciones:
            with RutaRegistros() as reg:
                # Obtener datos de la ruta y mostrarlos actualizando realizados y pospuestos
                col_list_reg = ["fecharuta","nombreruta","realizado","pospuesto"]
                datosruta = reg.listar(
                        filas=[int(ubicacion)],
                        columnas=col_list_reg
                        )
                col_realizado = col_list_reg.index("realizado")
                col_pospuesto = col_list_reg.index("pospuesto")
                datosruta["datos"][0][col_realizado] = 0 if not total_confpos else total_confpos["realizado"]
                datosruta["datos"][0][col_pospuesto] = 0 if not total_confpos else total_confpos["pospuesto"]
                if total_confpos:
                    for columna, dato in total_confpos.items():
                        reg.putDato(
                            dato=dato,
                            fila=int(ubicacion),
                            columna=columna
                            )
                
            paquete["datosruta"] = datosruta
            paquete["rutanombre"] = f"{fecharuta} - {nombreruta}"
            paquete["pagina"] = "rutas_registros_resultados.html"

    if "detalle_ruta_registro" in request.form:
        vc = VariablesCompartidas()
        ubicacion = request.form.get("rutas_registradas")
        vc.put_variable(reg_ult_busqueda=ubicacion)
        buscar_registros(ubicacion)

    elif "elimina_cliente_registro" in request.form:
        vc = VariablesCompartidas()
        ubicacion = request.form.get("elimina_cliente_registro")
        # Eliminar cliente en RutaBD
        with RutaBD() as rbd:
            status = rbd.get_status_retiro(ubicacion)
            rbd.eliminar(ubicacion)
        # Descontar de los clientes confirmado o pospuesto
        # with RutaRegistros() as reg:
        #     reg.cliente_confpos(int(ubicacion),status,-1)
        # Devolver pagina con registros actualizados al usuario
        if "reg_ult_busqueda" in vc.variables:
            buscar_registros(vc.get_variable("reg_ult_busqueda"))
        else:
            datos_base()

    elif "disposicion_final" in request.form:
        vc = VariablesCompartidas()
        ubicacion = request.form.get("disposicion_final")
        with RutaBD() as rbd:
            rbd.disposicion_final(int(ubicacion),"PRE-ELIMINACION")
        if "reg_ult_busqueda" in vc.variables:
            buscar_registros(vc.get_variable("reg_ult_busqueda"))
        else:
            datos_base()

    elif "eliminar_ruta" in request.form:
        ubicacion = request.form.get("rutas_registradas")
        ubicaciones = buscar_registros(ubicacion,solo_ubicaciones=True)
        if ubicaciones:
            with RutaBD() as rbd:
                for fila in ubicaciones:
                    rbd.eliminar(fila)
        with RutaRegistros() as reg:
            reg.eliminar(ubicacion)
        with RutaActual() as ra:
            if ra.ruta_existente():
                for campo in ["fecharuta","nombreruta"]:
                    ra.putDato(
                            fila=ra.hoja_actual["filadatos"],
                            dato=None,
                            columna=campo
                            )
                ra.eliminarContenidos()
        vc = VariablesCompartidas()
        if "reg_ult_busqueda" in vc.variables:
            vc.del_variable("reg_ult_busqueda")
        datos_base()

    elif "modifica_registro" in request.form:
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

