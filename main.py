from flask import Flask, render_template, jsonify, request, make_response, redirect, url_for
from werkzeug.utils import secure_filename
from pdfgen import PDFGen, Cord
from helpers import privilegios, login_required
from coder.codexpy import Codexpy
from coder.codexpy2 import Codexpy2
from enigmacoder.en_coder import EnCoder
from urllib.parse import quote, unquote
from cimprime import cimprime
from datetime import datetime, timedelta
import conector
import params
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = params.RUTA_IMPORTACION
sesion = conector.SessionSingleton()

@app.route('/')
@login_required
def index():
    token = request.cookies.get("aut")# {{{
    usuario = sesion.get_usuario(token)
    datos = privilegios(usuario)
    datos["tituloPagina"] = "Administracion de ruta"
    datos["user_connected"] = usuario
    return render_template('bienvenida.html', datos=datos)# }}}

# ============ RUTAS CODER ================
# {{{
@app.route('/getapikey', methods=['POST'])
def getapikey():
    json = request.get_json()
    usuario = json.get("user")
    contrasena = json.get("pswd")
    token = sesion.iniciar_sesion(usuario, contrasena)
    return jsonify({"token":token} if token else {"error":"Usuario o contraseña incorrecto"})

@app.route('/login', methods=['GET', 'POST'])
def login():
    datos = {
            "tituloPagina":"Login"
            }
    if request.method == 'GET':
        return render_template('login.html', datos=datos)
    elif request.method == 'POST':
        usuario = request.form.get("usuario")
        contrasena = request.form.get("contrasena")
        token = sesion.iniciar_sesion(usuario, contrasena)
        token_expires = datetime.now() + timedelta(hours=24)
        if token:
            response = make_response(redirect(url_for('index')))
            response.set_cookie(
                    "aut",
                    value=token,
                    httponly=True,
                    samesite='Lax',
                    expires=token_expires
                    )
            return response
        datos["incorrecto"] = True
        return render_template('login.html', datos=datos)

@app.route('/logout', methods=['POST'])
def logout():
    token = request.cookies.get("aut")
    sesion.del_user(token)
    response = make_response(redirect('login'))
    response.delete_cookie("aut")
    return response
# }}}

# ============ RUTAS CODER ================
# {{{
@app.route('/coder')
@login_required
def coder():# {{{
    token = request.cookies.get("aut")
    usuario = sesion.get_usuario(token)
    datos = {
            "tituloPagina":"CODER"
            }
    datos = privilegios(usuario,datos)
    return render_template('coder.html', datos=datos)# }}}

@app.route('/coder1/frcod')
@login_required
def coder1():# {{{
    frase = request.args.get("fr")
    coder = Codexpy()
    return jsonify({"frproc":coder.procesa(frase)})# }}}

@app.route('/coder2/frcod')
@login_required
def coder2():# {{{
    frase = request.args.get("fr")
    coder = Codexpy2()
    return jsonify({"frproc":coder.encripta(frase) if frase else "- Ingresa palabra -"})#}}}

@app.route('/coder2/frdec')
@login_required
def coder2deco():# {{{
    frase = request.args.get("fr")
    coder = Codexpy2()
    return jsonify({"frproc":coder.desencripta(frase) if frase else "- Ingresa palabra -"})#}}}

@app.route('/enicod', methods=["GET","POST"])
@login_required
def enicod():# {{{
    if request.method == "GET":
        token = request.cookies.get("aut")
        usuario = sesion.get_usuario(token)
        datos = {
                "tituloPagina":"ENIGMA CODER"
                }
        datos = privilegios(usuario,datos)
        return render_template('enigmacoder.html', datos=datos)
    elif request.method == "POST":
        datos = request.get_json()
        frase = datos.get("frase")
        clave = datos.get("clave")
        cod = EnCoder(clave)
        return jsonify({"frproc":cod.codifica(frase)})# }}}
# }}}

