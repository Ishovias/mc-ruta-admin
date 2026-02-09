from datetime import datetime, timedelta
from functools import wraps
from flask import request, redirect, url_for
from cimprime import cimprime
import conector
import params


class VariablesCompartidas:
     
    __instance = None# {{{
    variables = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
     
    def put_variable(self, **variable) -> None:
        for nombre, valor in variable.items():
            self.variables[nombre] = valor
     
    def get_variable(self, variable: str) -> str:
        if type(variable) == str and variable in self.variables:
            return self.variables[variable]
        return None
          
    def del_variable(self, variable: str) -> bool:
        if variable not in self.variables:
            return False
        del(self.variables[variable])# }}}
          
# ---------------------- VERIFICATOKEN  --------------------------
def verifica_token(request: object) -> bool:
    auth_header = request.headers.get("aut")# {{{
    sesion = conector.SessionSingleton()
    aut = None
    if request.cookies:
        aut = request.cookies.get("aut")
    if auth_header:
        aut = auth_header
    if aut:
        if sesion.get_autenticado(aut):
            return True
    return False# }}}

def login_required(f):
    @wraps(f)# {{{
    def decorated_function(*args, **kwargs):
        if not verifica_token(request):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function# }}}

# ---------------------- RETORNO DE PRIVILEGIOS ----------------------

def privilegios(usuario: str, paquete: dict=None) -> map:
    for rango in ["admin","user","spectator"]:# {{{
        if usuario in params.PRIVILEGIOS[rango]["usuarios"]:
            if not paquete:
                return {
                        "privilegios":params.PRIVILEGIOS[rango]["privilegios"],
                        "rango":rango
                        }
            else:
                paquete["privilegios"] = params.PRIVILEGIOS[rango]["privilegios"]
                paquete["rango"] = rango
                return paquete# }}}


