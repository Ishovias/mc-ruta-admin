# hoja de parametros generales
IMPRESION_LOGS = False

# Privilegios usuarios
PRIVILEGIOS = {
     "admin":{
         "usuarios":["iberoiza"],
         "privilegios":{
             "btnClientes":{"pagina":"clientes.html","js":"clientes.js"},
             "btnRutaActual":{"pagina":"rutas_rutaactual.html","js":"rutaactual.js"},
             "btnRutas":{"pagina":"rutas_bd.html","js":"rutabd.js"},
             "btnRutaImportar":{"pagina":"uploadruta.html","js":"uploadruta.js"},
             "btnInventario":{"pagina":"inventario.html","js":"inventario.js"},
             "btnInventarioMod":{"pagina":"inventario_mod.html","js":"inventario_mod.js"}
             }
         },
     "user":{
         "usuarios":["mjose"],
         "privilegios":{
             "btnClientes":{"pagina":"clientes.html","js":"clientes.js"},
             "btnRutaActual":{"pagina":"rutas_rutaactual.html","js":"rutaactual.js"},
             "btnRutas":{"pagina":"rutas_bd.html","js":"rutabd.js"},
             "btnRutaImportar":{"pagina":"uploadruta.html","js":"uploadruta.js"},
             "btnInventario":{"pagina":"inventario.html","js":"inventario.js"}
             }
         },
     "spectator":{
         "usuarios":["invitado"],
         "privilegios":{
             "btnRutaActual":{"pagina":"rutas_rutaactual.html","js":"rutaactual_spectator.js"},
             "btnInventario":{"pagina":"inventario.html","js":"inventario.js"},
             "btnRutas":{"pagina":"rutas_bd.html","js":"rutabd_spectator.js"}
             }
         }
}

# ---------- RUTAS DE DESARROLLO --------------
LIBRODATOS = "./bd/mediclean_bd.xlsx"
LIBROTODO = "./bd/todo_bd.xlsx"
LIBRORUTA = "./bd/ruta.xlsx"
RUTA_IMPORTACION = "./ruta_import"

# ---------- RUTAS DE PRODUCCION --------------
#LIBRODATOS = "/home/iberoiza/mediclean/bd/mediclean_bd.xlsx"
#LIBROTODO = "/home/iberoiza/mediclean/bd/todo_bd.xlsx"
#LIBRORUTA= "/home/iberoiza/mediclean/bd/ruta.xlsx"
#RUTA_IMPORTACION = "/home/iberoiza/mediclean/ruta_import"
# UPLOAD_FOLDER = "/home/iberoiza/mediclean/ruta_import"

EXTENSIONES_PERMITDAS = {"xlsx", "xls"}
MAX_FILAS = 10000
FORMATO_FECHA = "%Y-%m-%d"
FORMATO_FECHA_CODIGO = "%Y%m%d"

CLIENTES = {
     "nombrehoja": "clientes",
     "filainicial": 2,
     "columnas": {
          "id": {"num": 1, "encabezado": "ID"},
          "estado": {"num": 2, "encabezado": "ESTADO"},
          "contrato": {"num": 3, "encabezado": "CONTRATO"},
          "rut": {"num": 4, "encabezado": "RUT"},
          "cliente": {"num": 5, "encabezado": "CLIENTE"},
          "direccion": {"num": 6, "encabezado": "DIRECCION"},
          "comuna": {"num": 7, "encabezado": "COMUNA"},
          "telefono": {"num": 8, "encabezado": "TELEFONO"},
          "otro": {"num": 9, "encabezado": "OTRO"},
          "ultimoretiro": {"num": 10, "encabezado": "ULT.RETIRO"},
          "proxretiro": {"num": 11, "encabezado": "PROX.RETIRO"}
     },
     "columnas_todas": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
     "ncolumnas":["id","estado","contrato","rut","cliente","direccion","comuna","telefono","otro"],
     "encabezados": 1
}