# ========== RUTAS CLIENTES ===============
# {{{
@app.route('/clientes')
@login_required
def clientes():# {{{
    usuario = sesion.get_usuario(request.cookies.get("aut"))
    datos = privilegios(usuario)
    datos["tituloPagina"] = "Administracion clientes"
    return render_template('clientes.html', datos=datos)# }}}

@app.route('/clientes/buscar')
@login_required
def clientes_buscar():# {{{
    busqueda = request.args.get("search")
    filtro = request.args.get("filtro")
    resultados = conector.sindatos
    if len(busqueda) > 1:
        resultados = conector.buscar_cliente(busqueda, filtro)
    return jsonify(resultados)# }}}

@app.route('/clientes/getid/<idcliente>')
@login_required
def cliente_get_nombre(idcliente):
    return jsonify(conector.get_cliente(idcliente))

@app.route('/clientes/newclient', methods=['GET','POST'])
@login_required
def clientes_nuevo():# {{{
    resultado = conector.formulario_nuevo_cliente(request)
    if "render" in resultado:
        return render_template('cliente_nuevo.html', datos=resultado.get("render"))
    else:
        return jsonify({"newClienteOK":resultado.get("realizado")}), resultado.get("status")# }}}
# }}}

# ============== RUTAS ========================
# {{{
@app.route('/rutas/rutaactual', methods=['POST','GET'])
@login_required
def rutaactual():# {{{
    usuario = sesion.get_usuario(request.cookies.get("aut"))
    datos = privilegios(usuario)
    datos["tituloPagina"] = "Gestor de ruta actual"
    return render_template('rutas_rutaactual.html', datos=datos)# }}}

@app.route('/rutas/rutaactual/getData', methods=["POST"])
@login_required
def rutaactual_getdata():# {{{
    return jsonify(conector.get_cl_enruta())# }}}

@app.route('/rutas/sumario/rutaactual', methods=["GET"])
@login_required
def rutaactual_sumario():# {{{
    return jsonify(conector.get_sumario())# }}}

@app.route('/rutas/rutaactual/aruta', methods=["POST"])
@login_required
def rutaactual_cliente_aruta():# {{{
    return '', conector.cliente_a_ruta(request)# }}}

@app.route('/rutas/rutaactual/eliminarcliente/<ubicacion>', methods=["POST"])
@login_required
def rutaactual_eliminarcliente(ubicacion):# {{{
    return jsonify({"resultado":conector.eliminar_ubicacion("clientes",ubicacion)})# }}}

@app.route('/rutas/rutaactual/confpos', methods=["POST"])
@login_required
def rutaactual_confpos():# {{{
    data = conector.cliente_confpos(
                ubicacion=request.args.get("idclte"),
                observaciones=request.args.get("observaciones"),
                accion=request.args.get("accion")
                )
    if request.args.get("accion") == "REALIZADO":
        conector.inv_registra_mov(data)
    return jsonify({"accion_cliente":request.args.get("accion")})# }}}

@app.route('/rutas/rutaactual/clientemanual', methods=["POST"])
@login_required
def rutaactual_clientemanual():# {{{
    conector.cliente_manual(request)
    return jsonify({"message":"Exito"}), 200# }}}

@app.route('/rutas/rutaactual/movpos/<pos_pos>', methods=["PUT"])
@login_required
def rutaactual_movpos(pos_pos):# {{{
    ubicaciones = pos_pos.split("-")
    pos_a = int(ubicaciones[0])
    pos_b = int(ubicaciones[1])
    return jsonify({"resultado":conector.movpos(pos_a,pos_b)})# }}}
# }}}

# ============== RUTAS BD ========================
# {{{
@app.route('/rutas/rutabd')
@login_required
def rutabd():# {{{
    datos = privilegios(sesion.get_usuario(request.cookies.get("aut")))
    datos["tituloPagina"] = "Registros de ruta"
    return render_template('rutas_bd.html', datos=datos)# }}}

