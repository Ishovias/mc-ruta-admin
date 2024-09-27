from bd.repository import bdmediclean
import params

class Usuariosbd(bdmediclean):

    def __init__(self) -> None:
        super().__init__(params.USUARIO)

    def comprueba_usuario(self, nombre: str, contrasena: str) -> bool:
        dnombre = super().buscadato(self.hoja_actual["filainicial"],1,nombre,exacto=True)
        dcontrasena = super().buscadato(self.hoja_actual["filainicial"],2,contrasena,exacto=True)
        if dnombre != None and dcontrasena != None:
            resultado = True
        else:
            resultado = False
        return resultado
    
    def elimina_token(self, token: str) -> bool:
        ubicacionUsuario = super().busca_ubicacion(dato=token,columna="token")
        if ubicacionUsuario:
            return super().putDato(dato="",fila=ubicacionUsuario,columna="token")
        return False
        
    def token_registrado(self, usuario: str) -> bool:
        ubicacionUsuario = super().busca_ubicacion(dato=usuario,columna="usuario")
        return super().getDato(fila=ubicacionUsuario,columna="token")
    
    def token_existente(self, tokenDado: str) -> str: # nuevo metodo
        ubicacion = super().busca_ubicacion(dato=tokenDado,columna="token") 
        if ubicacion:
            return super().getDato(fila=ubicacion,columna="usuario")
        return None
        
    def registra_token(self, usuario: str, token: str) -> bool:
        ubicacionUsuario = super().busca_ubicacion(dato=usuario,columna="usuario")
        return super().putDato(dato=token,fila=ubicacionUsuario,columna="token")