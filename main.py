from flask import Flask, redirect, request, render_template, url_for
from coder.codexpy2 import codexpy2
from empaquetadores.pack_clientes import empaquetador_clientes
from empaquetadores.pack_rutas import empaquetador_registros_rutas, empaquetador_rutaactual
from empaquetadores.pack_admin import empaquetador_usersactives
from empaquetadores.pack_todo import empaquetador_todo
from helpers import SessionSingleton, empaquetador_login

app = Flask(__name__)
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
     
if __name__ == '__main__':
     app.run(debug=True,host='0.0.0.0')