USUARIO = {
     "nombrehoja": "usuarios",
     "filainicial": 2,
     "columnas": {
          "usuario": {"num": 1, "encabezado": "USUARIO"},
          "contrasena": {"num": 2, "encabezado": "CLAVE"},
          "token": {"num": 3, "encabezado": "TOKEN"}
     },
     "columnas_todas": [1, 2, 3],
     "encabezados": 1
}

RUTA_ACTUAL = {
     "nombrehoja": "ruta_actual",
     "filainicial": 3,
     "filadatos": 1,
     "columnas": {
          "fecha": {"num": 1, "encabezado": "FECHA"},
          "id_ruta": {"num": 2, "encabezado": "ID"},
          "contrato": {"num": 3, "encabezado": "CONTRATO"},
          "rut": {"num": 4, "encabezado": "RUT"},
          "cliente": {"num": 5, "encabezado": "CLIENTE"},
          "direccion": {"num": 6, "encabezado": "DIRECCION"},
          "comuna": {"num": 7, "encabezado": "COMUNA"},
          "telefono": {"num": 8, "encabezado": "TELEFONO"},
          "otro": {"num": 9, "encabezado": "OTRO"},
          "id": {"num": 10, "encabezado": "ID CLIENTE"},
          # Columnas de datos de la ruta
          "fecharuta": {"num": 2, "encabezado": "FECHA"},
          "nombreruta": {"num": 3, "encabezado": "RUTA"},
          "realizado": {"num": 4, "encabezado": "REALIZADOS"},
          "pospuesto": {"num": 5, "encabezado": "POSPUESTOS"},
     },
     "columnas_todas": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
     "columnas_datos": [2,3,4,5],
     "ncolumnas_datos":["fecharuta","nombreruta"],
     "ncolumnas_todas": ["fecha","id_ruta","contrato","rut","cliente","direccion","comuna","telefono","otro","id"],
     "encabezados": 2
}

