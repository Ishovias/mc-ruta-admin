__all__ = [
        'buscar_cliente', #{{{
        'sindatos',
        'get_cliente',
        'formulario_nuevo_cliente',
        'nuevo_cliente',
        'get_cl_enruta',
        'get_sumario',
        'cliente_a_ruta',
        'cliente_confpos',
        'cliente_manual',
        'movpos',
        'get_rutas',
        'get_ruta',
        'get_totales_ruta',
        'marcar_status',
        'rutas_buscar_dato',
        'rutabd_modregistro',
        'rutabd_obsdecoder',
        'inv_registra_mov',
        'inv_get_stock',
        'inv_mod_stock',
        'inv_suma_stock',
        'extrae_ruta',
        'importa_datos',
        'eliminar_ubicacion',
        'get_dato',
        'rendicion',
        'get_campos_formulario',
        'get_data',
        'get_totales',
        'get_fechas',
        'add_gasto'# }}}
        ]

from cimprime import cimprime
import handlers
import params
from utils import fecha_formato, formato_moneda
from pdfgen import PDFGen, Cord

CLASES_BD = {
        "clientes":handlers.Clientes,
        "rutabd":handlers.RutaBD,
        "inventario":handlers.Inventario,
        "rutaimportar":handlers.RutaImportar,
        "gastos":handlers.Gastos
        }

sindatos = {"sindatos":"No se encontraron datos coincidentes con esa busqueda"}

# FUNCIONES AUXILIARES UTILITARIAS
# {{{
def get_clase(clase: str) -> object:
    if clase not in CLASES_BD:
        raise ValueError(f"Clase solicitada '{clase}' inexistente")
    return CLASES_BD.get(clase)

def validador_int(valor: any) -> any:
    if type(valor) != int:
        try:
            valor = int(valor)
        except:
            raise ValueError("Error en conector, ubicacion dada no se puede convertir en int")
        else:
            return valor
    return valor
# }}}
# --------- CONECTORES CLIENTE ---------------
# {{{
def buscar_cliente(busqueda: str, filtro: str) -> dict:
    with handlers.Clientes() as cl:# {{{
        resultados = cl.busca_cliente(
            busqueda=busqueda,
            filtro=filtro
            )
        return resultados if resultados else sindatos# }}}

def get_cliente(idcliente: str) -> dict:
    with handlers.Clientes() as cl:# {{{
        return cl.get_cliente(idcliente,"id")# }}}

def formulario_nuevo_cliente(request: object) -> dict:
    if request.method == 'GET':# {{{
        with handlers.Clientes() as cl:
            campos = cl.mapdatos(
                    columnas=cl.hoja_actual["ncolumnas"]
                    )
            campos["id"]["dato"] = int(cl.get_id()) + 1
            del campos["estado"]
        return {"render":campos}
    elif request.method == 'POST':
        data = {}
        for campo in params.CLIENTES["ncolumnas"]:
            data[campo] = request.form.get(campo)
        data["estado"] = "activo"
        with handlers.Clientes() as cl:
            realizado = cl.nuevo_cliente(data)
            status = 201 if realizado else 400
        return {"realizado":realizado,"status":status}# }}}

def nuevo_cliente(datos: dict, datoeval: str, retornoid: bool) -> any:
    with handlers.Clientes() as cl:# {{{
        return cl.nuevo_cliente(datos,datoeval=datoeval,retornoid=retornoid)# }}}
# }}}
# --------- CONECTORES RUTAS -----------------
# {{{
def get_cl_enruta() -> dict:
    with handlers.RutaBD() as rbd:# {{{
        return rbd.clientes_enruta()# }}}

def get_sumario() -> dict:
    with handlers.RutaBD() as rbd:# {{{
        ra = rbd.get_nf_rutaactual()
        if ra:
            fecha = ra.get("fecha")
            datos = {
                    "enruta":rbd.sumario("enruta",fecha),
                    "postergados":rbd.sumario("POSPUESTO",fecha),
                    "realizados":rbd.sumario("REALIZADO",fecha)
                    }
        else:
            datos = {"sin datos":False}
    return datos#}}}

