from flask import Flask, redirect, url_for, request, render_template
from coder.codexpy2 import codexpy2
from helpers import lista_rutas, SessionSingleton, verificatoken, empaquetador, mensajes

app = Flask(__name__)
coder = codexpy2()
sesion = SessionSingleton()

               
@app.route('/', methods=['GET','POST'])
def index() -> render_template:
     
     destino = "index"
     
     if request.method == "POST":
          # print(request.form)
          for direccion in lista_rutas:
               for item in lista_rutas[direccion]:
                    if item in request.form:
                         destino = direccion
                         break
          if "cierrasesion" in request.form:
               if sesion.getAutenticado(request):
                    sesion.cierraSesion(request)
               
     datos = empaquetador(coder, request, destino)
     
     if not sesion.getAutenticado(request):
          datos["pagina"] = "autorizador.html"
     
     return render_template(datos["pagina"], datos=datos)

if __name__ == '__main__':
     app.run(debug=True,host='0.0.0.0')
