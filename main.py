from flask import Flask, redirect, url_for, request, render_template
from conectorbd import conectorbd
from coder.codexpy2 import codexpy2
import params
import datetime

app = Flask(__name__)
coder = codexpy2()

def autenticador(aut: str) -> map:
  datos = {}
  datos["aut"] = coder.ranToken()
  datos["ok"] = False
  if aut != None:
    token = coder.getCurrentToken()
    if aut == token:
      datos["aut"] = coder.setToken(aut)
      datos["ok"] = True
    
  return datos

@app.route('/')
def index() -> redirect:
  aut = request.args["aut"] if request.args else None
  datos = autenticador(aut)
  ok = datos["ok"]
  return redirect(url_for('inicio' if ok else 'login', aut=datos["aut"]))
  
@app.route('/inicio')
def inicio() -> render_template:
   aut = request.args["aut"] if request.args else None
   datos = autenticador(aut)
   if datos["ok"]:
    return render_template("index.html", datos=datos)
   else:
    return redirect(url_for("login"))

@app.route('/login')
def login() -> render_template:
   if request.args:
      pass
   else:
      return render_template("autorizador.html", aut=coder.ranToken())
   aut = request.args["aut"] if request.args else None
   datos = autenticador(aut)
   ok = datos["ok"]
   return render_template("index.html" if ok else "autorizador.html", aut=datos["aut"], datos=datos)
  
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
  userbd.cierra_conexion()
  return redirect(url_for('login', aut=resultado))
  
@app.route('/accion', methods=['POST','GET'])
def accion() -> render_template:
    
    if request.args:
      pass
    else:
      return redirect(url_for('login', aut=coder.ranToken()))
    
    habilitador = autenticador(request.args["aut"])
    
    if "clientes" in request.form:
      if habilitador["ok"]:
        return render_template("clientes.html", aut=habilitador["aut"], datos=habilitador)
      else:
        return redirect(url_for("login", aut=habilitador["aut"]))

@app.route('/clientes', methods=['POST'])
def clientes() -> render_template:
   aut = request.args["aut"] if request.args else None
   verifier = autenticador(aut)
   ok = verifier["ok"]
   if ok:
      datos = {"aut":verifier["aut"]}
      pass
   else:
      return redirect(url_for("login", aut=verifier["aut"]))
   
   clientesbd = conectorbd(conectorbd.hojaClientes)
   
   if "buscar" in request.form:
      nombre = request.form["nombre"]
      resultados = clientesbd.busca_cliente(nombre)
      datos["listaclientes"] = resultados
      print(">>>>>>> {resultados}")
   
   clientesbd.cierra_conexion()
   return render_template('clientes.html', datos=datos)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
