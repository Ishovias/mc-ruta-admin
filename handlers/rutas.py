from bd.repository import bdmediclean
from helpers import cimprime
import params

class RutaActual(bdmediclean):

    def __init__(self) -> None:
        super().__init__(params.RUTA_ACTUAL, otrolibro=params.LIBRORUTA)

    def nueva_ruta(self, fecha: str, ruta: str) -> bool:
        filadatos = self.hoja_actual["filadatos"]
        for dato, columna in [(fecha,"fecharuta"),(ruta,"nombreruta")]:
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

    def importar(self, datos: map) -> bool:
        super().putDato(dato=datos["fecharuta"],identificador="fecharuta")
        super().putDato(dato=datos["nombreruta"],identificador="nombreruta")
        super().eliminarContenidos()
        filaubicacion = self.hoja_actual["filainicial"]
        for fila in datos["datos"]:
            super().putDato(datos=fila,fila=filaubicacion,columna="fecha")
            filaubicacion += 1
        else:
            return True
        return False

class RutaRegistros(bdmediclean):

    def __init__(self) -> None:
        super().__init__(params.RUTAS_REGISTROS)

    def nueva_ruta(self, fecha: str, ruta: str) -> None:
        ubicacion = super().buscafila()
        super().putDato(
                dato=fecha,
                fila=ubicacion,
                columna="fecharuta"
                )
        super().putDato(
                dato=ruta,
                fila=ubicacion,
                columna="nombreruta"
                )

    def ubicacion_registro(self, datos: map) -> int:
        fechasruta = super().buscadato(
                dato=datos["fecharuta"],
                columna="fecharuta",
                exacto=True,
                buscartodo=True
                )
        nombresruta = super().buscadato(
                dato=datos["fecharuta"],
                columna="fecharuta",
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
                dato=int(cantidad_actual) + cantidad,
                fila=fila,
                columna=confpos
                )

    def registra_importacion(self, datos: map) -> bool:
        pass

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
               filainicio = super().buscadato(dato=str(fechainicio),columna="fecha")
               filafinal = super().buscadato(dato=str(fechafinal),columna="fecha")
               if not filainicio and not filafinal:
                   self.kilosItems = items
                   return items
               for i in range(filafinal, super().getmaxfilas(),1):
                    dato = super().getDato(fila=i,columna="fecha")
                    if str(dato) != str(fechafinal):
                         filafinal = i
                         break
               for item in items:
                   for f in range(filainicio,filafinal,1):
                       dato = super().getDato(fila=f,columna=item)
                       if dato:
                              items[item] += int(dato)
                              self.kilosItems[item] += int(dato)
         return items

         if filaCliente:
               for item in items:
                  dato = super().getDato(fila=filaCliente,columna=item)
                  if dato:
                     items[item] += int(dato)
                     self.kilosItems[item] += int(dato)
               return items

         return None

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

class RutaImportar(bdmediclean):

     def __init__(self, archivo: str) -> None:
          super().__init__(params.RUTA_ACTUAL, otrolibro=str(archivo))
          self.hoja_actual = params.RUTA_ACTUAL

     def extrae_ruta(self) -> map:
         return {
                 "fecha": super().getDato(identificador="fecha", retornostr=True),
                 "nombreruta": super().getDato(identificador="nombreruta", retornostr=True),
                 "datos":super().listar(retornostr=True, solodatos=True)
                 }
