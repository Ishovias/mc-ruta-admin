from openpyxl import load_workbook
import params
import os

class bdmediclean:

    def __init__(self, hoja: str) -> None:
        self.bd = load_workbook(params.LIBRODATOS,read_only=False)
        self.hoja_actual = hoja
        self.hojabd = self.bd[self.hoja_actual["nombrehoja"]]
        self.maxfilas = self.contarfilas()
        self.datosPorGuardar = False
    
    def __enter__(self) -> object:
        return self

    def sethoja(self, hoja: str) -> None:
        self.hoja_actual = hoja
        self.hojabd = self.bd[self.hoja_actual["nombrehoja"]]
    
    def setmaxfilas(self) -> None:
        self.maxfilas = self.contarfilas()

    def getmaxfilas(self) -> int:
        self.maxfilas = self.contarfilas()
        return self.maxfilas

    def contarfilas(self) -> int:
        filas = 1
        while True:
            celda = self.hojabd.cell(row=filas,column=1)
            if celda.value != None:
                filas += 1
            else:
                return filas + 2

    def eliminarContenidos(self,cantidadfilas: int, filainicio: int=4) -> bool:

        completado = False
        cantidadfilas += 100

        for fila in range(filainicio,cantidadfilas,1):
            for columna in range(1,10,1):
                celda = self.hojabd.cell(row=fila,column=columna)
                celda.value = None
        else:
            completado = True
            self.datosPorGuardar = True
            return completado

    def buscafila(self, filainicio: int=None, columna: int=1) -> int:
        if not filainicio:
            filainicio = self.hoja_actual["filainicial"]
        
        filalibre = filainicio

        for fila in range(filainicio,self.maxfilas,1):
            celda = self.hojabd.cell(row=fila,column=columna)
            if celda.value == None:
                return filalibre
            else:
                filalibre += 1

    def buscadato(self, filainicio: int, columna: int, dato: str) -> int:

        fila = filainicio

        for fila in range(filainicio, self.maxfilas, 1):
            celda = self.hojabd.cell(row=fila,column=columna)
            try:
                valorcelda = str(celda.value).lower()
                datob = dato.lower()
            except:
                valorcelda = str(celda.value)
                datob = dato
            finally:
                if datob == valorcelda:
                    return fila
                else:
                    fila += 1
        else:
            fila = None
        return fila
        
    def buscapartedato(self, filainicio:int, columna: int, dato: str) -> list:

        fila = filainicio
        
        filas = []
        
        for fila in range(filainicio, self.maxfilas, 1):
            celda = self.hojabd.cell(row=fila,column=columna)
            valorcelda = str(celda.value)
            if dato.lower() in valorcelda.lower():
                filas.append(fila)
            elif valorcelda == None:
                break
            else:
                fila += 1
                
        return filas

    def busca_datoscliente(self, nombre: str, filtro: str="cliente") -> list:
        ubicacion = self.buscadato(
            self.hoja_actual["filainicial"],
            self.hoja_actual["columnas"][filtro],
            nombre
            )
        if ubicacion == None:
            return 0
        datos = self.extraefila(
            fila=ubicacion,
            columna="todas"
            )
        return datos
    
    def busca_ubicacion(self, dato: str=None, columna: str="cliente", filainicio: str="filainicial") -> int:
        column = self.hoja_actual["columnas"][columna]
        if type(filainicio) == str:
            filainicial = self.hoja_actual[filainicio]
        else:
            filainicial = filainicio
        if not dato:
            fila = self.buscafila(filainicial,column)
        else:
            fila = self.buscadato(filainicial,column,dato)
        return fila


    def listar(self, filainicial: int=None, columnas: list=None, encabezados: int=None) -> map:
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
        if not filainicial:
            filainicial = self.hoja_actual["filainicial"]
        if not columnas:
            columnas = self.hoja_actual["columnas"]["todas"]
        if not encabezados:
            encabezados = self.hoja_actual["encabezados"]
        
        resultados = {}

        # Extraccion de encabezados
        resultados["encabezados"] = []
        for campo in columnas:
            dato = self.hojabd.cell(row=encabezados, column=campo)
            resultados["encabezados"].append(dato.value)

        # Extraccion de datos "filas"
        resultados["datos"] = []
        for fila in range(filainicial,self.maxfilas,1):
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
        self.datosPorGuardar = True

    def putDato(self, dato: str=None, datos: list=None, fila: int=None, columna: str=None, identificador: str=None) -> bool:
        if identificador:
            row = self.hoja_actual[identificador]["fila"]
            column = self.hoja_actual[identificador]["columna"]
        else:
            row = fila
            column = self.hoja_actual["columnas"][columna]
        try:
            if datos:
                    self.ingresador(row,datos,column)
            else:
                    self.ingresador(row,[dato],column)
        except:
            return False
        else:
            self.datosPorGuardar = True
            return True


    def ingresador_columnas(self, fila: int, datos: list, columnas: list) -> None:
        
        columna = 0
        for dato in datos:
            celdaDato = self.hojabd.cell(row=fila,column=columnas[columna])
            celdaDato.value = dato
            columna += 1
        self.datosPorGuardar = True

    def eliminar(self, fila: int) -> None:        
        self.hojabd.delete_rows(fila)
        self.datosPorGuardar = True

    def idActual(self, filainicial: int, columna: int, encabezado: str) -> int:
        for fila in range(filainicial,self.maxfilas,1):
            celda = self.hojabd.cell(row=fila,column=columna)
            celdaAnterior = self.hojabd.cell(row=(fila-1),column=columna)
            if celda.value == None:
                if celdaAnterior.value == encabezado:
                    return 1
                else:
                    return int(celdaAnterior.value)+1

    def extraefila(self, fila: int, columna: str=None, columnas: list=None) -> list:
        if type(columna) == str and columna != None:
            ListaColumnas = self.hoja_actual["columnas"][columna]
            if type(ListaColumnas) == list:
                columnas = ListaColumnas
            else:
                columnas = [ListaColumnas]
        elif type(columna) == int and columna != None:
            columnas = [columna]
        elif columnas != None:
            pass
        
        datos = []

        for column in columnas:
            celda = self.hojabd.cell(row=fila, column=column)
            datos.append(celda.value)

        return datos

    def getDato(self, fila: int=None, columna: str=None, columnas: list=None, identificador: str=None) -> bool:
        if identificador:
            row = self.hoja_actual[identificador]["fila"]
            column = self.hoja_actual[identificador]["columna"]
        else:
            row = fila
            column = self.hoja_actual["columnas"][columna]
        
        if columnas:
            if row:
                 datos = self.extraefila(fila=row,columnas=columnas)
                 return datos
            return None
        else:
            if row:
               datos = self.extraefila(fila=row,columna=column)
               return datos[0]
            return None


    def guardar(self) -> None:
        try:
            self.bd.save(params.LIBRODATOS)
        except:
            return False
        else:
            return True

    def cerrar(self) -> None:
        self.bd.close()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self.datosPorGuardar:
            self.guardar()
        self.cerrar()

