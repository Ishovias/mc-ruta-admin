from bd.repository import bdmediclean
import params

class Usuariosbd(bdmediclean):

    def __init__(self) -> None:
        super().__init__(params.USUARIO)

    def comprueba_usuario(self, nombre: str, contrasena: str) -> bool:
        dnombre = super().buscadato(self.hoja_actual["filainicial"],1,nombre)
        dcontrasena = super().buscadato(self.hoja_actual["filainicial"],2,contrasena)
        if dnombre > 0 and dcontrasena > 0:
            resultado = True
        else:
            resultado = False
        return resultado