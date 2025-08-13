from flask import Flask, render_template, jsonify, request, make_response, redirect, url_for
from werkzeug.utils import secure_filename
from handlers.clientes import Clientes
from handlers.rutas import RutaActual, RutaRegistros, RutaBD, RutaImportar
from handlers.inventarios import Inventario
from helpers import SessionSingleton, privilegios, login_required
from coder.codexpy import Codexpy
from coder.codexpy2 import Codexpy2
from urllib.parse import quote, unquote
from cimprime import cimprime
from datetime import datetime, timedelta
import params
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = params.RUTA_IMPORTACION
sesion = SessionSingleton()

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

@app.route('/')
@login_required
def index():
    token = request.cookies.get("aut")
    usuario = sesion.get_usuario(token)
    datos = privilegios(usuario)
    datos["tituloPagina"] = "Administracion de ruta"
    datos["user_connected"] = usuario
    return render_template('bienvenida.html', datos=datos)

@app.route('/coder')
@login_required
def coder():
    token = request.cookies.get("aut")
    usuario = sesion.get_usuario(token)
    datos = {
            "tituloPagina":"CODER"
            }
    datos = privilegios(usuario,datos)
    return render_template('coder.html', datos=datos)

@app.route('/coder1/frcod')
@login_required
def coder1():
    frase = request.args.get("fr")
    coder = Codexpy()
    return jsonify({"frproc":coder.procesa(frase)})

@app.route('/coder2/frcod')
@login_required
def coder2():
    frase = request.args.get("fr")
    coder = Codexpy2()
    return jsonify({"frproc":coder.encripta(frase) if frase else "- Ingresa palabra -"})

@app.route('/coder2/frdec')
@login_required
def coder2deco():
    frase = request.args.get("fr")
    coder = Codexpy2()
    return jsonify({"frproc":coder.desencripta(frase) if frase else "- Ingresa palabra -"})

@app.route('/clientes')
@login_required
def clientes():
    usuario = sesion.get_usuario(request.cookies.get("aut"))
    datos = privilegios(usuario)
    datos["tituloPagina"] = "Administracion clientes"
    return render_template('clientes.html', datos=datos)

@app.route('/clientes/buscar')
@login_required
def clientes_buscar():
    busqueda = request.args.get("search")
    filtro = request.args.get("filtro")
    sindatos = {"sindatos":"No se encontraron clientes coincidentes con esa busqueda"}
    resultados = sindatos
    if len(busqueda) > 1:
        with Clientes() as cl:
            resultados = cl.busca_cliente(
                busqueda=busqueda,
                filtro=filtro
                )
            resultados = resultados if resultados else sindatos
    return jsonify(resultados)

@app.route('/clientes/getid/<idcliente>')
@login_required
def cliente_get_nombre(idcliente):
    with Clientes() as cl:
        cliente = cl.get_cliente(idcliente,"id")
    return jsonify(cliente)

@app.route('/clientes/newclient', methods=['GET','POST'])
@login_required
def clientes_nuevo():
    if request.method == 'GET':
        with Clientes() as cl:
            campos = cl.mapdatos(
                    columnas=cl.hoja_actual["ncolumnas"]
                    )
            campos["id"]["dato"] = int(cl.get_id()) + 1
            del campos["estado"]
        return render_template('cliente_nuevo.html', datos=campos)
    elif request.method == 'POST':
        data = {}
        for campo in params.CLIENTES["ncolumnas"]:
            data[campo] = request.form.get(campo)
        data["estado"] = "activo"
        with Clientes() as cl:
            realizado = cl.nuevo_cliente(data)
            status = 201 if realizado else 400
        return jsonify({"newClienteOK":realizado}), status
    
# ============== RUTAS ========================

@app.route('/rutas/rutaactual', methods=['POST','GET'])
@login_required
def rutaactual():
    usuario = sesion.get_usuario(request.cookies.get("aut"))
    datos = privilegios(usuario)
    datos["tituloPagina"] = "Gestor de ruta actual"
    return render_template('rutas_rutaactual.html', datos=datos)

@app.route('/rutas/rutaactual/getData', methods=["POST"])
@login_required
def rutaactual_getdata():
    with RutaBD() as rbd:
        return jsonify(rbd.clientes_enruta())

@app.route('/rutas/rutaactual/aruta', methods=["POST"])
@login_required
def rutaactual_cliente_aruta():
    statuscode = 200
    with Clientes() as cl:
        datos_cliente = cl.get_cliente(
                dato=request.args.get("idclte"),
                tipo="id"
                )
    with RutaBD() as rbd:
        fecha = request.args.get("fecha")
        nombreruta = request.args.get("nombreruta")
        if not rbd.obtener_nombre_ruta(fecha) and not nombreruta:
            statuscode =  400
        elif nombreruta:
            rbd.cliente_a_ruta(datos_cliente,fecha,nombreruta)
        else:
            rbd.cliente_a_ruta(datos_cliente,fecha)
    return '', statuscode

@app.route('/rutas/rutaactual/eliminarcliente/<ubicacion>', methods=["POST"])
@login_required
def rutaactual_eliminarcliente(ubicacion):
    with RutaBD() as rbd:
        return jsonify({"resultado":rbd.eliminar(ubicacion)})

@app.route('/rutas/rutaactual/confpos', methods=["POST"])
@login_required
def rutaactual_confpos():
    with RutaBD() as rbd:
        data = rbd.cliente_confpos(
                ubicacion=request.args.get("idclte"),
                observaciones=request.args.get("observaciones"),
                accion=request.args.get("accion")
                )
    if request.args.get("accion") == "REALIZADO":
        with Inventario() as inv:
            inv.registra_movimiento(data)
    return jsonify({"accion_cliente":request.args.get("accion")})

