from bd.repository import bdmediclean
from cimprime import cimprime
import params

class RutaActual(bdmediclean):

    def __init__(self) -> None:
        super().__init__(params.RUTA_ACTUAL, otrolibro=params.LIBRORUTA)

    def ruta_existente(self) -> bool:
        if super().getDato(
                fila=self.hoja_actual["filadatos"],
                columna="fecharuta"
                ) and super().getDato(
                        fila=self.hoja_actual["filadatos"],
                        columna="nombreruta"
                        ):
            return True
        return False

    def listar_rutaactual(self, columnas: list, idy: bool=False) -> map:
        listado = super().listar(columnas=columnas,idy=idy)
        listado["encabezados"].insert(0,"INDICE")
        indice = 1
        for fila in listado["datos"]:
            fila.insert(0,indice)
            indice += 1
        return listado

    def nueva_ruta(self, fecha: str, ruta: str) -> bool:
        filadatos = self.hoja_actual["filadatos"]
        for dato, columna in [(fecha,"fecharuta"),(ruta,"nombreruta"),("0","realizado"),("0","pospuesto")]:
            super().putDato(
                    dato=dato,
                    fila=filadatos,
                    columna=columna
                    )
        return True

    def id_ruta(self) -> int:
        return int(self.maxfilas) - int(self.hoja_actual["filainicial"])

    def getFechaRuta(self) -> str:
        return super().getDato(identificador="fecharuta")

    def agregar_a_ruta(self, datos: map) -> bool:
        cliente_existente = super().buscadato(
                dato=datos["cliente"]["dato"],
                columna="cliente",
                exacto=True
                )
        rut_existente = super().buscadato(
                dato=datos["rut"]["dato"],
                columna="rut",
                exacto=True
                )
        if cliente_existente or rut_existente:
            return False
        ubicacion = super().buscafila()
        datos["fecha"] = {"dato":super().getDato(
                fila=self.hoja_actual["filadatos"],
                columna="fecharuta"
                )}
        datos["id_ruta"] = {"dato":self.id_ruta() + 2}

        for dato in self.hoja_actual["ncolumnas_todas"]:
            super().putDato(
                    dato=datos[dato]["dato"],
                    fila=ubicacion,
                    columna=dato
                    )
        return True

    def verifica_ruta_completa(self) -> int:
        datos = super().listar(solodatos=True, columnas=["otro"])
        if datos == []:
            return 0
        for dato in datos:
            if "DEUDA" in dato[0] or "deuda" in dato[0] or "Deuda" in dato[0]:
                continue
            else:
                return None
        else:
            return len(datos)

    def importar(self, datos: map) -> bool:
        for columna in ["fecharuta","nombreruta"]:
            super().putDato(
                    dato=datos[columna],
                    fila=self.hoja_actual["filadatos"],
                    columna=columna
                    )
        columnas = datos["orden_columnas"]
        filalibre = super().buscafila()
        for fila in datos["datos"]:
            for dato in fila:
                super().putDato(
                        dato=dato,
                        columna=columnas[fila.index(dato)],
                        fila=filalibre
                        )
            filalibre += 1
        else:
            return True

class RutaRegistros(bdmediclean):

    def __init__(self) -> None:
        super().__init__(params.RUTAS_REGISTROS)

    def nueva_ruta(self, fecha: str, ruta: str) -> None:
        ubicacion = super().buscafila()
        for dato, columna in [(fecha,"fecharuta"),(ruta,"nombreruta"),(0,"realizado"),(0,"pospuesto")]:
            super().putDato(
                    dato=dato,
                    fila=ubicacion,
                    columna=columna
                    )

    def ubicacion_registro(self, datos: map) -> int:
        fechasruta = super().buscadato(
                dato=datos["fecharuta"],
                columna="fecharuta",
                exacto=True,
                buscartodo=True
                )
        nombresruta = super().buscadato(
                dato=datos["nombreruta"],
                columna="nombreruta",
                exacto=True,
                buscartodo=True
                )
        for fila_fecha in fechasruta:
            for fila_nombre in nombresruta:
                if fila_nombre == fila_fecha:
                    return fila_fecha
        return None

    def cliente_confpos(self, fila: int, confpos: str, cantidad: int=1) -> None:
        cantidad_actual = super().getDato(
                fila=fila,
                columna=confpos
                )
        # Sumar uno cliente con-pos
        super().putDato(
                dato=int(cantidad_actual) + cantidad if cantidad_actual else cantidad,
                fila=fila,
                columna=confpos
                )

    def _busca_existente(self, datos: map) -> bool:
        fecharuta = datos["fecharuta"]
        nombreruta = datos["nombreruta"]
        ubicaciones_fecharuta = super().buscadato(
                dato=fecharuta,
                columna="fecharuta",
                buscartodo=True
                )
        ubicaciones_nombreruta = super().buscadato(
                dato=nombreruta,
                columna="nombreruta",
                exacto=True
                )
        if not ubicaciones_nombreruta:
            return False
        elif ubicaciones_fecharuta:
            for filafecha in ubicaciones_fecharuta:
                if filafecha in ubicaciones_nombreruta:
                    return True
        else:
            return False

    def registra_importacion(self, datos: map) -> bool:
        if self._busca_existente(datos):
            return False
        for col in ["fecharuta","nombreruta"]:
            super().putDato(
                    dato=datos[col],
                    columna=col
                    )
        return True

