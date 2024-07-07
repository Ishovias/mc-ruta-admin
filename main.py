from flask import Flask, redirect, url_for, request, render_template
from coder.codexpy2 import codexpy2
from helpers import SessionSingleton, verificatoken, empaquetador, mensajes

app = Flask(__name__)
coder = codexpy2()
sesion = SessionSingleton()

@app.route('/', methods=['GET','POST'])
def index() -> render_template:
     
     destino = "index"
     
     if request.method == "POST":
          print(request.form)
          if "logueo" in request.form:
               destino = "login"
          elif "clientes" in request.form:
               destino = "clientes"
          elif "rutaactual" in request.form or "iniciaruta" in request.form:
               destino = "rutaactual"
          elif "rutas" in request.form:
               destino = "rutas"
          elif "codexpy" in request.form or "codpy" in request.form:
               destino = "codexpy"
          elif "codexpy2" in request.form or "codpy2" in request.form or "decodpy2" in request.form:
               destino = "codexpy2"
          
          elif "cierrasesion" in request.form:
               if sesion.getAutenticado(request):
                    sesion.cierraSesion(request)
               
     datos = empaquetador(coder, request, destino)
     
     if not sesion.getAutenticado(request):
          datos["pagina"] = "autorizador.html"
     
     return render_template(datos["pagina"], datos=datos)

if __name__ == '__main__':
     app.run(debug=True,host='0.0.0.0')
