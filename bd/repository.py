from openpyxl import load_workbook
import params
import os

class pysecretario:

    # Variables
    hoja_actual = ""

    def __init__(self, hoja: str) -> None:
        self.bd = load_workbook(params.LIBRODATOS,read_only=False)
        self.hoja_actual = hoja
        self.hojabd = self.bd[self.hoja_actual]
    
    def sethoja(self, hoja: str) -> None:
        self.hoja_actual = hoja
        self.hojabd = self.bd[self.hoja_actual]
    
    def contarfilas(self, filainicial: int) -> int:

        filas = 0

        for fila in range(filainicial, params.MAX_FILAS,1):
            celda = self.hojabd.cell(row=fila,column=1)
            if celda.value != None:
                filas += 1
            else:
                return filas

    def eliminarContenidos(self,cantidadfilas: int, filainicio: int=4) -> bool:

        completado = False
        cantidadfilas += 100

        for fila in range(filainicio,cantidadfilas,1):
            for columna in range(1,10,1):
                celda = self.hojabd.cell(row=fila,column=columna)
                celda.value = None
        else:
            completado = True
            return completado

    def buscafila(self, filainicio: int, columna: int=1) -> int:

        filalibre = filainicio

        for fila in range(filainicio,params.MAX_FILAS,1):
            celda = self.hojabd.cell(row=fila,column=columna)
            if celda.value == None:
                return filalibre
            else:
                filalibre += 1

    def buscadato(self, filainicio:int, columna: int, dato: str) -> int:

        fila = filainicio

        for fila in range(filainicio, params.MAX_FILAS, 1):
            celda = self.hojabd.cell(row=fila,column=columna)
            valorcelda = str(celda.value)
            if valorcelda.lower() == dato.lower():
                return fila
            else:
                fila += 1
        else:
            fila = 0
        return fila

    def listar(self, filainicial: int, columnas: list, encabezados: int) -> map:
        """Devuelve todos los datos en una hoja especifica
        o desde la fila especifica hasta el final

        Args:
            columnas (list): lista con las columnas ej. [1,2,3,4]
            de las que se extraeran los datos por cada fila especificada

            filainicio(int): numero que identifica la fila por la que se
            iniciara la extraccion de los datos.

        Returns:
            map: devuelve un map con dos llaves y sus respectivas listas de datos
            "encabezados" con una lista de los encabezados y
            "datos" con una lista de los datos por cada fila
        """        
        resultados = {}

        # Extraccion de encabezados
        resultados["encabezados"] = []
        for campo in columnas:
            dato = self.hojabd.cell(row=encabezados, column=campo)
            resultados["encabezados"].append(dato.value)

        # Extraccion de datos "filas"
        resultados["datos"] = []
        for fila in range(filainicial,params.MAX_FILAS,1):
            celda = self.hojabd.cell(row=fila, column=columnas[0])
            if celda.value == None:
                break
            else:
                datafile = []
                for campo in columnas:
                    dato = self.hojabd.cell(row=fila, column=campo)
                    datafile.append(dato.value)
                resultados["datos"].append(datafile)
        return resultados

    def ingresador(self, fila: int, datos: list, columnainicio: int) -> None:
        
        for dato in datos:
            celdaDato = self.hojabd.cell(row=fila,column=columnainicio)
            celdaDato.value = dato
            columnainicio += 1
            
    def ingresador_columnas(self, fila: int, datos: list, columnas: list) -> None:
        
        columna = 0
        for dato in datos:
            celdaDato = self.hojabd.cell(row=fila,column=columnas[columna])
            celdaDato.value = dato
            columna += 1

    def rangofechas(self, fechainicio: str, fechatermino: str) -> list:

        fechainicio = int(fechainicio)
        fechatermino = int(fechatermino)

        listafechas = []

        for i in range(fechainicio,(fechainicio + 5),1):
            listafechas.append(i)
        
        for i in range((fechainicio + 91),(fechatermino + 1),1):
            listafechas.append(i)

        return listafechas

    def reportehermano(self, hermano: str, listafechas: list) -> map:

        datos = {}

        encabezados = self.extraefila(
            params.HOJA_ACTIVIDAD["encabezados"],
            params.HOJA_ACTIVIDAD["columnas"]["todas"]
            )
        datos["encabezados"] = encabezados
        datos["datos"] = []

        for fecha in listafechas:
            filahallada = 0
            for fila in range(params.HOJA_ACTIVIDAD["filainicial"],params.MAX_FILAS,1):
                celda = self.hojabd.cell(row=fila,column=1)
                if celda.value == hermano:
                    celdahermano = self.hojabd.cell(row=fila,column=2)
                    if celdahermano.value == fecha:
                        filahallada = fila
                        break
            if filahallada > 0:
                dato = self.extraefila(
                  filahallada,
                  params.HOJA_ACTIVIDAD["columnas"]["todas"]
                  )
                datos["datos"].append(dato)
        
        if len(datos["datos"]) == 0:
            datos["datos"] = 0

        return datos

    def eliminar(self, fila: int) -> None:        
        self.hojabd.delete_rows(fila)

    def idActual(self, tipo: str) -> int:
        for fila in range(4,params.MAX_FILAS,1):
            celda = self.hojabd.cell(row=fila,column=1)
            celdaAnterior = self.hojabd.cell(row=(fila-1),column=1)
            if celda.value == None:
                if celdaAnterior.value == "CODIGO":
                    if tipo == "venta":
                        return 10000
                    if tipo == "carrito":
                        return 1
                else:
                    return int(celdaAnterior.value)+1

    def extraedatos(self, columnas: list, codigo: str) -> list:

        fila = 4

        for fila in range(4,params.MAX_FILAS,1):
            celda = self.hojabd.cell(row=fila,column=1)
            if celda.value == int(codigo):
                break
            elif celda.value == None:
                return None
            else:
                fila += 1

        datos = []
        for dato in columnas:
            celda = self.hojabd.cell(row=fila,column=dato)
            datos.append(celda.value)

        return datos

    def extraefila(self, fila: int, columnas: list) -> list:

        datos = []

        for columna in columnas:
            celda = self.hojabd.cell(row=fila, column=columna)
            datos.append(celda.value)

        return datos

    def guardar(self) -> None:
        self.bd.save(params.LIBRODATOS)

    def cerrar(self) -> None:
        self.bd.close()

if __name__ == '__main__':
    os.system("clear")
    sheetname = "Informes"
    bd = pysecretario(sheetname)
    borrado = bd.eliminarContenidos(10,2)
    if borrado:
      print(f"\n\n\nDatos borrados de la hoja {sheetname}\n\n\n")
    else:
      print(f"\n\n\nError al intentar borrar de la hoja {sheetname}\n\n\n")
      
    try:
      bd.guardar()
    except:
      print("Error en guardado del libro")
    else:
      print("Cambios guardados")
    finally:
      bd.cerrar()
