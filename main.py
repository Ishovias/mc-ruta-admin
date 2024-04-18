from flask import Flask, redirect, url_for, request, render_template
from conectorbd import conectorbd
from coder.codexpy2 import codexpy2
from combletras.combletras import combletras
import params
import datetime

app = Flask(__name__)
coder = codexpy2()
scrab = combletras()

def autenticador(multidic: map) -> map:
  datos = {}
  if "aut" in request.args:
    aut = request.args["aut"]
    token = coder.getCurrentToken()
    if aut == token:
      datos["aut"] = token
      datos["plantilla"]:"index.html"
  else:
      datos["alerta"] = "USUARIO NO AUTORIZADO"
    
  return datos

@app.route('/')
def index() -> redirect:
  if request.args:
    if "aut" in request.args:
      verificacion = verificatoken(request.args)
      if verificacion:
        return redirect(url_for("inicio", aut=coder.getCurrentToken()))
  return redirect(url_for("login"))
  
@app.route('/inicio')
def inicio() -> render_template:
  if request.args:
    if verificatoken(request.args):
      datos["token"] = coder.getCurrentToken()
      return render_template("index.html", datos=datos)
  return redirect(url_for("login"))

@app.route('/login')
def login() -> render_template:
  if request.args:
    pass
  else:
    return render_template('autorizador.html', datos=datos)
  datos = autenticador(request.args)
  return render_template(datos["plantilla"], datos=datos)

@app.route('/autorizador', methods=['POST'])
def autorizador() -> redirect:
  userbd = conectorbd(conectorbd.hojaUsuarios)
  nombre = request.form["user"]
  contrasena = request.form["contrasena"]
  result = userbd.comprueba_usuario(nombre,contrasena)
  if result:
    resultado = coder.getCurrentToken()
  else:
    resultado = coder.ranToken()
  return redirect(url_for('login', aut=resultado))
  userbd.cierra_conexion()

@app.route('/accion', methods=['POST','GET'])
def accion() -> render_template:
    
    if request.args:
      pass
    else:
      return redirect(url_for('login', aut=coder.ranToken()))
    
    if "aut" in request.args:
      habilitador = verificatoken(request.args)
      print(request.args["aut"])
      print(habilitador)
      print(coder.getCurrentToken())
    
    datos = {
      "encabezado":"Registros de asistencia",
      "subtitulo":"(Secretario Pargua)",
      "habilitador":"disabled",
    }

    # Accion BOTON INGRESAR ASISTENCIA -------
    if "ingresarasistencia" in request.form:
        datos = {
        "encabezado":"Registros de asistencia",
        "subtitulo":"(Secretario Pargua)",
        "ingresarasistencia":True,
        }

    # Accion BOTON REGISTROS DE ASISTENCIA
    elif "registrosasistencias" in request.form or "registrosasistencias" in request.args:
        conexion = conectorbd(conectorbd.hojaAsistencia)
        registros = conexion.registros_asistencia()
        datos = {
        "encabezado":"Registros de asistencia históricos",
        "subtitulo":"(Secretario Pargua)",
        "registrosasistencias":registros,
        }
        conexion.cierra_conexion()

        if "alerta" in request.args:
            datos["alerta"] = request.args.get("alerta")

    # Accion BOTON INFORME HERMANO o BOTON INGRESAR INFORME
    elif "informehermano" in request.form or "ingresarinforme" in request.form or "datoshermanos" in request.form:
        
        if "informehermano" in request.form:
            datos = {
              "encabezado":"Informe de actividad por hermano",
              "subtitulo":"(Secretario Pargua)",
              "informehermano":True,
            }
            columnas_seleccionadas = [
              params.HOJA_DATOS["columnas"]["nombre"]
              ]
            filtrar_activos = None

        elif "ingresarinforme" in request.form:
            datos = {
            "encabezado":"Ingreso de informes",
            "subtitulo":"(Secretario Pargua)",
            "ingresoinformes":True,
            }
            columnas_seleccionadas = [
              params.HOJA_DATOS["columnas"]["nombre"],
              params.HOJA_DATOS["columnas"]["activo"]
              ]
            filtrar_activos = "activo"
        
        elif "datoshermanos" in request.form:
          datos = {
            "encabezado":"Datos hermanos",
            "subtitulo":"(Secretario Pargua)",
            "datoshermanos":True,
            }
          columnas_seleccionadas = [
            params.HOJA_DATOS["columnas"]["nombre"],
            params.HOJA_DATOS["columnas"]["activo"]
            ]
          filtrar_activos = None
        
        datosbd = conectorbd(conectorbd.hojaDatos)
        informesbd = conectorbd(conectorbd.hojaInformes)
        
        lista_hermanos = datosbd.listarhermanos(
          columnas_seleccionadas,
          filtrar_activos
          )
        
        if "ingresoinformes" in datos:
          lista_filtrada = informesbd.elimina_ingresados(lista_hermanos)
          lista_ingresados = informesbd.lista_ingresos_informes()
          
          datos["listahermanos"] = lista_filtrada
          datos["reporte"] = lista_ingresados
        else:
          datos["listahermanos"] = lista_hermanos

        datosbd.cierra_conexion()
        informesbd.cierra_conexion()
    print(habilitador)
    if habilitador:
      datos["aut"] = coder.setToken(request.args["aut"])
      return render_template('index.html', datos=datos)
    return redirect(url_for('login', aut=coder.ranToken()))

