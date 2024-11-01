# hoja de parametros generales


# ---------- RUTAS DE DESARROLLO --------------
LIBRODATOS = "./bd/mediclean_bd.xlsx"
LIBROTODO = "./bd/todo_bd.xlsx"
LIBRORUTA= "./bd/ruta.xlsx"
LIBROST = "./bd/sublitote_bd.xlsx"
RUTA_IMPORTACION = "./ruta_import"

# ---------- RUTAS DE PRODUCCION --------------
#LIBRODATOS = "/home/iberoiza/mediclean/bd/mediclean_bd.xlsx" 
#LIBROTODO = "/home/iberoiza/mediclean/bd/todo_bd.xlsx"
#LIBRORUTA= "/home/iberoiza/mediclean/bd/ruta.xlsx"
#RUTA_IMPORTACION = "/home/iberoiza/mediclean/ruta_import"
#UPLOAD_FOLDER = "/home/iberoiza/mediclean/ruta_import"

EXTENSIONES_PERMITDAS = {"xlsx","xls"}
MAX_FILAS = 10000

CLIENTES = {
  "nombrehoja":"clientes", 
  "filainicial":2,
  "columnas":{
    "estado":1,
    "rut":2,
    "cliente":3,
    "direccion":4,
    "comuna":5,
    "telefono":6,
    "gps":7,
    "otro":8,
    "diascontrato":9,
    "ultimoretiro":10,
    "proxretiro":11,
    "todas":[1,2,3,4,5,6,7,8,9,10,11]
  }, 
  "encabezados":1
}

USUARIO = {
  "nombrehoja":"usuarios", 
  "filainicial":2,
  "columnas":{
    "usuario":1,
    "contrasena":2,
    "token":3,
    "todas":[1,2,3]
  }, 
  "encabezados":1
}

RUTA_ACTUAL = {
  "nombrehoja":"ruta_actual", 
  "filainicial":3,
  "rutaencurso":{"fila":1,"columna":2},
  "nombreruta":{"fila":1,"columna":3},
  "REALIZADO":{"fila":1,"columna":4},
  "POSPUESTO":{"fila":1,"columna":5},
  "columnas":{
    "fecha":1,
    "id":2,
    "rut":3,
    "cliente":4,
    "direccion":5,
    "comuna":6,
    "telefono":7,
    "contrato":8,
    "otro":9,
    "ultimoretiro":10,
    "todas":[1,2,3,4,5,6,7,8,9,10]
  }, 
  "encabezados":2
}

RUTAS_BD = {
  "nombrehoja":"rutas_bd", 
  "filainicial":2,
  "columnas":{
    "fecha":1,
    "id":2,
    "rut":3,
    "cliente":4,
    "direccion":5,
    "comuna":6,
    "telefono":7,
    "contrato":8,
    "otro":9,
    "ultimoretiro":10,
    "status":11,
    "detalleretiro":12,
    "farmaco":13,
    "patologico":14,
    "contaminado":15,
    "cortopunzante":16,
    "otropeligroso":17,
    "liquidorx":18,
    "cajaroja_0.5":19,
    "cajaroja_1":20,
    "cajaroja_1.3":21,
    "cajaroja_1.65":22,
    "cajaroja_3":23,
    "cajaamarilla_1":24,
    "cajaamarilla_3":25,
    "cajaamarilla_5":26,
    "cajaamarilla_15":27,
    "basureroamarillo_120":28,
    "bolsaroja":29,
    "bolsaroja_farmaco":30,
    "bolsaamarilla":31,
    "bidon_5":32,
    "frascoamalgama":33,
    "todas":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,23,23,24,25,26,27,28,29,30,31,32,33]  
  }, 
  "encabezados":1,
  "encabezados_nombre":[
      "",
      "Fecha",
      "ID",
      "Rut",
      "Cliente",
      "Direccion",
      "Comuna",
      "Telefono",
      "Contrato",
      "Otro",
      "Ultimo Retiro",
      "Status",
      "Detalle Retiro",
      "Farmaco",
      "Patologico",
      "Contaminado",
      "Cortopunzante",
      "Otro (Peligroso)",
      "Liquido (RX)"
      ]
}

RUTAS_REGISTROS = {
  "nombrehoja":"rutas_registros", 
  "filainicial":2,
  "columnas":{
    "fecha":1,
    "ruta":2,
    "REALIZADO":3,
    "POSPUESTO":4,
    "otros":5,
    "farmaco":6,
    "patologico":7,
    "contaminado":8,
    "cortopunzante":9,
    "otropeligroso":10,
    "liquidorx":11,
    "todas":[1,2,3,4,5,6,7,8,9,10,11]  
  }, 
  "encabezados":1,
  "encabezados_nombre":[
    "",
    "Fecha",
    "Ruta",
    "REALIZADO",
    "POSPUESTO",
    "Otros",
    "Farmaco",
    "Patologico",
    "Contaminado",
    "Cortopunzante",
    "Otro (Peligroso)",
    "Liquido (RX)"
  ]    
}

