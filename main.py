from flask import Flask, redirect, request, render_template, url_for
from coder.codexpy2 import codexpy2
from empaquetadores.pack_clientes import empaquetador_clientes
from empaquetadores.pack_rutas import empaquetador_registros_rutas, empaquetador_rutaactual
from helpers import SessionSingleton, empaquetador_login

app = Flask(__name__)
coder = codexpy2()
sesion = SessionSingleton()

@app.route('/', methods=['GET','POST'])
def index() -> render_template:
     if sesion.getAutenticado(request):
          datos = {"bienvenida":f"Bienvenido {sesion.getUsuario(request)}, escoge una accion"}
          return render_template("index.html", datos=datos)
     return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login() -> render_template:
     
     if request.method == 'POST':
          if not sesion.getAutenticado(request):
               datos = empaquetador_login(coder, request)
               if "pagina" in datos:
                    return render_template(datos["pagina"], datos=datos)
          return redirect(url_for('index'))
     else:
          if sesion.getAutenticado(request):
               return redirect(url_for('index'))
          return render_template("autorizador.html")

@app.route('/clientes', methods=['POST'])
def clientes() -> render_template:
     datos = empaquetador_clientes(request)
     return render_template(datos["pagina"], datos=datos)

@app.route('/rutaactual', methods=['POST'])
def rutaactual() -> render_template:
     datos = empaquetador_rutaactual(request)
     return render_template(datos["pagina"], datos=datos)

@app.route('/rutas', methods=['POST'])
def rutas() -> render_template:
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

if __name__ == '__main__':
     app.run(debug=True,host='0.0.0.0')