@app.route('/ingresa_asistencia', methods=['POST'])
def ingresa_asistencia() -> render_template:
    
    if request.args:
      pass
    else:
      return redirect(url_for('login', aut=coder.ranToken()))
    
    autorizar = False
    if "aut" in request.args:
      autorizar = verificatoken(request.args["aut"])
    
    if autorizar:
      token = coder.setToken(request.args["aut"])
    else:
      return redirect(url_for('login', aut=coder.ranToken())) 
      
    datos = {
        "encabezado":"Menu principal",
        "subtitulo":"(Secretario Pargua)",
        "ingresarasistencia":True,
        "aut":token
    }

    anomes = request.form["fecha_asistencia"][2:4] + request.form["fecha_asistencia"][5:7]
    dia = request.form["fecha_asistencia"][8:]
    tiporeunion = request.form["tiporeunion"]
    asistencia = request.form["asistencia"]
    observacion = request.form["observaciones"]
    
    data = [
      anomes,
      int(dia),
      tiporeunion,
      int(asistencia),
      observacion
      ]
    
    conexion = conectorbd(conectorbd.hojaAsistencia)
    resultado = conexion.ingresar_asistencia(data)
    datos["alerta"] = resultado
    
    conexion.cierra_conexion()
    return render_template('index.html', datos=datos)

@app.route('/elimina_asistencia', methods=['POST'])
def elimina_asistencia() -> redirect:
    if request.args:
      pass
    else:
      return redirect(url_for('login', aut=coder.ranToken()))
    
    autorizar = False
    if "aut" in request.args:
      autorizar = verificatoken(request.args["aut"])
    
    if autorizar:
      token = coder.setToken(request.args["aut"])
    else:
      return redirect(url_for('login', aut=coder.ranToken())) 
      
    conexion = conectorbd(conectorbd.hojaAsistencia)

    anomes = request.form["fechaeliminar"][2:4] + request.form["fechaeliminar"][5:7]
    dia = request.form["fechaeliminar"][8:]

    resultado = conexion.elimina_asistencia(anomes,dia)

    conexion.cierra_conexion()
    return redirect(url_for('accion',registrosasistencias="registrosasistencias", aut=token, alerta=resultado))