GASTOS_BD = {
  "nombrehoja":"gastos_bd", 
  "filainicial":2,
  "columnas":{
    "fecha":1,
    "monto":2,
    "descripcion":3,
    "todas":[1,2,3]
  }, 
  "encabezados":1
}

INVENTARIOS = {
  "nombrehoja":"inventarios",
  "filaStockActual":2,
  "filainicial":4,
  "columnas":{
    "fecha":1,
    "cajaroja_0.5":2,
    "cajaroja_1":3,
    "cajaroja_1.3":4,
    "cajaroja_1.65":5,
    "cajaroja_3":6,
    "cajaamarilla_1":7,
    "cajaamarilla_3":8,
    "cajaamarilla_5":9,
    "cajaamarilla_15":10,
    "basureroamarillo_120":11,
    "bolsaroja":12,
    "bolsaroja_farmaco":13,
    "bolsaamarilla":14,
    "bidon_5":15,
    "frascoamalgama":16,
    "guias":17,
    "amarras_paquete":18,
    "mascarillas":19,
    "guantes":20,
    "alcoholgel":21,
    "todas":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
  }, 
  "encabezados":1,
  "encabezados_nombre":[
    None,
    "FECHA",
    "CAJA ROJA 0,5 LTS (x unidad)",
    "CAJA ROJA 1 LTS (x unidad)",
    "CAJA ROJA 1,3 LTS (x unidad)",
    "CAJA ROJA 1,65 LTS (x unidad)",
    "CAJA ROJA 3 LTS (x unidad)",
    "CAJA AMARILLA 1 LTS (x unidad)",
    "CAJA AMARILLA 3 LTS (x unidad)",
    "CAJA AMARILLA 5 LTS (x unidad)",
    "CAJA AMARILLA 15 LTRS (x unidad)",
    "BASURERO AMARILLO 120 LTRS (x unidad)",
    "BOLSAS ROJAS (x unidad)",
    "BOLSAS ROJAS FARMACOS (x unidad)",
    "BOLSAS AMARILLAS (x unidad)",
    "BIDON 5 LTS (x unidad)",
    "FRASCO AMALGAMAS (x unidad)",
    "TALONARIO GUIAS (x unidad)",
    "PQTE. AMARRAS PLASTICAS",
    "MASCARILLAS",
    "GUANTES",
    "ALCOHOL GEL"
    ]
}

RETIROS_ELIMINADOS = {
  "nombrehoja":"retiros_eliminados", 
  "encabezados":1,
  "filainicial":2,
  "columnas":{
    "fecha":1,
    "id":2,
    "rut":3,
    "cliente":4,
    "direccion":5,
    "comuna":6,
    "telefono":7,
    "contrato":8,
    "otro":9,
    "ultimoretiro":10,
    "status":11,
    "detalleretiro":12,
    "farmaco":13,
    "patologico":14,
    "contaminado":15,
    "cortopunzante":16,
    "otropeligroso":17,
    "liquidorx":18,
    "todas":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
  }
}

REGISTRO_ELIMINACIONES = {
  "nombrehoja":"registro_eliminaciones",
  "encabezados":1,
  "filainicial":2,
  "columnas":{
    "fechaeliminacion":1,
    "observacion":2,
    "farmaco":3,
    "patologico":4,
    "contaminado":5,
    "cortopunzante":6,
    "otropeligroso":7,
    "liquidorx":8,
    "todas":[1,2,3,4,5,6,7,8]
  }
}

# ----------- APP SUBLITOTE --------------

TODO = {
  "nombrehoja":"todo_list", 
  "filainicial":2,
  "columnas":{
    "fecha":1,
    "descripcion":2,
    "completado":3,
    "fechacompletado":4,
    "todas":[1,2,3,4]
  }, 
  "encabezados":1
}

ST_PRODUCTOS = {
  "nombrehoja":"st_productos", 
  "filainicial":3,
  "columnas":{
    "codigo":1,
    "producto":2,
    "preciocosto":3,
    "precioventa":4,
    "existencias":5,
    "observaciones":6,
    "todas":[1,2,3,4,5,6]
  }, 
  "encabezados":2
} 

ST_COTIZACION = {
  "nombrehoja":"st_cotizacion", 
  "filainicial":3,
  "numcotizacion":{"fila":1,"columna":2},
  "columnas":{
    "item":1,
    "codigo":2,
    "producto":3,
    "preciounitario":4,
    "cantidad":5,
    "precio":6,
    "todas":[1,2,3,4,5,6]
  }, 
  "encabezados":2
} 

ST_BD_COTIZACIONES = {
  "nombrehoja":"st_bd_cotizaciones", 
  "filainicial":3,
  "columnas":{
    "idcotizacion":1,
    "item":2,
    "codigo":3,
    "producto":4,
    "preciounitario":5,
    "cantidad":6,
    "precio":7,
    "todas":[1,2,3,4,5,6,7]
  }, 
  "encabezados":2
} 

ST_REGISTRO_COTIZACIONES = {
  "nombrehoja":"st_registro_cotizaciones", 
  "filainicial":3,
  "columnas":{
    "idcotizacion":1,
    "descripcion":2,
    "precio":3,
    "todas":[1,2,3]
  }, 
  "encabezados":2
}
