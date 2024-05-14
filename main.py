from flask import Flask, redirect, url_for, request, render_template
from conectorbd import conectorbd
from coder.codexpy2 import codexpy2
from helpers import verificatoken, empaquetador, comprueba_usuario

app = Flask(__name__)
coder = codexpy2()

@app.route('/')
def index() -> redirect:
  return redirect(url_for('inicio' if verificatoken(coder, request) else 'login'))
  
@app.route('/inicio')
def inicio() -> render_template:
     if not verificatoken(coder, request):
          return redirect(url_for("login"))
     datos = empaquetador(coder, request, "inicio")
     return render_template("index.html", datos=datos)

@app.route('/login')
def login() -> render_template:
   datos = empaquetador(coder, request, "login")
   return render_template("autorizador.html", datos=datos)

@app.route('/autorizador', methods=['POST'])
def autorizador() -> redirect:
  if comprueba_usuario(request):
       return redirect(url_for('inicio', aut=coder.getCurrentToken()))
  return redirect(url_for('login'))
  
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