@app.route('/rutas/rutabd/getData', methods=["POST"])
@login_required
def rutabd_getlista():# {{{
    return jsonify(conector.get_rutas())# }}}

@app.route('/rutas/rutabd/getRuta/<fecharuta>', methods=["POST"])
@login_required
def rutabd_getruta(fecharuta):# {{{
    return jsonify(conector.get_ruta(fecharuta))# }}}

@app.route('/rutas/rutabd/getTotales/<fecharuta>', methods=["POST"])
@login_required
def rutabd_gettotales(fecharuta):# {{{
    return jsonify({"totales":conector.get_totales_ruta(fecharuta)})# }}}

@app.route('/rutas/rutabd/marcarStatus', methods=["POST"])
@login_required
def rutabd_marcarstatus():# {{{
    ubicacion = request.args.get('ubicacion')
    status = request.args.get('status')
    conector.marcar_status(ubicacion,status)
    return jsonify({"message":"ok"}), 200# }}}

@app.route('/rutas/rutabd/buscar')
@login_required
def rutabd_busqueda():# {{{
    busqueda = request.args.get("search")
    filtro = request.args.get("filtro")
    resultados = conector.sindatos
    if len(busqueda) > 1:
        resultados = conector.rutas_buscar_dato(busqueda,filtro)
        resultados = resultados if resultados else conector.sindatos
    return jsonify(resultados)# }}}

@app.route('/rutas/rutabd/modregistro/<idy>', methods=["GET","PUT"])
@login_required
def rutabd_mod_registro(idy):# {{{
    modregistro = conector.rutabd_modregistro(request, idy)
    if "render" in modregistro:
        modregistro["render"] = privilegios(sesion.get_usuario(request.cookies.get("aut")), modregistro["render"])
        return render_template('rutabd_modregistro.html',datos=modregistro.get("render"))
    else:
        return jsonify(modregistro)#}}}
# }}}

# ------------------- INVENTARIO ----------------------------
# {{{
@app.route('/inventario')
@login_required
def inventario():# {{{
    datos = privilegios(sesion.get_usuario(request.cookies.get("aut")))
    datos["tituloPagina"] = "Inventario de insumos en stock"
    return render_template('inventario.html', datos=datos)# }}}

@app.route('/inventario/getstock')
@login_required
def inventario_getstock():# {{{
    return jsonify(conector.inv_get_stock())# }}}

@app.route('/inventario/modifica', methods=['POST','GET'])
@login_required
def inventario_modifica():# {{{
    if request.method == "POST":
        cantidad = request.args.get("cant")
        columna = request.args.get("col")
        conector.inv_mod_stock(
            cantidad=cantidad,
            columna=columna
            )
        return '', 200
    elif request.method == "GET":
        datos = privilegios(sesion.get_usuario(request.cookies.get("aut")))
        datos["tituloPagina"] = "Modificacion de inventario"
        return render_template('inventario_mod.html', datos=datos)#}}}
# }}}