@app.route('/informehermano', methods=['POST'])
def informehermano() -> render_template:
    if request.args:
      pass
    else:
      return redirect(url_for('login', aut=coder.ranToken()))
    
    autorizar = False
    if "aut" in request.args:
      autorizar = verificatoken(request.args["aut"])
    
    if autorizar:
      token = coder.setToken(request.args["aut"])
    else:
      return redirect(url_for('login', aut=coder.ranToken())) 
      
    datosbd = conectorbd(conectorbd.hojaDatos)
    
    nombres_hermanos = datosbd.listarhermanos(
      [params.HOJA_DATOS["columnas"]["nombre"],
      params.HOJA_DATOS["columnas"]["activo"]],
      "activo"
      )
    
    datosbd.cierra_conexion()
    
    datos = {
        "encabezado":"Informe de actividad por hermano",
        "subtitulo":"(Secretario Pargua)",
        "informehermano":True,
        "listahermanos":nombres_hermanos,
        "aut":token
        }
        
    nombrehermano = request.form["listahermanos"]
    
    if nombrehermano == "--Seleccione--":
        return render_template('index.html', datos=datos)
    else:
        anoservicio = int(request.form["anoservicio"])
        fechainicio = str(anoservicio - 1) + "09"
        fechatermino = str(anoservicio) + "08"
        
        actividadbd = conectorbd(conectorbd.hojaActividad)
        
        datos["reporte"] = actividadbd.informe_hermano(fechainicio,fechatermino,nombrehermano)

        actividadbd.cierra_conexion()
        return render_template('index.html', datos=datos)

@app.route('/ingresoInforme', methods=['POST'])
def ingresoInforme() -> render_template:
    if request.args:
      pass
    else:
      return redirect(url_for('login', aut=coder.ranToken()))
    
    autorizar = False
    if "aut" in request.args:
      autorizar = verificatoken(request.args["aut"])
    
    if autorizar:
      token = coder.setToken(request.args["aut"])
    else:
      return redirect(url_for('login', aut=coder.ranToken())) 
      
    # Conexiones requeridas a bd
    datosbd = conectorbd(conectorbd.hojaDatos)
    informebd = conectorbd(conectorbd.hojaInformes)
    
    nombres_hermanos = datosbd.listarhermanos(
      [params.HOJA_DATOS["columnas"]["nombre"],
      params.HOJA_DATOS["columnas"]["activo"]],
      "activo"
      )
    if "btneliminanombre" in request.form:
      nombre = request.form["eliminarnombre"]
      if nombre != "--Seleccione--":
        informebd.elimina_informe(nombre)
        resultado = "informe eliminado"
      else:
        resultado = "Indica un nombre"
        
    if "ingresainforme" in request.form:
      anomes = request.form["anomes"]
      nombre = request.form["nombre"]
      cursos = request.form["cursos"]
      horas = request.form["horas"]
      observaciones = request.form["observaciones"]
      
      if "actividad" in request.form:
        actividad = 1
      else:
        actividad = 0
      
      if "auxiliar" in request.form:
        auxiliar = 1
      else:
        auxiliar = 0
      
      # estas funciones entregan listas
      privilegio = datosbd.extraeinfo(nombre,[params.HOJA_DATOS["columnas"]["privilegio"]])
      grupo = datosbd.extraeinfo(nombre,[params.HOJA_DATOS["columnas"]["grupo"]])
      
      # orden de los datos
      data = [
        nombre,
        int(anomes),
        privilegio[0],
        grupo[0],
        actividad,
        int(cursos),
        auxiliar,
        int(horas),
        observaciones
        ]
        
      resultado = informebd.ingresa_informe(data)
    
    nombres_porinformar = informebd.elimina_ingresados(nombres_hermanos)
    lista_ingresados = informebd.lista_ingresos_informes()
    lista_nombresIngresados = informebd.lista_nombres_informados()
    
    if "confirmarmes" in request.form:
      if len(nombres_porinformar) > 0 and "confirmar" not in request.form:
        resultado = "Aun faltan hermanos por informar. Para ingresar de todas formas, marca confirmar antes de presionar el boton"
      elif len(lista_ingresados["datos"]) == 0:
        resultado = "Aun no se ha ingresado siquiera un informe"
      else:
        confirmacion = informebd.confirmar_informes(lista_ingresados)
        if confirmacion[0]:
          informebd.limpiar_hoja_informes()
        resultado = confirmacion[1]
    
    if "eliminarecoleccion" in request.form:
      if "confirmar" in request.form:
        informebd.limpiar_hoja_informes()
        resultado = "Recoleccion de informes borrada"
      else:
        resultado = "Para borrar recoleccion actual selecciona casilla de confirmacion antes"
        
    nombres_porinformar = informebd.elimina_ingresados(nombres_hermanos)
    lista_ingresados = informebd.lista_ingresos_informes()
    lista_nombresIngresados = informebd.lista_nombres_informados()
    
    datos = {
        "encabezado":"Ingreso de informes",
        "subtitulo":"(Secretario Pargua)",
        "ingresoinformes":True,
        "listahermanos":nombres_porinformar,
        "reporte":lista_ingresados,
        "nombresingresados":lista_nombresIngresados,
        "alerta":resultado,
        "aut":token
        }
    
    datosbd.cierra_conexion()
    informebd.cierra_conexion()
    return render_template('index.html', datos=datos)

