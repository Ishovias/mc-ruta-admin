from flask import Flask, redirect, request, render_template, url_for
from coder.codexpy2 import codexpy2
from empaquetadores.pack_clientes import empaquetador_clientes
from empaquetadores.pack_rutas import empaquetador_registros_rutas, empaquetador_rutaactual, empaquetador_carga_ruta
from empaquetadores.pack_admin import empaquetador_usersactives
from empaquetadores.pack_todo import empaquetador_todo
from empaquetadores.pack_st_inicio import pack_st_login, pack_st_index
from helpers import SessionSingleton, empaquetador_codex1, empaquetador_codex2, empaquetador_login
from params import RUTA_IMPORTACION, EXTENSIONES_PERMITDAS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = RUTA_IMPORTACION
coder = codexpy2()
sesion = SessionSingleton()

@app.route('/', methods=['GET','POST'])
def index() -> render_template:
     if sesion.getAutenticado(request):
          datos = {
               "bienvenida":f"Bienvenido {sesion.getUsuario(request)}, escoge una accion",
               "aut":request.args.get("aut"),
               "usuario":sesion.getUsuario(request)
          }
          return render_template("index.html", datos=datos)
     return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login() -> render_template:
     if request.method == 'POST':
          if not sesion.getAutenticado(request):
               datos = empaquetador_login(coder, request)
               if "pagina" in datos:
                    return render_template(datos["pagina"], datos=datos)
          return redirect(url_for('index', aut=datos["aut"]))
     else:
          if sesion.getAutenticado(request):
               return redirect(url_for('index'))
          return render_template("autorizador.html", datos={"alerta":"Debes iniciar sesion primeramente"})

@app.route('/clientes', methods=['POST'])
def clientes() -> render_template:
     if not sesion.getAutenticado(request):
          return redirect(url_for('login'))
     datos = empaquetador_clientes(request)
     return render_template(datos["pagina"], datos=datos)

@app.route('/rutaactual', methods=['POST'])
def rutaactual() -> render_template:
     if not sesion.getAutenticado(request):
          return redirect(url_for('login'))
     datos = empaquetador_rutaactual(request)
     return render_template(datos["pagina"], datos=datos)

@app.route('/rutas', methods=['POST'])
def rutas() -> render_template:
     if not sesion.getAutenticado(request):
          return redirect(url_for('login'))
     datos = empaquetador_registros_rutas(request)
     return render_template(datos["pagina"], datos=datos)

@app.route('/logout', methods=['POST'])
def logout() -> render_template:
     alerta = "Sesion ya cerrada, debes iniciar sesion nuevamente"
     if sesion.getAutenticado(request):
          alerta = f"Sesion de usuario {sesion.getUsuario(request)} cerrada"
          sesion.cierraSesion(request)
     datos = {"alerta":alerta}
     return render_template('autorizador.html', datos=datos)

@app.route('/todo', methods=['POST'])
def todo() -> render_template:
     if not sesion.getAutenticado(request):
          return redirect(url_for('login'))
     datos = empaquetador_todo(request)
     return render_template(datos["pagina"], datos=datos)

@app.route('/usersactives', methods=['POST'])
def usersactives() -> render_template:
     if not sesion.getAutenticado(request):
          return redirect(url_for('login'))
     datos = empaquetador_usersactives(request)
     return render_template(datos["pagina"], datos=datos)

@app.route('/codex1', methods=['POST'])
def codex1() -> render_template:
     if not sesion.getAutenticado(request):
          return redirect(url_for('login'))
     datos = empaquetador_codex1(request)
     return render_template(datos["pagina"], datos=datos)

@app.route('/codex2', methods=['POST'])
def codex2() -> render_template:
     if not sesion.getAutenticado(request):
          return redirect(url_for('login'))
     datos = empaquetador_codex2(coder, request)
     return render_template(datos["pagina"], datos=datos)

@app.route('/uploadRuta', methods=['POST'])
def uploadRuta() -> render_template:
     if not sesion.getAutenticado(request):
          return redirect(url_for('login'))
     datos = empaquetador_carga_ruta(request,app)
     return render_template(datos["pagina"], datos=datos)

@app.route('/sublitote/login', methods=['GET','POST'])
def sublitote_login() -> render_template:
     if request.method == 'POST':
          if not sesion.getAutenticado(request):
               datos = pack_st_login(coder, request)
               if "pagina" in datos:
                    return render_template(datos["pagina"], datos=datos)
          return redirect(url_for('sublitote', aut=datos["aut"]))
     else:
          if sesion.getAutenticado(request):
               return redirect(url_for('sublitote'))
          return render_template("st_autorizador.html", datos={"alerta":"Debes iniciar sesion primeramente"})

@app.route('/sublitote', methods=['GET','POST'])
def sublitote() -> render_template:
     if not sesion.getAutenticado(request):
          return redirect(url_for('sublitote_login'))
     datos = pack_st_index(request)
     return render_template(datos["pagina"], datos=datos)

@app.route('/productos', methods=['GET','POST'])
def productos() -> render_template:
     if not sesion.getAutenticado(request):
          return redirect(url_for('sublitote_login'))
     datos = pack_st(request)
     return render_template(datos["pagina"], datos=datos)

@app.route('/cotizacion', methods=['GET','POST'])
def cotizacion() -> render_template:
     if not sesion.getAutenticado(request):
          return redirect(url_for('sublitote_login'))
     datos = pack_st(request, coder)
     return render_template(datos["pagina"], datos=datos)

if __name__ == '__main__':
     app.run(debug=True,host='0.0.0.0')
