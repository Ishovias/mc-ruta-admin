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
    "todas":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]  
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