RUTAS_BD = {
     "nombrehoja": "rutas_bd",
     "filainicial": 2,
     "columnas": {
          "fecha": {"num": 1, "encabezado": "FECHA"},
          "id_ruta": {"num": 2, "encabezado": "ID"},
          "contrato": {"num": 3, "encabezado": "CONT"},
          "rut": {"num": 4, "encabezado": "RUT"},
          "cliente": {"num": 5, "encabezado": "CLIENTE"},
          "direccion": {"num": 6, "encabezado": "DIRECCION"},
          "comuna": {"num": 7, "encabezado": "COMUNA"},
          "telefono": {"num": 8, "encabezado": "TELEFONO"},
          "otro": {"num": 9, "encabezado": "OTRO"},
          "id": {"num": 10, "encabezado": "ID CLIENTE"},
          "status": {"num": 11, "encabezado": "STATUS"},
          "detalleretiro": {"num": 12, "encabezado": "DETALLE"},
          "farmaco": {"num": 13, "encabezado": "FARMACO"},
          "patologico": {"num": 14, "encabezado": "PATOLOGICO"},
          "contaminado": {"num": 15, "encabezado": "CONTAMINADO"},
          "cortopunzante": {"num": 16, "encabezado": "CORTOPUNZANTE"},
          "otropeligroso": {"num": 17, "encabezado": "OTRO PELIGROSO"},
          "liquidorx": {"num": 18, "encabezado": "LIQUIDOS RX"},
          "cajaroja_0.5": {"num": 19, "encabezado": "CAJA ROJA 0.5 lts"},
          "cajaroja_1": {"num": 20, "encabezado": "CAJA ROJA 1 lt"},
          "cajaroja_1.3": {"num": 21, "encabezado": "CAJA ROJA 1.3 lts"},
          "cajaroja_1.65": {"num": 22, "encabezado": "CAJA ROJA 1.65 lts"},
          "cajaroja_3": {"num": 23, "encabezado": "CAJA ROJA 3 lts"},
          "cajaroja_5": {"num": 24, "encabezado": "CAJA ROJA 5 lts"},
          "cajaamarilla_1": {"num": 25, "encabezado": "CAJA AMARILLA 1 lt"},
          "cajaamarilla_3": {"num": 26, "encabezado": "CAJA AMARILLA 3 lts"},
          "cajaamarilla_5": {"num": 27, "encabezado": "CAJA AMARILLA 5 lts"},
          "cajaamarilla_15": {"num": 28, "encabezado": "CAJA AMARILLA 15 lts"},
          "basureroamarillo_120": {"num": 29, "encabezado": "CONTENEDOR AMARILLO 120 lts"},
          "bolsaroja": {"num": 30, "encabezado": "BOLSA ROJA"},
          "bolsaroja_farmaco": {"num": 31, "encabezado": "BOLSA ROJA FARAMCO"},
          "bolsaamarilla": {"num": 32, "encabezado": "BOLSA AMARILLA"},
          "bidon_5": {"num": 33, "encabezado": "BIDON 5 lts"},
          "frascoamalgama": {"num": 34, "encabezado": "FRASCO AMALGAMAS"},
          "ruta":{"num":35,"encabezado":"RUTA"}
     },
     "rutaactual":["fecha","id_ruta","contrato","rut","cliente","direccion","comuna","telefono","otro","id"],
     "rutabd_busquedas":["fecha","id_ruta","contrato","rut","cliente","direccion","comuna","telefono","otro","id","detalleretiro","status"],
     "kgcols":["farmaco","patologico","contaminado","cortopunzante","otropeligroso","liquidorx"],
     "itemscols":["cajaroja_0.5","cajaroja_1","cajaroja_1.3","cajaroja_1.65","cajaroja_3","cajaroja_5","cajaamarilla_1","cajaamarilla_3","cajaamarilla_5","cajaamarilla_15","basureroamarillo_120","bolsaroja","bolsaroja_farmaco","bolsaamarilla","bidon_5","frascoamalgama"],
     "columnas_todas": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33],
     "retirokgs":["farmaco","patologico","contaminado","cortopunzante","otropeligroso","liquidorx"],
     "encabezados": 1,
     "obsdecoder":{
          "far":{"columna":"farmaco", "nombre": "FARMACO"},
          "pat":{"columna":"patologico", "nombre": "PATOLOGICO"},
          "con":{"columna":"contaminado", "nombre": "CONTAMINADO"},
          "cor":{"columna":"cortopunzante", "nombre": "CORTOPUNZANTE"},
          "pel":{"columna":"otropeligroso", "nombre": "OTRO PELIGROSO"},
          "rx":{"columna":"liquidorx", "nombre": "LIQUIDOS RX"},
          "cr0.5l":{"columna":"cajaroja_0.5", "nombre": "CAJA ROJA 0.5 lts"},
          "cr1l":{"columna":"cajaroja_1", "nombre": "CAJA ROJA 1 lt"},
          "cr1.3l":{"columna":"cajaroja_1.3", "nombre": "CAJA ROJA 1.3 lts"},
          "cr1.65l":{"columna":"cajaroja_1.65", "nombre": "CAJA ROJA 1.65 lts"},
          "cr3l":{"columna":"cajaroja_3", "nombre": "CAJA ROJA 3 lts"},
          "cr5l":{"columna":"cajaroja_5", "nombre": "CAJA ROJA 5 lts"},
          "ca1l":{"columna":"cajaamarilla_1", "nombre": "CAJA AMARILLA 1 lt"},
          "ca3l":{"columna":"cajaamarilla_3", "nombre": "CAJA AMARILLA 3 lts"},
          "ca5l":{"columna":"cajaamarilla_5", "nombre": "CAJA AMARILLA 5 lts"},
          "ca15l":{"columna":"cajaamarilla_15", "nombre": "CAJA AMARILLA 15 lts"},
          "basam":{"columna":"basureroamarillo_120", "nombre": "CONTENEDOR AMARILLO 120 lts"},
          "br":{"columna":"bolsaroja", "nombre": "BOLSA ROJA"},
          "brfar":{"columna":"bolsaroja_farmaco", "nombre": "BOLSA ROJA FARAMCO"},
          "ba":{"columna":"bolsaamarilla", "nombre": "BOLSA AMARILLA"},
          "bid":{"columna":"bidon_5", "nombre": "BIDON 5 lts"},
          "fram":{"columna":"frascoamalgama", "nombre": "FRASCO AMALGAMAS"}
         }
}

