from werkzeug.utils import secure_filename
from flask import request
from datetime import datetime, date
from handlers.clientes import Clientes
from handlers.eliminaciones import RetirosEliminados, EliminacionRegistros
from handlers.rutas import RutaActual, RutaBD, RutaRegistros, RutaImportar, cimprime
from handlers.inventarios import Inventario
from helpers import mensajes, privilegios, constructor_paquete
from cimprime import cimprime as cimp
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

def confpos(datos: map, confpos: str="realizado") -> map:
    datosruta = ["fecha","nombreruta","realizado","pospuesto"]
    with RutaBD() as rbd:
        ubicacion = rbd.buscafila()
        for dato in datos.keys():
            if dato not in datosruta:
                rbd.putDato(
                        fila=ubicacion,
                        dato=datos[dato],
                        columna=dato
                        )
            rbd.putDato(
                dato=confpos,
                fila=rbd.hoja_actual["filadatos"],
                columna=confpos
                )
    if confpos == "realizado":
        with Inventario() as inv:
            for col in inv.hoja_actual["insumos_ruta"]:
                inv.modificaStock(
                        elemento=col,
                        modificacion=int(f"-{datos[col]}")
                        )

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
        with Inventario() as inv:
            inventario_actual = inv.mapdatos(
                    columnas=params.INVENTARIOS["insumos_ruta"]
                    )
        with RutaActual() as ra:
            if ubicacion == "formulario_respuesta":
                for columna in params.INVENTARIOS["insumos_ruta"]:
                    datos[columna] = request.form.get(columna)
                confpos(datos=datos, confpos=confpos)
            else:
                columnas = ["fecha","id_ruta","id","contrato","rut","cliente","direccion","comuna","telefono","otro"]
                datos = ra.mapdatos(fila=int(ubicacion), columnas=columnas)
                if confpos == "realizado":
                    for clave, valor in inventario_actual.items():
                        datos[clave] = valor 
                datos["detalleretiro"] = {"encabezado":"Detalle del retiro"}
                paquete[f"formulario_confpos"] = datos
                if confpos == "realizado":
                    botonconfpos = "REALIZADO"
                else:
                    botonconfpos = "POSPONER"
                paquete["botonconfpos"] = botonconfpos
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
    paquete = {"pagina":"rutasRegistros.html","aut":request.args.get("aut")}
    privilegio = privilegios(request, paquete, retornaUser=True)
    paquete = privilegio["paquete"]
    usuario = privilegio["usuario"]
    paquete["usuario"] = usuario

    if "detalle_ruta_registro" in request.form:
        fecha = request.form.get("detalle_ruta_registro")
        data: list = []
        
        with RutaBD() as rutabd:
            encabezados = params.RUTAS_BD["encabezados_nombre"].copy()
            encabezados.remove(encabezados[0])
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
                recopilado.append(f)
                data.append(recopilado)

            insumos_usados = rutabd.cuenta_insumos(
                insumos=seleccionar_conjunto_elementos(
                    hoja=rutabd.hoja_actual,
                    nombreDesde="cajaroja_0.5",
                    nombreHasta="frascoamalgama"
                ),
                ubicaciones=filasEncontradas
            )

            paquete["encabezados"] = encabezados
            paquete["itemskg"] = rutabd.kgtotales(fecha,fecha)
            paquete["fecha"] = fecha
            paquete["rutaResultado"] = data
            paquete["insumos_usados"] = insumos_usados
            
        cimprime(insumos_usados=insumos_usados,itemskg=paquete["itemskg"])

    elif "agrega_eliminacion" in request.form:
        with RutaBD() as rbd:     
            ubicacionCliente = int(request.form.get("agrega_eliminacion"))
            estadoRetiro = rbd.getDato(
                fila=ubicacionCliente,
                columna="otro"
            )
            if "ELIMINADO" not in estadoRetiro:
                rbd.putDato(
                    fila=int(ubicacionCliente),
                    dato="FASE_ELIMINACION",
                    columna="otro"
                    )
            else:
                paquete["alerta"] = "Retiro ya eliminado en disposicion final"
    
    elif "lista_eliminacion" in request.form:
        encabezados = params.RUTAS_BD["encabezados_nombre"].copy()
        encabezados.remove(encabezados[0])
        
        with RutaBD() as rbd:
            filashalladas = rbd.buscadato(
                filainicio=rbd.hoja_actual["filainicial"], 
                columna=rbd.hoja_actual["columnas"]["otro"], 
                dato="FASE_ELIMINACION", 
                exacto=True, 
                buscartodo=True
                )
            data = []
            rbd.eliminaKilosRegistrados()
            for fila in filashalladas:
                recopilado = rbd.extraefila(
                    fila=fila,
                        columnas=params.RUTAS_BD["columnas"]["todas"]
                        )
                data.append(recopilado)
                rbd.kgtotales(filaCliente=fila)
            totalKilos = rbd.getKilos()
            paquete["itemskg"] = totalKilos.copy()

        paquete["encabezados"] = encabezados
        paquete["fecha"] = "Objetos en fase de eliminacion"
        paquete["rutaResultado"] = data

    elif "eliminar_desechos" in request.form:
        with RutaBD() as rbd:
            fechaEliminacion = date.isoformat(date.today())
            fechaEliminacion = fechaEliminacion.replace("-","")
            listaFilas = rbd.buscadato(
            filainicio=rbd.hoja_actual["filainicial"], 
            columna=rbd.hoja_actual["columnas"]["otro"], 
            dato="FASE_ELIMINACION", 
            buscartodo=True
            )
            fechasEliminadas = []
            for fila in listaFilas:
                fechasEliminadas.append(rbd.getDato(fila=fila, columna="fecha"))
            kilos = rbd.recuentoKgEliminar()
        with EliminacionRegistros() as rege:
            mensajeRegistro = rege.obtener_fechas_eliminadas(fechasEliminadas=fechasEliminadas)
            datosRegistro = {
                "fechaeliminacion":fechaEliminacion,
                "observacion":mensajeRegistro,
            }
            for elemento, valor in kilos.items():
                datosRegistro[elemento] = valor
            rege.registra_eliminacion(datosRegistro)
        with RutaBD() as rbd:    
            clientesEliminados = []
            for fila in listaFilas:
                rbd.putDato(
                    dato=f"ELIMINADO-{fechaEliminacion}",
                    fila=fila,
                    columna="otro"
                    )
                clientesEliminados.append(rbd.getDato(fila=fila,columnas=rbd.hoja_actual["columnas"]["todas"]))

        with RetirosEliminados() as relim:
            fila = relim.busca_ubicacion(columna="fecha")
            for eliminado in clientesEliminados:
                relim.putDato(
                    datos=eliminado, 
                    fila=fila, 
                    columna="fecha"
                    )
                fila += 1

    elif "cancelar_eliminacion" in request.form:
        with RutaBD() as rbd:
            for f in range(rbd.hoja_actual["filainicial"],rbd.getmaxfilas(),1):
                celda = rbd.getDato(fila=f,columna="otro")
                if not celda:
                    continue
                if "FASE_ELIMINACION" in celda:
                    celda = celda.replace("FASE_ELIMINACION", "")
                    rbd.putDato(
                        dato=celda,
                        fila=f,
                        columna="otro"
                        )

    elif "eliminar_ruta" in request.form:
        with RutaBD() as rbd:
            fechaRuta = request.form.get("eliminar_ruta")
            ubicaciones = rbd.buscadato(
                filainicio = rbd.hoja_actual["filainicial"], 
                columna=rbd.hoja_actual["columnas"]["fecha"], 
                dato=fechaRuta,
                buscartodo=True
                )
            for fila in ubicaciones:
                rbd.putDato(
                    fila=fila,
                    dato="FASE_ELIMINACION",
                    columna="otro"
                )

    with RutaRegistros() as rutaregistros:
        paquete["rutaLista"] = rutaregistros.listar(retornostr=True)

    cimp(paquete_rutaactual=paquete)
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

