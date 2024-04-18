# hoja de parametros generales

LIBRODATOS = "./bd/mediclean_bd.xlsx"
CLIENTES = {
  "nombrehoja":"clientes", 
  "filainicial":2,
  "columnas":{
    "rut":1,
    "cliente":2,
    "direccion":3,
    "comuna":4,
    "telefono":5,
    "observaciones":6,
    "todas":[1,2,3,4,5,6]
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
  "filainicial":2,
  "columnas":{
    "fecha":1,
    "id":2,
    "rut":3,
    "cliente":4,
    "direccion":5,
    "comuna":6,
    "observaciones":7,
    "todas":[1,2,3,4,5,6,7]
  }, 
  "encabezados":1
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
    "observaciones":7,
    "todas":[1,2,3,4,5,6,7]
  }, 
  "encabezados":1
}

