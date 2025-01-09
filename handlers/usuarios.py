from bd.repository import bdmediclean
import params

class Usuariosbd(bdmediclean):

    def __init__(self) -> None:
        super().__init__(params.USUARIO)

    def comprueba_usuario(self, nombre: str, contrasena: str) -> bool:
        dnombre = super().buscadato(dato=nombre,columna="usuario",exacto=True)
        dcontrasena = super().buscadato(dato=contrasena,columna="contrasena",exacto=True)
        if dnombre != None and dcontrasena != None:
            resultado = True
        else:
            resultado = False
        return resultado
    
    def elimina_token(self, token: str) -> bool:
        ubicacionUsuario = super().buscadato(dato=token,columna="token")
        if ubicacionUsuario:
            super().putDato(dato="",fila=ubicacionUsuario,columna="token")
        return False
        
    def token_registrado(self, usuario: str) -> bool:
        ubicacionUsuario = super().buscadato(dato=usuario,columna="usuario")
        return super().getDato(fila=ubicacionUsuario,columna="token")
    
    def token_existente(self, tokenDado: str) -> str: # nuevo metodo
        ubicacion = super().buscadato(dato=tokenDado,columna="token") 
        if ubicacion:
            return super().getDato(fila=ubicacion,columna="usuario")
        return None
        
    def registra_token(self, usuario: str, token: str) -> bool:
        ubicacionUsuario = super().buscadato(dato=usuario,columna="usuario")
        super().putDato(dato=token,fila=ubicacionUsuario,columna="token")