# ========== UPLOAD RUTA  ===============
# {{{
@app.route('/uploadRuta', methods=['POST','GET'])
@login_required
def uploadRuta() -> render_template:# {{{
    if request.method == 'POST':
        statuscode = 400
        jsondata = {"message":"Error en archivo o archivo no permitido"}
        def fichero_permitido(archivo: str) -> bool:
            return "." in archivo and archivo.rsplit(".",1)[1].lower() in params.EXTENSIONES_PERMITDAS
        if "file" in request.files:
            if "file" not in request.files:
                statuscode = 400
                jsondata = {"message":"No se ha cargado archivo"}
            else:
                file = request.files["file"]
                if file.filename == "":
                    statuscode = 400
                    jsondata = {"message":"No se ha cargado ningun archivo valido"}
            if file and fichero_permitido(file.filename):
                filename = secure_filename(file.filename)
                archivo_cargado = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(archivo_cargado)
                datos = conector.extrae_ruta(archivo_cargado)
                os.system(f"rm {archivo_cargado}")
                idcliente = datos["orden_columnas"].index("id")
                for fila in datos["datos"]:
                    if not fila[idcliente] or fila[idcliente] == "None":
                        mapdatos = {}
                        for dato in fila:
                            index = fila.index(dato)
                            mapdatos[datos["orden_columnas"][index]] = dato
                        mapdatos["contrato"] = "60"
                        mapdatos["estado"] = "activo"
                        mapdatos["otro"] = "cliente ingresado automaticamente"
                        retorno_id = conector.nuevo_cliente(mapdatos,datoeval="cliente",retornoid=True)
                        datos["datos"][datos["datos"].index(fila)][idcliente] = retorno_id
                if conector.importa_datos(datos):
                    statuscode = 200
                    jsondata = {
                            "message":"Importacion realizada con éxito",
                            "resultado":True
                            }
                else:
                    statuscode = 400
                    jsondata = {
                            "message":"Error al intentar escribir los datos",
                            "resultado":False
                            }
        return jsonify(jsondata), statuscode
    elif request.method == 'GET':
        datos = privilegios(sesion.get_usuario(request.cookies.get("aut")))
        datos["tituloPagina"] = "Carga de ruta XLS"
        return render_template('uploadruta.html', datos=datos)# }}}
# }}}

# =========== RUTAS DE GASTOS ===========
# {{{
@app.route('/gastos')
@login_required
def gastos() -> render_template:
    datos = conector.get_campos_formulario()
    datos = privilegios(sesion.get_usuario(request.cookies.get("aut")), datos)
    datos["tituloPagina"] = "Registro de gastos"
    return render_template('gastos.html', datos=datos)

@app.route('/gastos/getData/<fecha>')
@login_required
def gastos_getdata(fecha) -> jsonify:
    if fecha == "vigente":
        datos = conector.get_data()
        if not datos:
            datos = {
                    "encabezados":["Sin datos"],
                    "datos":[["-- Sin datos --"]]
                    }
        datos["totales"] = conector.get_totales()
    else:
        if "-" in fecha:
            fecha = fecha.replace("-","")
        datos = conector.get_data(fecha)
        datos["totales"] = conector.get_totales(fecha)
    return jsonify(datos)

@app.route('/gastos/totales/<fecha>')
@login_required
def gastos_totales(fecha) -> jsonify:
    if fecha == "vigente":
        fecha = None
    return jsonify({"totales":conector.get_totales(fecha)})

@app.route('/gastos/getFechas')
@login_required
def gastos_getfechas() -> jsonify:
    return jsonify({"fechas":conector.get_fechas()})

@app.route('/gastos/addGasto', methods=["POST"])
@login_required
def gastos_addgasto() -> jsonify:
    form = request.form.to_dict()
    return jsonify({"resultado":conector.add_gasto(form)})

@app.route('/gastos/rendir/<fecha>', methods=["GET","PATCH"])
@login_required
def gastos_rendir(fecha) -> render_template:
    if request.method == "GET":
        conector.rendicion(fecha)
        datos = privilegios(sesion.get_usuario(request.cookies.get("aut")))
        datos["tituloPagina"] = f"Rendicion gastos: {fecha}"
        datos["fecha"] = fecha
        datos["cerrado"] = False
        if fecha != "vigente":
            datos["cerrado"] = True
        return render_template("rendicion.html", datos=datos)
    elif request.method == "PATCH":
        return jsonify({"resultado":conector.rendicion(fecha,cerrar=True)})

@app.route('/gastos/eliminar/<idy>', methods=['DELETE'])
@login_required
def gastos_eliminar(idy) -> jsonify:
    status = 400
    resultado = conector.eliminar_ubicacion("gastos",idy)
    if resultado:
        status = 200
    return jsonify({"resultado":resultado}),400
# }}}

if __name__ == '__main__':
    app.run(debug=True)

