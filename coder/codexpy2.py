
## Pequeña aplicacion para convertir palabras en base a
## juego infantil llamado CLAVE MURCIELAGO con modificaciones
## programado por isaias beroiza
## util para hacer una llave maestra de combinaciones para
## generar contraseñas complejas en base a contraseñas simples
## con modificaciones que cristian riquelme aporta para codificacion doble

import os
import random

class codexpy2:

    cod_a = list("abcdefghijklmnopqrstuvwxyz1234567890@#$")
    cod_b = list("$#@0987654321zYXwvUTSRqpOnmlkjihgfedcba")
    cod_c = list("ZyxwVutsIqponmLk@#$%&?1234567abcdefghij")
    
    largotoken = 20
    
    def __init__(self) -> None:
      self.token = self.gtoken()
      
    def gtoken(self) -> str:
          pretoken = []
  
          for a in range(self.largotoken):
                caracter = random.choice(self.cod_b)
                pretoken.append(caracter)
          
          token = "".join(pretoken)
          return token

    def encripta(self, frase: str) -> str:
            encriptar = frase.lower()
            encriptando = []
            ctd_letras = len(encriptar)
            largo_cod = len(self.cod_a)
            for l in range(ctd_letras):
                    for a in range(largo_cod):
                            if encriptar[l].isspace():
                                    encriptando.append('*')
                                    encriptando.append('y')
                                    break
                            if encriptar[l] == self.cod_a[a]:
                                    encriptando.append(self.cod_b[a])
                                    encriptando.append(self.cod_c[a])
                                    break
            encriptado = "".join(encriptando)
            return encriptado

    def desencripta(self, frase: str) -> str:
            desencriptando = []
            fraselow = frase.lower()
            ctd_select = []
            ctd_letras = len(frase)/2
            ctd_letras = int(ctd_letras)
            largo_cod = len(self.cod_a)
            sel = 0
            for i in range(ctd_letras):
                    ctd_select.append(sel)
                    sel = sel+2
            for l in ctd_select:
                    for a in range(largo_cod):
                            if fraselow[l] == "*":
                                    desencriptando.append(" ")
                                    break
                            if fraselow[l] == self.cod_a[a]:
                                    desencriptando.append(self.cod_b[a])
                                    break
            desencriptado = "".join(desencriptando).lower()
            return desencriptado
    
    def setLargoToken(self, largo: int) -> None:
        self.largotoken = largo
    
    def setToken(self, actualToken: str) -> str:  
        
        if actualToken == self.token:
          token = self.gtoken()
          self.token = token
          return token
        
        else:
          return None
    
    def ranToken(self) -> str:
        return self.gtoken()
    
    def getCurrentToken(self) -> str:
      return self.token


# Main de instrucciones
def initialscreen(resultado: str="", modo: str="encriptar") -> None:
        os.system("clear")
        print ("")
        print ("+++CODIFICADOR PERSONALIZADO ISHO+++")
        print (f"Estas en modo >>> {modo.upper()}")
        print ("------------------------------------")
        print (" ")
        print (resultado)
        print (" ")
        print ("------------------------------------")
        print (" ")

if __name__ == '__main__':
    modo = "encripta"
    initialscreen(modo=modo)

    while True:
        entrada = input("Ingresa una frase --> ")

        if entrada == "quit":
            print("bye!\n\n")
            break

        elif entrada == "encripta":
            modo = entrada
            initialscreen(modo=modo)

        elif entrada == "desencripta":
            modo = entrada
            initialscreen(modo=modo)

        elif entrada == "gtoken":
              modo = entrada
              initialscreen(modo=modo)

        elif entrada != "" and entrada != "desencripta" or entrada != "encripta" or entrada != "gtoken":
            
                cod = codexpy2()
                
                if modo == "encripta":
                        parafrase = cod.encripta(entrada)
                elif modo == "desencripta":
                        parafrase = cod.desencripta(entrada)
                elif modo == "gtoken":
                        try:
                                entrada = int(entrada)
                        except:
                                print("Debes ingresar solo numeros")
                                parafrase = ""
                        else:
                                parafrase = cod.gtoken(entrada)
            
                initialscreen(parafrase,modo)