@app.route('/datoshermanos', methods=['POST','GET'])
def datoshermanos() -> render_template:
  if request.args:
    pass
  else:
    return redirect(url_for('login', aut=coder.ranToken()))
  
  autorizar = False
  if "aut" in request.args:
    autorizar = verificatoken(request.args["aut"])
  
  if autorizar:
    token = coder.setToken(request.args["aut"])
  else:
    return redirect(url_for('login', aut=coder.ranToken())) 
      
  def construye_fecha(date: str) -> map:
    fecha = {}
    fecha["ano"] = int(date[:4])
    fecha["mes"] = int(date[6:7])
    fecha["dia"] = int(date[9:])
    
    return fecha
    
  datosbd = conectorbd(conectorbd.hojaDatos)

  listahermanos = datosbd.listarhermanos(
    [params.HOJA_DATOS["columnas"]["nombre"]]
    )
  
  datos = {
    "encabezado":"Datos hermanos",
    "subtitulo":"(Secretario Pargua)",
    "datoshermanos":True,
    "listahermanos":listahermanos,
    }
    
  if request.args:
    nombre = request.args["nombre"]
    if "moddatos" in request.args:
      datos["disablemodifica"] = "disabled"
      datos["disableguarda"] = "enabled"
      datos["editar"] = "enabled"
    
    if "guardamod" in request.args:
      datastore = []
      for dato in request.args:
        datastore.append(request.args[dato])
        
      print(datastore)
    
      del datastore[0]
      
      try:
        fecha = construye_fecha(datastore[4])
        datastore[4] = datetime.datetime(
          fecha["ano"],
          fecha["mes"],
          fecha["dia"],
          0,0
          )
      except:
        pass
      
      try:
        fecha = construye_fecha(datastore[5])
        datastore[5] = datetime.datetime(
          fecha["ano"],
          fecha["mes"],
          fecha["dia"],
          0,0
          )
      except:
        pass
          
      datos["datastore"] = datastore
      
      datos["disablemodifica"] = "enabled"
      datos["disableguarda"] = "disabled"
      
      resultado = datosbd.actualiza_datos(nombre, datastore)
      datos["alerta"] = resultado
    
    if "eliminahermano" in request.args:
      if "confirmar" in request.args:
        nombrehermano = request.args["nombre"]
        resultado = datosbd.elimina_registro(nombrehermano)
        datos["alerta"] = f"Registro de {nombrehermano} eliminado"
      else:
        datos["alerta"] = "Si quieres eliminar al hermano debes confirmar la accion marcando el recuadro"
      
      listahermanos = datosbd.listarhermanos(
        [params.HOJA_DATOS["columnas"]["nombre"]]
        )
      datos["listahermanos"] = listahermanos
      return render_template('index.html', datos=datos)
      
  elif "nuevoregistro" in request.form:
    return redirect(url_for('nuevoregistro'))
  
  else:
    datos["disablemodifica"] = "enabled"
    datos["disableguarda"] = "disabled"
    datos["editar"] = "readonly"
    nombre = request.form["listahermanos"]
  
  # Extraccion de datos desde BD
  data = datosbd.extraeinfo(
    nombre,
    params.HOJA_DATOS["columnas"]["todas"]
    )
  
  hoy = datetime.datetime.now().year

  dfnac = data[5]
  dbaut = data[6]
  
  ## calculo de años de edad
  try:
    fnac = datetime.datetime.date(dfnac).year
  except:
    fnac = int(dfnac[:4])
  
  edad = hoy - fnac
  data.append(edad)
  
  try:
    fnac = datetime.datetime.date(dfnac)
    data[5] = fnac
  except:
    pass

  # Calculo de años de bautismo
  try:
    fbaut = datetime.datetime.date(dbaut).year
  except:
    try:
      fbaut = int(dbaut[:4])
    except:
      data.append(0)
    else:
      bautizado = hoy - fbaut
      data.append(bautizado)
  else:
    bautizado = hoy - fbaut
    data.append(bautizado)
    fbaut = datetime.datetime.date(dbaut)
    data[6] = fbaut
  finally:
    hoy = datetime.datetime.today().date()

  data.append(hoy)
  
  datos["data"] = data
  datosbd.cierra_conexion()
  return render_template('index.html', datos=datos)

