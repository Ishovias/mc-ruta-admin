from werkzeug.utils import secure_filename
from datetime import datetime
from handlers.clientes import Clientes
from handlers.rutas import RutaActual, RutaBD, RutaRegistros, RutaImportar
from helpers import mensajes, privilegios, priv
import params
import os


def empaquetador_rutaactual(request: object) -> map:
    
    def verifica_cliente(datos_cliente_confirmado: list) -> bool:
        with Clientes() as cverif:
            nombrecliente = datos_cliente_confirmado[3]
            filacliente = cverif.verifica_existencia(nombrecliente, "cliente")
            if not filacliente:  # Procedimiento puntual si es que no es encontrado cliente en BD
                cverif.nuevo_cliente(
                    estado = "activo",
                    rut = datos_cliente_confirmado[2],
                    cliente = datos_cliente_confirmado[3],
                    direccion = datos_cliente_confirmado[4],
                    comuna = datos_cliente_confirmado[5],
                    telefono = datos_cliente_confirmado[6],
                    gps = datos_cliente_confirmado[7],
                    otro = datos_cliente_confirmado[8],
                    diascontrato = 60 # Lapso por defecto
                )
                return False
            elif not cverif.getDato(fila=filacliente, columna="diascontrato"):
                cverif.putDato(
                    dato=60,
                    fila=filacliente,
                    columna="diascontrato"
                    )
                return False
            else:
                return True
    
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
        fecharetiro = datos_cliente_confirmado[0]
        rutcliente = datos_cliente_confirmado[2]
        nombrecliente = datos_cliente_confirmado[3]
        # isoformateo de fecha para registro y calculo de sgte fecha
        compfecha = list(str(fecharetiro))
        compfecha.insert(4,"-")
        compfecha.insert(7,"-")
        fecharetiro = "".join(compfecha)

        if realizadopospuesto == "REALIZADO":
            verifica_cliente(datos_cliente_confirmado)
            with Clientes() as curetiro:
                filacliente = curetiro.verifica_existencia(
                    nombrecliente,
                    "cliente",
                    retornafila=True
                    )
                proxfecharetiro = curetiro.proximo_retiro(
                            rut=rutcliente,
                            fecharetiro=fecharetiro
                            )
                ingresoclientes = curetiro.putDato(
                    dato=fecharetiro,
                    fila=filacliente,
                    columna="ultimoretiro"
                    )
                if proxfecharetiro:
                    proxfecha = curetiro.putDato(
                        dato=proxfecharetiro,
                        fila=filacliente,
                        columna="proxretiro"
                        )
                else:
                    proxfecha = False
        else:
            verifica_cliente(datos_cliente_confirmado)
            proxfecha = True
            ingresoclientes = True

        if ingresobd and ingresoclientes and proxfecha:
            paquete["alerta"] = mensaje_ok
        else:
            paquete["alerta"] = f"{mensaje_bad}, ingresobd:{ingresobd}, ingresoclientes:{ingresoclientes}, proxfecha{proxfecha}"

        return paquete

    paquete = {"pagina":"rutas.html","aut":request.args.get("aut"), "nombrePagina":"RUTA EN CURSO"}
    privilegio = privilegios(request, paquete, retornaUser=True)
    paquete = privilegio["paquete"]
    usuario = privilegio["usuario"]
    paquete["usuario"] = usuario

    if "iniciaruta" in request.form and priv[usuario]["inirutaEnabled"] == "enabled":
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

    elif "finalizaRutaActual" in request.form and priv[usuario]["finEnabled"] == "enabled":
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
    
    elif "reubicar" in request.form and priv[usuario]["reubicarEnabled"] == "enabled":
        posicion_origen = request.form.get("uboriginal")
        posicion_destino = request.form.get("ubdestino")
        with RutaActual() as ra:
            datos_origen = ra.getDato(fila=posicion_origen, columna="todas")
            ra.eliminar(posicion_origen)
            ra.insertarfila(posicion_destino)
            if not ra.putDato(datos=datos_origen, fila=posicion_destino, columna="fecha"):
                paquete["alerta"] = "Error, no se pudo reubicar"
    
    elif "cliente_ruta_confirmar" in request.form and priv[usuario]["cpEnabled"] == "enabled":
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
            paquete["clienteidx"] = confirmacion
            with RutaActual() as rutaactual:
                paquete["clientenombre"] = rutaactual.getDato(
                        fila=confirmacion,
                        columnas=[
                            params.RUTA_ACTUAL["columnas"]["rut"],
                            params.RUTA_ACTUAL["columnas"]["cliente"],
                        ])

    elif "cliente_ruta_posponer" in request.form and priv[usuario]["cpEnabled"] == "enabled":
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
        columnasMostrar = [
            params.RUTA_ACTUAL["columnas"]["id"],
            params.RUTA_ACTUAL["columnas"]["rut"],
            params.RUTA_ACTUAL["columnas"]["cliente"],
            params.RUTA_ACTUAL["columnas"]["direccion"],
            params.RUTA_ACTUAL["columnas"]["comuna"],
            params.RUTA_ACTUAL["columnas"]["telefono"],
            params.RUTA_ACTUAL["columnas"]["otro"],
            params.RUTA_ACTUAL["columnas"]["contrato"],
            params.RUTA_ACTUAL["columnas"]["ultimoretiro"]
            ]
        rutaDatos = ractualbd.listar(columnas=columnasMostrar, retornostr=True)
        indice = 1
        rutaDatos["encabezados"].insert(0,"Idx")
        for fila in rutaDatos["datos"]:
            fila.insert(0,indice)
            indice += 1
        if rutaActiva:
            paquete["ruta"] = rutaActiva
        else:
            paquete["ruta"] = None
        paquete["rutaLista"] = rutaDatos
    
    return paquete
    
def empaquetador_registros_rutas(request: object) -> map:
    paquete = {"pagina":"rutasRegistros.html","aut":request.args.get("aut")}
    privilegio = privilegios(request, paquete, retornaUser=True)
    paquete = privilegio["paquete"]
    usuario = privilegio["usuario"]
    paquete["usuario"] = usuario

    if "detalle_ruta_registro" in request.form:
        fecha = request.form.get("detalle_ruta_registro")
        paquete["fecha"] = fecha
        
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
        paquete["rutaLista"] = rutaregistros.listar(retornostr=True)

    return paquete

def empaquetador_carga_ruta(request: object, app: object) -> map:
    
    def fichero_permitido(archivo: str) -> bool:
        return "." in archivo and archivo.rsplit(".",1)[1].lower() in params.EXTENSIONES_PERMITDAS
    
    paquete = {"pagina":"cargaruta.html","aut":request.args.get("aut"), "nombrePagina":"CARGA DE RUTA POR XLSX"}
    privilegio = privilegios(request, paquete, retornaUser=True)
    paquete = privilegio["paquete"]
    usuario = privilegio["usuario"]
    paquete["usuario"] = usuario
    
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