RUTAS_REGISTROS = {
    "nombrehoja": "rutas_registros",
    "filainicial": 2,
    "columnas": {
        "fecharuta": {"num": 1, "encabezado": "FECHA"},
        "nombreruta": {"num": 2, "encabezado": "RUTA"},
        "realizado": {"num": 3, "encabezado": "REALIZADOS"},
        "pospuesto": {"num": 4, "encabezado": "POSPUESTOS"},
        "otros": {"num": 5, "encabezado": "OTRO"},
        "farmaco": {"num": 6, "encabezado": "FARMACO"},
        "patologico": {"num": 7, "encabezado": "PATOLOGICO"},
        "contaminado": {"num": 8, "encabezado": "CONTAMINADO"},
        "cortopunzante": {"num": 9, "encabezado": "CORTOPUNZANTE"},
        "otropeligroso": {"num": 10, "encabezado": "OTRO PELIGROSO"},
        "liquidorx": {"num": 11, "encabezado": "LIQUIDO RX"},
        "insumos_usados": {"num": 12, "encabezado": "RESUMEN INSUMOS"}
        },
    "columnas_todas": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "encabezados": 1
    }

GASTOS_BD = {
     "nombrehoja": "gastos_bd",
     "filainicial": 2,
     "columnas": {
          "fecha": 1,
          "monto": 2,
          "descripcion": 3,
          "todas": [1, 2, 3]
     },
     "encabezados": 1
}

INVENTARIOS = {
     "nombrehoja": "inventarios",
     "filaStockActual": 2,
     "filainicial": 4,
     "columnas": {
          "fecha": {"num": 1, "encabezado": "FECHA"},
          "id":{"num": 2, "encabezado": "ID"},
          "cajaroja_0.5": {"num": 3, "encabezado": "CAJA ROJA 0.5 LTS (X UNIDAD)"},
          "cajaroja_1": {"num": 4, "encabezado": "CAJA ROJA 1 LTS (X UNIDAD)"},
          "cajaroja_1.3": {"num": 5, "encabezado": "CAJA ROJA 1.3 LTS (X UNIDAD)"},
          "cajaroja_1.65": {"num": 6, "encabezado": "CAJA ROJA 1.65 LTS (X UNIDAD)"},
          "cajaroja_3": {"num": 7, "encabezado": "CAJA ROJA 3 LTS (X UNIDAD)"},
          "cajaroja_5": {"num": 8, "encabezado": "CAJA ROJA 5 LTS (X UNIDAD)"},
          "cajaamarilla_1": {"num": 9, "encabezado": "CAJA AMARILLA 1 LTS (X UNIDAD)"},
          "cajaamarilla_3": {"num": 10, "encabezado": "CAJA AMARILLA 3 LTS (X UNIDAD)"},
          "cajaamarilla_5": {"num": 11, "encabezado": "CAJA AMARILLA 5 LTS (X UNIDAD)"},
          "cajaamarilla_15": {"num": 12, "encabezado": "CAJA AMARILLA 15 LTS (X UNIDAD)"},
          "basureroamarillo_120": {"num": 13, "encabezado": "BASURERO AMARILLO 120 LTS"},
          "bolsaroja": {"num": 14, "encabezado": "BOLSA ROJA (X UNIDAD)"},
          "bolsaroja_farmaco": {"num": 15, "encabezado": "BOLSA ROJA FARMACO (X UNIDAD)"},
          "bolsaamarilla": {"num": 16, "encabezado": "BOLSA AMARILLA (X UNIDAD)"},
          "bidon_5": {"num": 17, "encabezado": "BIDON 5 LTS"},
          "frascoamalgama": {"num": 18, "encabezado": "FRASCO AMALGAMAS"},
          "guias": {"num": 19, "encabezado": "GUIAS"},
          "amarras_paquete": {"num": 20, "encabezado": "AMARRAS PAQUETE"},
          "mascarillas": {"num": 21, "encabezado": "MASCARILLAS"},
          "guantes": {"num": 22, "encabezado": "GUANTES"},
          "alcoholgel": {"num": 23, "encabezado": "ALCOHOL GEL"}
     },
     "columnas_todas": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
     "encabezados": 1,
     "columnas_ruta":[
         "cajaroja_0.5",
         "cajaroja_1",
         "cajaroja_1.3",
         "cajaroja_1.65",
         "cajaroja_3",
         "cajaroja_5"
         "cajaamarilla_1",
         "cajaamarilla_3",
         "cajaamarilla_5",
         "cajaamarilla_15",
         "basureroamarillo_120",
         "bolsaroja",
         "bolsaroja_farmaco",
         "bolsaamarilla",
         "bidon_5",
         "frascoamalgama"
         ]
}

