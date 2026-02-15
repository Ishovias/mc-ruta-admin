__all__ = ['SessionSingleton']

import handlers
import secrets
from coder.codexpy2 import Codexpy2

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
        with handlers.Usuariosbd() as userbd:
            result = userbd.comprueba_usuario(usuario,passwd)
            if result:
                token = secrets.token_urlsafe(32)
                self.__usr[token] = usuario
                userbd.registra_token(usuario=usuario,token=token)
                return token
        return result

    def cierra_sesion(self, token: str) -> None:
        with handlers.Usuariosbd() as ubd:
            ubd.elimina_token(token)
        del(self.__usr[token])

    def get_autenticado(self, token: str) -> bool:
        if token in self.__usr:
            return True
        else: # Comprobacion token largo plazo
            with handlers.Usuariosbd() as ubd:
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
        with handlers.Usuariosbd() as ubd:
            ubd.elimina_token(token)
        if self.__usr.get(token):
            del(self.__usr[token])

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass
