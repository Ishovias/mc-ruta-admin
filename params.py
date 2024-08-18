# hoja de parametros generales

LIBRODATOS = "./bd/mediclean_bd.xlsx" # Ruta de desarrollo
# LIBRODATOS = "/home/iberoiza/mediclean/bd/mediclean_bd.xlsx" # Ruta en linea
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
    "gps":8,
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
    "gps":8,
    "otro":9,
    "ultimoretiro":10,
    "status":11,
    "detalleretiro":12,
    "todas":[1,2,3,4,5,6,7,8,9,10,11,12]  
  }, 
  "encabezados":1
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
    "todas":[1,2,3,4,5]  
  }, 
  "encabezados":1    
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