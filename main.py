from flask import Flask, redirect, url_for, request, render_template
from conectorbd import conectorbd
from coder.codexpy2 import codexpy2
from helpers import verificatoken, empaquetador, comprueba_usuario, mensajes

app = Flask(__name__)
coder = codexpy2()

@app.route('/')
def index() -> redirect:
  return redirect(url_for('inicio' if verificatoken(coder, request) else 'login'))
  
@app.route('/inicio')
def inicio() -> render_template:
     if not verificatoken(coder, request):
          return redirect(url_for("login"))
     datos = empaquetador(coder, request)
     return render_template("index.html", datos=datos)

@app.route('/login')
def login() -> render_template:
   datos = empaquetador(coder, request, "login")
   return render_template("autorizador.html", datos=datos)

@app.route('/autorizador', methods=['POST'])
def autorizador() -> redirect:
  if comprueba_usuario(coder, request):
       return redirect(url_for('inicio', aut=coder.getCurrentToken()))
  return redirect(url_for('login',alerta=mensajes.USUARIO_INCORRECTO.value))
  
@app.route('/accion', methods=['POST','GET'])
def accion() -> render_template:
     if not verificatoken(coder, request):
          return redirect(url_for("login"))
     datos = empaquetador(coder, request, "accionesBotones")
     return render_template(datos["pagina"], datos=datos)

@app.route('/clientes', methods=['POST'])
def clientes() -> render_template:
     if not verificatoken(coder, request):
          return redirect(url_for("login"))
     datos = empaquetador(coder,request,"clientes")
     if "redirect" in datos:
          return redirect(url_for(datos["redirect"],aut=datos["aut"]))
     return render_template(datos["pagina"], datos=datos)

@app.route('/nuevoCliente', methods=['POST','GET'])
def nuevoCliente() -> render_template:
     if not verificatoken(coder, request):
          return redirect(url_for("login"))
     datos = empaquetador(coder,request,"nuevocliente")
     return render_template(datos["pagina"], datos=datos)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
