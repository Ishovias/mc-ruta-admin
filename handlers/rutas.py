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

        for dato in datos.keys():
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

     def registraMovimiento(self, datos: list) -> bool:
         try:
             super().ingresador(
                     super().buscafila(),
                     datos,
                     self.hoja_actual["columnas"]["fecha"]
                     )
         except Exception as e:
             print(e)
             return False
         else:
              return True

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


     def disposicion_final(self, ubicacion: int, status: str) -> None:
         super().putDato(
                 dato="PRE-ELIMINACION",
                 fila=int(ubicacion),
                 columna="status"
                 )
         pass

class RutaImportar(bdmediclean):

     def __init__(self, archivo: str) -> None:
          super().__init__(params.RUTA_ACTUAL, otrolibro=str(archivo))
          self.hoja_actual = params.RUTA_ACTUAL

     def extrae_ruta(self) -> map:
         filadatos = self.hoja_actual["filadatos"]
         columnas_datos = ["fecha","id_ruta","contrato","rut","cliente","direccion","comuna","telefono","otro","id"]
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