@app.route('/nuevoregistro', methods=['POST','GET'])
def nuevoregistro() -> render_template:
  normadosbd = conectorbd(conectorbd.hojaDatosNormados)
  datosbd = conectorbd(conectorbd.hojaDatos)
  
  privilegios = normadosbd.listado_privilegios()
  
  datos = {
    "encabezado":"Nuevo registro de hermano(a)",
    "subtitulo":"(Secretario Pargua)",
    "nuevoregistro":True,
    "privilegios":privilegios
  }
  
  if "ingreso" in request.args:
    data = []
    for dato in request.form:
      data.append(request.form[dato])
    resultado = datosbd.ingresa_nuevo_registro(data)
    datos["alerta"] = resultado
    datos["data"] = data
    
  normadosbd.cierra_conexion()
  datosbd.cierra_conexion()
  return render_template('index.html', datos=datos)

@app.route('/codex', methods=['POST','GET'])
def codex() -> render_template:
  
  if request.args:
    palabra = request.args["ingreso"]
    if "codificar" in request.args:
      resultado = coder.encripta(palabra)
    elif "decodificar" in request.args:
      resultado = coder.desencripta(palabra)
  else:
    resultado = ""
  
  datos = {
    "encabezado":"Codificador CODEXPY ver.2",
    "subtitulo":"(Isho apps)",
    "codexpy":True,
    "resultado":resultado
    }
  
  return render_template('codexpy.html', datos=datos)

@app.route('/scrabbleletras', methods=['POST','GET'])
def scrabbleletras() -> render_template:
  
  if request.args:
    letras = request.args["letras"]
    resultado = scrab.buscar_palabras(letras)
    titulotabla = "LISTA DE COMBINACIONES VÁLIDAS"

  else:
    resultado = ""
    titulotabla = "Ingresa las letras"


  datos = {
    "encabezado":"Scrabble letras",
    "subtitulo":"(Isho apps)",
    "scrabbleletras":True,
    "resultado":resultado,
    "titulotabla":titulotabla
    }
  return render_template('scrabbleletras.html', datos=datos)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