@app.route('/rutas/rutaactual/clientemanual', methods=["POST"])
@login_required
def rutaactual_clientemanual():
    with RutaBD() as rbd:
        mapdatos = {}
        columnas = rbd.hoja_actual["rutaactual"].copy()
        for campo in columnas:
            if campo in request.form:
                mapdatos[campo] = {"dato":request.form.get(campo)}
        rbd.cliente_a_ruta(
                mapdatos=mapdatos,
                fecha=int(request.form.get("fecha"))
                )
    return jsonify({"message":"Exito"}), 200

@app.route('/rutas/rutaactual/movpos/<pos_pos>', methods=["PUT"])
@login_required
def rutaactual_movpos(pos_pos):
    ubicaciones = pos_pos.split("-")
    pos_a = int(ubicaciones[0])
    pos_b = int(ubicaciones[1])
    cimprime(pos_a=pos_a,pos_b=pos_b)
    with RutaBD() as r:
        return jsonify({"resultado":r.movpos(pos_a,pos_b)})

    # ============== RUTAS BD ========================
@app.route('/rutas/rutabd')
@login_required
def rutabd():
    datos = privilegios(sesion.get_usuario(request.cookies.get("aut")))
    datos["tituloPagina"] = "Registros de ruta"
    return render_template('rutas_bd.html', datos=datos)

@app.route('/rutas/rutabd/getData', methods=["POST"])
@login_required
def rutabd_getlista():
    with RutaBD() as rbd:
        return jsonify(rbd.obtener_rutas())

@app.route('/rutas/rutabd/getRuta/<fecharuta>', methods=["POST"])
@login_required
def rutabd_getruta(fecharuta):
    with RutaBD() as rbd:
        return jsonify(rbd.obtener_ruta(fecharuta))

@app.route('/rutas/rutabd/getTotales/<fecharuta>', methods=["POST"])
@login_required
def rutabd_gettotales(fecharuta):
    with RutaBD() as rbd:
        return jsonify({"totales":rbd.obtener_totales_ruta(fecharuta)})

@app.route('/rutas/rutabd/marcarStatus', methods=["POST"])
@login_required
def rutabd_marcarstatus():
    ubicacion = request.args.get('ubicacion')
    status = request.args.get('status')
    with RutaBD() as rbd:
        rbd.marcar_status(ubicacion,status)
        fecha = rbd.getDato(fila=int(ubicacion),columna="fecha")
        id_cliente = rbd.getDato(fila=int(ubicacion),columna="id")
    if status == "aruta":
        with Inventario() as inv:
            inv.reversa_stock(fecha, id_cliente)
    return jsonify({"message":"ok"}), 200

@app.route('/rutas/rutabd/buscar')
@login_required
def rutabd_busqueda():
    busqueda = request.args.get("search")
    filtro = request.args.get("filtro")
    sindatos = {"sindatos":"No se encontraron clientes coincidentes con esa busqueda"}
    resultados = sindatos
    if len(busqueda) > 1:
        with RutaBD() as rbd:
            resultados = rbd.buscar_datos(
                busqueda=busqueda,
                filtro=filtro
                )
            resultados = resultados if resultados else sindatos
    return jsonify(resultados)

@app.route('/rutas/rutabd/modregistro/<idy>', methods=["GET","PUT"])
@login_required
def rutabd_mod_registro(idy):
    if request.method == "GET":
        with RutaBD() as r:
            data = r.mapdatos(fila=int(idy),columnas=r.hoja_actual["rutabd_busquedas"], idy=True)
            data = privilegios(sesion.get_usuario(request.cookies.get("aut")), data)
        return render_template('rutabd_modregistro.html',datos=data)
    elif request.method == "PUT":
        datos = request.form.to_dict()
        with RutaBD() as rbd:
            try:
                for campo in datos.keys():
                    rbd.putDato(
                            fila=int(idy),
                            columna=campo,
                            dato=datos[campo]
                            )
            except Exception as e:
                cimprime(titulo="Error en servidor",error=e)
                return jsonify({"resultado":False})
            else:
                return jsonify({"resultado":True})


# ------------------- INVENTARIO ----------------------------
@app.route('/inventario')
@login_required
def inventario():
    datos = privilegios(sesion.get_usuario(request.cookies.get("aut")))
    datos["tituloPagina"] = "Inventario de insumos en stock"
    return render_template('inventario.html', datos=datos)

@app.route('/inventario/getstock')
@login_required
def inventario_getstock():
    with Inventario() as inv:
        return jsonify(inv.get_stock())

@app.route('/inventario/modifica', methods=['POST','GET'])
@login_required
def inventario_modifica():
    if request.method == "POST":
        cantidad = request.args.get("cant")
        columna = request.args.get("col")
        with Inventario() as inv:
            return jsonify(inv.modifica_stock(
                cantidad=cantidad,
                columna=columna
                ))
    elif request.method == "GET":
        datos = privilegios(sesion.get_usuario(request.cookies.get("aut")))
        datos["tituloPagina"] = "Modificacion de inventario"
        return render_template('inventario_mod.html', datos=datos)

@app.route('/uploadRuta', methods=['POST','GET'])
@login_required
def uploadRuta() -> render_template:
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
                with RutaImportar(archivo_cargado) as ri:
                    datos = ri.extrae_ruta()
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
                        with Clientes() as cl:
                            retorno_id = cl.nuevo_cliente(mapdatos,datoeval="cliente",retornoid=True)
                        datos["datos"][datos["datos"].index(fila)][idcliente] = retorno_id
                with RutaBD() as rbd:
                    if rbd.importar_ruta(datos):
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
        return render_template('uploadruta.html', datos=datos)

if __name__ == '__main__':
    app.run(debug=True)