RETIROS_ELIMINADOS = {
     "nombrehoja": "retiros_eliminados",
     "encabezados": 1,
     "filainicial": 2,
     "columnas": {
          "fecha": 1,
          "id": 2,
          "rut": 3,
          "cliente": 4,
          "direccion": 5,
          "comuna": 6,
          "telefono": 7,
          "contrato": 8,
          "otro": 9,
          "ultimoretiro": 10,
          "status": 11,
          "detalleretiro": 12,
          "farmaco": 13,
          "patologico": 14,
          "contaminado": 15,
          "cortopunzante": 16,
          "otropeligroso": 17,
          "liquidorx": 18,
          "todas": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
     }
}

REGISTRO_ELIMINACIONES = {
     "nombrehoja": "registro_eliminaciones",
     "encabezados": 1,
     "filainicial": 2,
     "columnas": {
          "fechaeliminacion": 1,
          "observacion": 2,
          "farmaco": 3,
          "patologico": 4,
          "contaminado": 5,
          "cortopunzante": 6,
          "otropeligroso": 7,
          "liquidorx": 8,
          "todas": [1, 2, 3, 4, 5, 6, 7, 8]
     }
}

# ----------- APP SUBLITOTE --------------

TODO = {
     "nombrehoja": "todo_list",
     "filainicial": 2,
     "columnas": {
          "fecha": 1,
          "descripcion": 2,
          "completado": 3,
          "fechacompletado": 4,
          "todas": [1, 2, 3, 4]
     },
     "encabezados": 1
}

ST_PRODUCTOS = {
     "nombrehoja": "st_productos",
     "filainicial": 3,
     "columnas": {
          "codigo": 1,
          "producto": 2,
          "preciocosto": 3,
          "precioventa": 4,
          "existencias": 5,
          "observaciones": 6,
          "todas": [1, 2, 3, 4, 5, 6]
     },
     "encabezados": 2
}

ST_COTIZACION = {
     "nombrehoja": "st_cotizacion",
     "filainicial": 3,
     "numcotizacion": {"fila": 1, "columna": 2},
     "columnas": {
          "item": 1,
          "codigo": 2,
          "producto": 3,
          "preciounitario": 4,
          "cantidad": 5,
          "precio": 6,
          "todas": [1, 2, 3, 4, 5, 6]
     },
     "encabezados": 2
}

ST_BD_COTIZACIONES = {
     "nombrehoja": "st_bd_cotizaciones",
     "filainicial": 3,
     "columnas": {
          "idcotizacion": 1,
          "item": 2,
          "codigo": 3,
          "producto": 4,
          "preciounitario": 5,
          "cantidad": 6,
          "precio": 7,
          "todas": [1, 2, 3, 4, 5, 6, 7]
     },
     "encabezados": 2
}

ST_REGISTRO_COTIZACIONES = {
     "nombrehoja": "st_registro_cotizaciones",
     "filainicial": 3,
     "columnas": {
          "idcotizacion": 1,
          "descripcion": 2,
          "precio": 3,
          "todas": [1, 2, 3]
     },
     "encabezados": 2
}
