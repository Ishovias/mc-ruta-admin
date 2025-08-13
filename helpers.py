from handlers.usuarios import Usuariosbd
from datetime import datetime
from coder.codexpy2 import Codexpy2
from functools import wraps
from flask import request, redirect, url_for
import params
import secrets

class SessionSingleton:
     
    __instance = None
    __usr = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __enter__(self) -> object:
        return self

    def iniciar_sesion(self, usuario: str, contrasena: str) -> bool:
        codex = Codexpy2()
        passwd = codex.encripta(contrasena)
        with Usuariosbd() as userbd:
            result = userbd.comprueba_usuario(usuario,passwd)
            if result:
                token = secrets.token_urlsafe(32)
                self.__usr[token] = usuario
                userbd.registra_token(usuario=usuario,token=token)
                return token
        return result
      
    def cierra_sesion(self, token: str) -> None:
        with Usuariosbd() as ubd:
            ubd.elimina_token(token)
        del(self.__usr[token])
      
    def get_autenticado(self, token: str) -> bool:
        if token in self.__usr:
            return True
        else: # Comprobacion token largo plazo
            with Usuariosbd() as ubd:
                usuario = ubd.get_usuario(token)
                if usuario:
                     self.__usr[token] = usuario
                     return True
        return False
      
    def get_usuario(self, token: str) -> str:
        if token in self.__usr:
            return self.__usr[token]
        return None

    def get_users_map(self) -> map:
        return self.__usr

    def del_user(self, token: str):
        with Usuariosbd() as ubd:
            ubd.elimina_token(token)
        if self.__usr.get(token):
            del(self.__usr[token])

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

class VariablesCompartidas:
     
    __instance = None
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
        del(self.variables[variable])
          
# ---------------------- VERIFICATOKEN  --------------------------
def verifica_token(request: object) -> bool:
    auth_header = request.headers.get("aut")
    sesion = SessionSingleton()
    aut = None
    if request.cookies:
        aut = request.cookies.get("aut")
    if auth_header:
        aut = auth_header
    if aut:
        if sesion.get_autenticado(aut):
            return True
    return False

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not verifica_token(request):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ---------------------- RETORNO DE PRIVILEGIOS ----------------------

def privilegios(usuario: str, paquete: dict=None) -> map:
    for rango in ["admin","user","spectator"]:
        if usuario in params.PRIVILEGIOS[rango]["usuarios"]:
            if not paquete:
                return {
                        "privilegios":params.PRIVILEGIOS[rango]["privilegios"],
                        "rango":rango
                        }
            else:
                paquete["privilegios"] = params.PRIVILEGIOS[rango]["privilegios"]
                paquete["rango"] = rango
                return paquete