class RutaBD(bdmediclean):

     kilosItems = {
            "farmaco":0,
            "patologico":0,
            "contaminado":0,
            "cortopunzante":0,
            "otropeligroso":0,
            "liquidorx":0
            }

     def __init__(self) -> None:
        super().__init__(params.RUTAS_BD)

     def get_status_retiro(self, ubicacion: int) -> str:
         dato = super().getDato(
                 fila=int(ubicacion),
                 columna="status"
                 )
         return dato
   
     def buscar_datos(self, busqueda: str, filtro: str, columnas: list=None) -> list:
         # Devuelve un listado con encabezados y datos al estilo repository.listar
         filas = super().buscadato(
             dato=busqueda,
             columna=filtro,
             filtropuntuacion=True,
             buscartodo=True)
         busqueda = None
         if filas:
             busqueda = super().listar(filas=filas,columnas=columnas,idy=True)
             busqueda["datos"].reverse()
         return busqueda

     def clientes_enruta(self) -> dict:
         cols_rutaactual = self.hoja_actual["rutaactual"]
         resultados = {
                 "encabezados":cols_rutaactual,
                 "datos":[["Sin datos"]]
                 }
         filas = super().buscadato(
                     dato="enruta",
                     columna="status",
                     buscartodo=True
                 )
         if filas != []:
             resultados = super().listar(
                     filas=filas,
                     columnas=cols_rutaactual,
                     idy=True
                 )
         return resultados

     def cliente_a_ruta(self, mapdatos: dict, fecha: str, nombreruta: str=None) -> bool:
         fila=super().buscafila()
         mapdatos["fecha"] = {"dato":fecha}
         if nombreruta:
             mapdatos["ruta"] = {"dato":nombreruta}
             cimprime(nombreruta=mapdatos["ruta"])
         else:
             fila_nombreruta = super().buscadato(
                     dato=fecha,
                     columna="fecha",
                     )
             mapdatos["ruta"] = {"dato":super().getDato(
                 fila=fila_nombreruta,
                 columna="ruta"
                 )}
         mapdatos["id_ruta"] = {"dato":len(super().buscadato(
                 dato=fecha,
                 columna="fecha",
                 buscartodo=True
                 )) + 1}
         columnas_insercion = self.hoja_actual["rutaactual"].copy()
         columnas_insercion.append("ruta")
         for col in columnas_insercion:
             super().putDato(
                     fila=fila,
                     columna=col,
                     dato=mapdatos[col]["dato"]
                     )
             super().putDato(
                     fila=fila,
                     columna="status",
                     dato="enruta"
                     )
         else:
             return True
         return False

     def marcar_status(self, ubicacion: str, status: str) -> bool:
         try:
             super().putDato(
                     fila=int(ubicacion),
                     columna="status",
                     dato=status
                     )
         except:
             return False
         else:
             return True

     def cliente_confpos(self, ubicacion: str, observaciones: str, accion: str) -> str:
         super().putDato(
                 fila=int(ubicacion),
                 columna="status",
                 dato=accion
                 )
         super().putDato(
                 fila=int(ubicacion),
                 columna="detalleretiro",
                 dato=observaciones
                 )
         if accion == "REALIZADO":
             try:
                 data_stock = self.obsdecoder(
                         observacion=observaciones,
                         fila=int(ubicacion)
                         )
             except:
                 print("Error al intentar decodificar observacion, descartando")
             else:
                 for col in ["fecha","id"]:
                     data_stock[col] = super().getDato(
                             fila=int(ubicacion),
                             columna=col
                             )
                 return data_stock

     def obtener_rutas(self, filainicial: int=None) -> list:
         rutas = []
         filainicio = self.hoja_actual["filainicial"] if not filainicial else filainicial
         for fila in range(filainicio, self.maxfilas + 1, 1):
             dato = super().getDato(
                     fila=fila,
                     columna="fecha"
                     )
             if not dato:
                 break
             dato_siguiente = super().getDato(
                     fila=fila+1,
                     columna="fecha"
                     )
             if dato != dato_siguiente:
                 rutas.append([
                     dato,
                     super().getDato(
                     fila=fila-1,
                     columna="ruta"
                     )])
         rutas.reverse()
         return rutas

     def obtener_ruta(self, fecharuta: str) -> dict:
         filas = super().buscadato(
                 dato=fecharuta,
                 columna="fecha",
                 buscartodo=True
                 )
         columnas_mostrar = self.hoja_actual["rutaactual"].copy()
         columnas_mostrar.append("status")
         columnas_mostrar.append("detalleretiro")
         return super().listar(
                 filas=filas,
                 columnas=columnas_mostrar,
                 idy=True
                 )

     def obtener_nombre_ruta(self, fecharuta: str) -> str:
         fila = super().buscadato(
                     dato=fecharuta,
                     columna="fecha"
                     )
         if fila:
             return super().getDato(
                     fila=fila,
                     columna="ruta"
                     )
         return None

     def obtener_totales_ruta(self, fecharuta: str) -> list:
         resultados = {}
         filas = super().buscadato(
                 dato=fecharuta,
                 columna="fecha",
                 buscartodo=True
                 )
         items_kilos = self.hoja_actual["kgcols"]
         items_insumos = self.hoja_actual["itemscols"]
         items = items_kilos + items_insumos
         for item in items:
             resultados[item] = [self.hoja_actual["columnas"][item]["encabezado"],0]
             for fila in filas:
                 data = super().getDato(
                         fila=fila,
                         columna=item
                         )
                 if data:
                     resultados[item][1] += super().getDato(
                             fila=fila,
                             columna=item
                             )
         respuesta = []
         for item in resultados.keys():
             if resultados[item][1] > 0:
                 respuesta.append(resultados[item])
         return respuesta

     def _obtener_rangofecha(self, fechainicio: str=None, fechafinal: str=None) -> range: 
         filainicio = super().buscadato(dato=str(fechainicio),columna="fecha")
         if not fechafinal:
             fechafinal = fechainicio
         filafinal = super().buscadato(dato=str(fechafinal),columna="fecha")
         if not filainicio or not filafinal:
             return None
         maxfilas = super().getmaxfilas() + 2
         for i in range(filafinal, maxfilas,1):
             dato = super().getDato(fila=i,columna="fecha")
             if str(dato) != str(fechafinal):
                 filafinal = i
                 break
         return range(filainicio,filafinal,1)

     def obsdecoder(self, observacion: str, fila: int) -> None:
         codes = self.hoja_actual["obsdecoder"]
         data = {}
         if not observacion[-1].isspace():
             observacion = observacion + " "
         for code in codes.keys():
             if code in observacion:
                 col = codes[code]["columna"]
                 cantidad = int(observacion.split(code)[1].split(" ")[0])
                 super().putDato(
                         dato=cantidad,
                         columna=col,
                         fila=fila
                         )
                 data[col] = int(cantidad)
         return data

     def kgtotales(self, fechainicio: str=None, fechafinal: str=None, filaCliente: int=None) -> str:
         items = {
                 "farmaco":0,
                 "patologico":0,
                 "contaminado":0,
                 "cortopunzante":0,
                 "otropeligroso":0,
                 "liquidorx":0
                 }
         if fechainicio and fechafinal:
             rangodatos = self._obtener_rangofecha(fechainicio,fechafinal)
             if not rangodatos:
                 self.kilosItems = items
                 return items
             for item in items:
                 for f in rangodatos:
                     dato = super().getDato(fila=f,columna=item)
                     if dato:
                         items[item] += int(dato)
                         self.kilosItems[item] += int(dato)
         elif filaCliente:
               for item in items:
                  dato = super().getDato(fila=filaCliente,columna=item)
                  if dato:
                     items[item] += int(dato)
                     self.kilosItems[item] += int(dato)
         return items

     def resumen_insumos(self, fechainicio: str=None, fechafinal: str=None, filaCliente: int=None, retorna_map: bool=False) -> str:
         insumos = {}
         for insumo in params.INVENTARIOS["insumos_ruta"]:
             if insumo != "fecha":
                 insumos[insumo] = 0
         mensaje = ""
         if fechainicio and fechafinal:
             rangodatos = self._obtener_rangofecha(fechainicio,fechafinal)
             if not rangodatos:
                 return "Sin insumos usados"
             for insumo in insumos.keys():
                 for f in rangodatos:
                     dato = super().getDato(fila=f,columna=insumo)
                     if dato:
                         insumos[insumo] += int(dato)
         elif filaCliente:
             for insumo in insumos.keys():
                 dato = super().getDato(fila=filaCliente,columna=insumo)
                 if dato:
                     insumos[insumo] += int(dato)
         if retorna_map:
             return insumos
         for insumo in insumos.keys():
             if insumos[insumo] > 0:
                 mensaje += f"/ {insumo} = {insumos[insumo]} /"
         return mensaje

     def recuentoKgEliminar(self) -> map:
          self.eliminaKilosRegistrados()
          filasHalladas = super().buscadato(
                  filainicio=self.hoja_actual["filainicial"], 
                  columna=self.hoja_actual["columnas"]["otro"], 
                  dato="FASE_ELIMINACION", 
                  buscartodo=True
                  )
          for fila in filasHalladas:
              for elemento in self.kilosItems:
                  cantRegistrada = super().getDato(
                          fila=fila,
                          columna=elemento
                          )
                  self.kilosItems[elemento] += int(cantRegistrada) if cantRegistrada else 0
          return self.kilosItems

     def getKilos(self) -> map:
         return self.kilosItems

     def eliminaKilosRegistrados(self) -> None:
         for item in self.kilosItems:
             self.kilosItems[item] = 0

     def cuenta_insumos(self, insumos: list, ubicaciones: list) -> map:
          insumos_usados = {}
          for elemento in self.hoja_actual["encabezados_nombre"]:
              if elemento:
                  insumos_usados[elemento] = 0
          lista_elementos = list(self.hoja_actual["columnas"].keys())
          for fila in ubicaciones:
              for elemento in insumos:
                  cant = super().getDato(
                          fila=fila,
                          columna=elemento
                          )
                  nombre_elemento = self.hoja_actual["encabezados_nombre"][lista_elementos.index(elemento)+1]
                  if cant:
                      insumos_usados[nombre_elemento] += int(cant)
          for elemento in list(insumos_usados):
              if insumos_usados[elemento] == 0:
                  del insumos_usados[elemento]
          return insumos_usados

     def total_clientes_confpos(self, fechainicio: str=None, fechafinal: str=None) -> map:
          clientes = {
                  "realizado":0,
                  "pospuesto":0
                  }
          rango = self._obtener_rangofecha(fechainicio)
          if rango:
              for fila in rango:
                  dato = super().getDato(
                          fila=fila,
                          columna="status"
                          )
                  if dato == "realizado":
                      clientes["realizado"] += 1
                  elif dato == "pospuesto":
                      clientes["pospuesto"] += 1
              return clientes
          return None

     def importar_ruta(self, datos: dict) -> bool:
         ruta = datos["nombreruta"]
         columnas = datos["orden_columnas"]
         filainsert = super().buscafila()
         for fila in datos["datos"]:
             for dato in fila:
                 super().putDato(
                         dato=dato,
                         columna=columnas[fila.index(dato)],
                         fila=filainsert
                         )
             super().putDato(
                     dato=ruta,
                     fila=filainsert,
                     columna="ruta"
                     )
             super().putDato(
                     dato="enruta",
                     fila=filainsert,
                     columna="status"
                     )
             filainsert += 1
         else:
             return True

     def disposicion_final(self, ubicacion: int, status: str) -> None:
         super().putDato(
                 dato="PRE-ELIMINACION",
                 fila=int(ubicacion),
                 columna="status"
                 )
         pass

     def movpos(self, pos_a: int, pos_b: int) -> bool:
        cols = list(self.hoja_actual["columnas"].keys())
        try:
            datos_a = super().getDato(fila=pos_a,columna=cols)
            super().eliminar(pos_a)
            super().insertar_fila(pos_b)
            super().putDato(dato=datos_a,fila=pos_b,columna=cols)
        except Exception as e:
            cimprime(titulo="Error en handler RutaBD",error=e)
            return False
        else:
            return True

class RutaImportar(bdmediclean):

     def __init__(self, archivo: str) -> None:
          super().__init__(params.RUTA_ACTUAL, otrolibro=str(archivo))
          self.hoja_actual = params.RUTA_ACTUAL

     def extrae_ruta(self) -> map:
         filadatos = self.hoja_actual["filadatos"]
         columnas_datos = params.RUTAS_BD["rutaactual"].copy()
         return {
                 "fecharuta": super().getDato(
                     fila=filadatos,
                     columna="fecharuta"
                     ),
                 "nombreruta": super().getDato(
                     fila=filadatos,
                     columna="nombreruta"
                     ),
                 "datos":super().listar(
                     columnas=columnas_datos,
                     solodatos=True
                     ),
                 "orden_columnas":columnas_datos
                 }
