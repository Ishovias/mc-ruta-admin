## Pequeña aplicacion para convertir palabras en base a
## juego infantil llamado CLAVE MURCIELAGO con modificaciones
## programado por isaias beroiza (fase de aprendizaje)
## util para hacer una llave maestra de combinaciones para
## generar contraseñas complejas en base a contraseñas simples
## reciente adaptacion hecha el 28 de jun, 2024 se transforma a clase simple


class codexpy:

        def __init__(self) -> None:
                self.cod = list("abcdefghijklmnopqrstuvwxyz1234567890@#$")

        def procesa(self, frase: str) -> str:
                cod_a = self.cod
                clave = list(frase)
                ctd_letras = len(clave)
                cod_b = list(reversed(cod_a))
                largo_cod = len(cod_a)
                for l in range(ctd_letras):
                        for a in range(largo_cod):
                                if  clave[l] == cod_a[a]:
                                        clave[l] = cod_b[a]
                                        break
                resultado = ("".join(clave))
                return resultado
