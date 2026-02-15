from enigmacoder.matrix import ABC, MATRIX

class EnCoder:

    def __init__(self, clave: str) -> None:
        self.abc = ABC
        self.matrix = MATRIX
        self.clave = clave
        self.largo_clave = len(clave) - 1

    def set_clave(self, palabra: str) -> None:
        self.clave = palabra

    def codifica(self, frase: str) -> str:
        frase = list(frase.lower())
        resultado = []
        index = 0
        for letra in frase:
            if letra in self.abc:
                col = self.abc.index(letra)
                fila = self.clave[index]
                resultado.append(self.matrix[fila][col])
                index += 1
            else:
                resultado.append(letra)
                index += 1
            if index > self.largo_clave:
                index = 0
        return "".join(resultado)

    def decodifica(self, frase: str) -> str:
        frase = self._listador(frase)
        print(frase)
        resultado = []
        index = -1
        for letra in frase:
            index += 1
            if index > self.largo_clave:
                index = 0
            fila = self.clave[index]
            if letra in self.matrix[fila]:
                letra_decodificada = self.matrix[fila].index(letra)
                resultado.append(self.abc[letra_decodificada])
            else:
                resultado.append(letra)
        return "".join(resultado)
    
    def _listador(self, text: str) -> list:
        text = list(text)
        textlen = len(text)
        retorno = []
        for i in range(0,textlen,2):
            retorno.append(f"{text[i]}{text[i+1]}")
        return retorno
        
if __name__ == '__main__': 
    clave = input("Ingresa una palabra clave(solo letras no numeros ni simbolos): ")
    encoder = EnCoder(clave)
    modo = "cod"
    codificado = None
    while True:
        if codificado:
            print("-"*20,"\n", "Resultado->>>  ", codificado, "\n", "-"*20)
        frase = input("Ingresa una frase o palabra a codificar: ")
        acciones = ["setclave","dec","cod","quit"]
        if frase not in acciones:
            if modo == "cod":
                codificado = encoder.codifica(frase)
            elif modo == "dec":
                codificado = encoder.decodifica(frase)
        elif frase == acciones[0]:
            clave = input("Ingresa una palabra clave(solo letras no numeros ni simbolos): ")
            encoder.set_clave(clave)
        elif frase == acciones[1]:
            modo = "dec"
            codificado = None
        elif frase == acciones[2]:
            modo = "cod"
            codificado = None
        elif frase == acciones[3]:
            print("\n\nBye!\n\n")
            break