def cliente_a_ruta(request: object) -> int:
    statuscode = 200# {{{
    with handlers.Clientes() as cl:
        datos_cliente = cl.get_cliente(
                dato=request.args.get("idclte"),
                tipo="id"
                )
    with handlers.RutaBD() as rbd:
        fecha = request.args.get("fecha")
        nombreruta = request.args.get("nombreruta")
        if not rbd.obtener_nombre_ruta(fecha) and not nombreruta:
            statuscode =  400
        elif nombreruta:
            rbd.cliente_a_ruta(datos_cliente,fecha,nombreruta)
        else:
            rbd.cliente_a_ruta(datos_cliente,fecha)
    return statuscode# }}}

def cliente_confpos(ubicacion: str, observaciones: str, accion: str) -> dict:
    with handlers.RutaBD() as rbd:# {{{
        return rbd.cliente_confpos(
                ubicacion=ubicacion,
                observaciones=observaciones,
                accion=accion
                )# }}}

def cliente_manual(request: object) -> None:
    with handlers.RutaBD() as rbd:# {{{
        mapdatos = {}
        columnas = rbd.hoja_actual["rutaactual"].copy()
        for campo in columnas:
            if campo in request.form:
                mapdatos[campo] = {"dato":request.form.get(campo)}
        rbd.cliente_a_ruta(
                mapdatos=mapdatos,
                fecha=int(request.form.get("fecha"))
                )# }}}

def movpos(pos_a: int, pos_b: int) -> bool:
    with handlers.RutaBD() as r:# {{{
        return r.movpos(pos_a,pos_b)# }}}

def get_rutas() -> dict:
    with handlers.RutaBD() as rbd:# {{{
        return rbd.obtener_rutas()# }}}

def get_ruta(fecharuta: str) -> dict:
    with handlers.RutaBD() as r:# {{{
        return r.obtener_ruta(fecharuta)# }}}

def get_totales_ruta(fecharuta: str) -> dict:
    with handlers.RutaBD() as rbd:# {{{
        return rbd.obtener_totales_ruta(fecharuta)# }}}

def marcar_status(ubicacion: str, status: str) -> None:
    with handlers.RutaBD() as rbd:# {{{
        rbd.marcar_status(ubicacion,status)
        fecha = rbd.getDato(fila=int(ubicacion),columna="fecha")
        id_cliente = rbd.getDato(fila=int(ubicacion),columna="id")
    if status == "aruta":
        with handlers.Inventario() as inv:
            inv.reversa_stock(fecha, id_cliente)# }}}

def rutas_buscar_dato(busqueda: str, filtro: str) -> dict:
    with handlers.RutaBD() as rbd:# {{{
        return rbd.buscar_datos(
            busqueda=busqueda,
            filtro=filtro
            )# }}}

def rutabd_modregistro(request: object, idy: int) -> dict:
    if request.method == "GET":#{{{
        with handlers.RutaBD() as r:
            data = r.mapdatos(fila=int(idy),columnas=r.hoja_actual.get("rutabd_busquedas"), idy=True)
        return {"render":data}
    elif request.method == "PUT":
        datos = request.form.to_dict()
        with handlers.RutaBD() as rbd:
            try:
                for campo in datos.keys():
                    rbd.putDato(
                            fila=int(idy),
                            columna=campo,
                            dato=datos[campo]
                            )
            except Exception as e:
                cimprime(titulo="Error en servidor",error=e)
                return {"resultado":False}
            else:
                return {"resultado":True}# }}}

def rutabd_obsdecoder(obs: str) -> dict:
    with handlers.RutaBD() as rbd:# {{{
        data = rbd.obsdecoder(obs,solo_decodifica=True)
    return data
    # }}}

# }}}
# ------------ CONEXIONES INVENTARIO ----------
# {{{
def inv_registra_mov(data: dict) -> None:
    with handlers.Inventario() as inv:# {{{
        inv.registra_movimiento(data)# }}}

def inv_get_stock() -> dict:
    with handlers.Inventario() as inv:# {{{
        return inv.get_stock()# }}}

def inv_suma_stock(cantidad: any=None, columna: any=None, conjunto: dict=None, resta: bool=False) -> bool:
    try:# {{{
        with handlers.Inventario() as inv:
            if conjunto:
                for col in conjunto:
                    stock = int(inv.getDato(
                            fila=inv.hoja_actual.get("filaStockActual"),
                            columna=col
                            ))
                    cantidad = int(conjunto.get(col))
                    inv.modifica_stock(
                            cantidad=stock + cantidad if not resta else stock - cantidad,
                            columna=col
                            )
    except Exception as e:
        print("Error en conector/inv_suma_stock: ",e)
        return False
    else:
        return True
    # }}}

