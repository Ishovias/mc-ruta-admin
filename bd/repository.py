from openpyxl import load_workbook
from cimprime import cimprime
import params

class bdmediclean:

     def __init__(self, hoja: str, otrolibro: str=None, hojadefault: bool=False) -> None:
          if otrolibro:
               self.bd = load_workbook(otrolibro,read_only=False)
               self.libroPorGuardar = otrolibro
          else:   
               self.bd = load_workbook(params.LIBRODATOS,read_only=False)
               self.libroPorGuardar = params.LIBRODATOS
          self.hoja_actual = hoja
          self.hojabd = self.bd[self.hoja_actual["nombrehoja"]]
          self.maxfilas = self.contarfilas()
          self.datosPorGuardar = False
     
     def __enter__(self) -> object:
          return self
     
     def getmaxfilas(self) -> int:
          self.maxfilas = self.contarfilas()
          return self.maxfilas
     
     def contarfilas(self) -> int:
          filas = self.hoja_actual["filainicial"]
          while True:
               celda = self.hojabd.cell(row=filas,column=1)
               if celda.value != None:
                    filas += 1
               else:
                    return filas - 1
     
     def eliminarContenidos(self) -> None:
          filainicio = self.hoja_actual["filainicial"]
          filatermino = self.maxfilas + 1
          for fila in range(filainicio,filatermino,1):
               for columna in self.hoja_actual["columnas_todas"]:
                    celda = self.hojabd.cell(row=fila,column=columna)
                    celda.value = None
          self.datosPorGuardar = True
     
     def buscafila(self, columna: int=1) -> int:
          filainicio = self.hoja_actual["filainicial"]
          filatermino = self.maxfilas + 2
          if type(columna) == str:
               columna = self.hoja_actual["columnas"][columna]["num"]
          for fila in range(filainicio,filatermino,1):
               celda = self.hojabd.cell(row=fila,column=columna)
               if celda.value == None:
                    return fila
     
     def buscadato(self, dato: str, filainicio: int=None, columna: str=None, exacto: bool=False, filtropuntuacion: bool=False, buscartodo: bool=False) -> int:
          def buscador(filainicio: int) -> int:
               maxfilas = self.maxfilas + 1
               fila = filainicio
               for fila in range(filainicio, maxfilas, 1):
                celda = self.hojabd.cell(row=fila,column=columna)
                try:
                    valorcelda = str(celda.value) if exacto else str(celda.value).lower()
                    datob = dato if exacto else dato.lower()
                except:
                    valorcelda = str(celda.value)
                    datob = dato
                finally:
                    if filtropuntuacion:
                        datob = datob.replace(".","").replace(" ","").replace("-","")
                        valorcelda = valorcelda.replace(".","").replace(" ","").replace("-","")
                    if datob == valorcelda:
                        return fila
                    else:
                        fila += 1
               else:
                fila = None
               return fila      
          if buscartodo:
            filas = []
            while(filainicio <= self.maxfilas):
                hallado = buscador(filainicio)
                if hallado:
                    filas.append(hallado)
                else:
                    break
                filainicio = hallado + 1
            return filas
          else:
            return buscador(filainicio)
     
     def buscapartedato(self, filainicio: int=None, columna: int=None, dato: str=None) -> list:
     
        if not filainicio:
            filainicio = self.hoja_actual["filainicial"]
        if not columna:
            columna = 1
        if not dato:
            raise ValueError("No se ha ingresado un dato a buscar")
     
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
            return None
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
     
     def listar(self, filainicial: int=None, columnas: list=None, encabezados: int=None, retornostr: bool=False, solodatos_list: bool=False) -> map:
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
                    if retornostr:
                        datafile.append(str(dato.value))
                    else:
                        datafile.append(dato.value)
                resultados["datos"].append(datafile)
        if solodatos_list:
            return resultados["datos"]
        
        # Extraccion de encabezados
        resultados["encabezados"] = []
        for campo in columnas:
            dato = self.hojabd.cell(row=encabezados, column=campo)
            resultados["encabezados"].append(dato.value)
            
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
        except Exception as e:
            print(e)
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
        
     def insertafila(self, filainsercion: int) -> None:
        self.hojabd.insert_rows(filainsercion)
        self.datosPorGuardar = True
     
     def idActual(self, columna: str) -> int:
        for fila in range(self.hoja_actual["filainicial"],self.maxfilas,1):
            col = self.hoja_actual["columnas"][columna]
            celda = self.hojabd.cell(row=fila,column=col)
            celdaAnterior = self.hojabd.cell(row=(fila-1),column=col)
            encabezados = self.getDato(
                 fila=self.hoja_actual["encabezados"],
                 columnas=self.hoja_actual["columnas"]["todas"]
                 )
            if celda.value == None:
                if celdaAnterior.value in encabezados:
                    return 1
                else:
                    return int(celdaAnterior.value)+1
     
     def extraefila(self, fila: int, columna: str=None, columnas: list=None, retornostr: bool=False) -> list:
        if columna and type(columna) == str:
            ListaColumnas = self.hoja_actual["columnas"][columna]
            if type(ListaColumnas) == list:
                columnas = ListaColumnas
            else:
                columnas = [ListaColumnas]
        elif columna and type(columna) == int:
            columnas = [columna]
        elif columna and type(columna) == list:
            columnas = columna
        elif columnas != None:
            pass
        
        datos = []
     
        for column in columnas:
            celda = self.hojabd.cell(row=fila, column=column)
            if retornostr:
                datos.append(str(celda.value))
            else:
                datos.append(celda.value)
     
        return datos
     
     def getDato(self, fila: int=None, columna: str=None, columnas: list=None, identificador: str=None, retornostr: bool=False) -> bool:
        if identificador:
            row = self.hoja_actual[identificador]["fila"]
            column = self.hoja_actual[identificador]["columna"]
        else:
            row = fila
            if columna:
                column = self.hoja_actual["columnas"][columna]
        
        if columnas:
            if row:
                if retornostr:
                    datos = self.extraefila(fila=row,columnas=columnas,retornostr=True)
                else:
                    datos = self.extraefila(fila=row,columnas=columnas)
                return datos
            return None
        else:
            if row:
                if retornostr:
                    datos = self.extraefila(fila=row,columna=column,retornostr=True)
                else:
                    datos = self.extraefila(fila=row,columna=column)
                return datos[0]
            return None
     
     
     def guardar(self) -> None:
        try:
            self.bd.save(self.libroPorGuardar)
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