def inv_mod_stock(cantidad: any, columna: any) -> None:
    with handlers.Inventario() as inv:# {{{
        inv.modifica_stock(
            cantidad=cantidad,
            columna=columna
            )# }}}
# }}}
# ------------ CONEXIONES UPLOADRUTA ----------
# {{{
def extrae_ruta(archivo_cargado:str) -> dict:
    with handlers.RutaImportar(archivo_cargado) as ri:# {{{
        return ri.extrae_ruta()# }}}

def importa_datos(datos: dict) -> bool:
    with handlers.RutaBD() as rbd:# {{{
        return rbd.importar_ruta(datos)# }}}

# }}}
## =========== CONEXIONES GENERICAS ===========
# {{{
def eliminar_ubicacion(clase: str, ubicacion: int) -> bool:
    clase = get_clase(clase)
    ubicacion = validador_int(ubicacion)
    with clase() as cl:
        return cl.eliminar(ubicacion)

def get_dato(clase: str, fila: int, columna: str) -> bool:
    clase = get_clase(clase)
    fila = validador_int(fila)
    with clase() as cl:
        return cl.getDato(fila=fila,columna=columna)

def put_dato(clase: str, dato: str, fila: int, columna: str) -> bool:
    clase = get_clase(clase)
    fila = validador_int(fila)
    with clase() as cl:
        return cl.getDato(dato=dato,fila=fila,columna=columna)
# }}}
# ----------- CONECTORES GASTOS ---------------
# {{{
def rendicion(fecha: str, cerrar: str=False) -> None:
    # >>>>>>>>>>>>>>>>>Extraer datos {{{
    with handlers.Gastos() as g:
        if fecha == "vigente":
            fecha = None
        rendicion = g.rendir(fecha, cerrar=cerrar)
        if not cerrar:
            totales = g.get_totales(fecha)
            fechas = g.get_fechas(data=g.datos_buscados)
            fecha = ""
            for x in fechas:
                fecha += f"{x[1]}"
                if x != fechas[-1]:
                    fecha += ", "
        else:
            return rendicion
    # <<<<<<<<<<<<<<<  Crear pdf
    if not cerrar:
        with PDFGen() as pdfgen:
            # INSERCION DE PLANTILLA RENDICION
            pdfgen.add_plantilla("rendicion_template.jpg")
            # INSERCION DATOS PRINCIPALES
            pdfgen.inserta_texto(fecha, Cord.FECHA.value)
            pdfgen.inserta_texto(totales.get("abonos"), Cord.RECIBIDO.value)
            pdfgen.inserta_texto(totales.get("gastos"), Cord.TOTAL_GASTOS.value)
            pdfgen.inserta_texto(totales.get("diferencia"), Cord.DIFERENCIA.value)
            pdfgen.inserta_texto(totales.get("diferencia_anterior"), Cord.DINERO_RUTA_ANTERIOR.value)
            # ------ ITERACION DATOS -------
            filainicial = Cord.FILA_INICIAL.value
            factor_incremento = 0
            for fila in rendicion:
                incremento = Cord.FILA_INCREMENTO.value * factor_incremento
                fila_index = filainicial + incremento
                pdfgen.inserta_texto(fecha_formato(fila[0],"codigo","vista"),(Cord.FECHA_DATO.value,fila_index))
                pdfgen.inserta_texto(formato_moneda(fila[1]),(Cord.MONTO.value,fila_index))
                pdfgen.inserta_texto(fila[2],(Cord.OBSERVACION.value,fila_index))
                factor_incremento += 1# }}}

def get_campos_formulario() -> dict:
    with handlers.Gastos() as g:# {{{
        return {"campos":g.get_campos()}# }}}

def get_data(fecha: str=None) -> dict:
    with handlers.Gastos() as g:# {{{
        return g.get_data(fecha)# }}}

def get_totales(fecha: str=None) -> dict:
    with handlers.Gastos() as g:# {{{
        return g.get_totales(fecha)# }}}

def get_fechas() -> dict:
    with handlers.Gastos() as g:# {{{
        return g.get_fechas()# }}}

def add_gasto(datos_dict: dict) -> bool:
    with handlers.Gastos() as g:# {{{
        return g.add_gasto(datos_dict)# }}}
# }}}
