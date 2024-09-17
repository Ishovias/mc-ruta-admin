from bd.repository import bdmediclean
from datetime import datetime
import params

class SublitoteProductos(bdmediclean):

     def __init__(self) -> None:
          super().__init__(
               hoja=params.ST_PRODUCTOS,
               otrolibro=params.LIBROST
               )

     def listar_productos(self) -> map:
          resultados = super().listar()
          idx = 1
          for fila in resultados["datos"]:
               fila.insert(0,idx)
               idx += 1
          return resultados

     def nuevo_codigo(self) -> int:
          ultimo_codigo = super().getDato(
               fila=self.maxfilas,
               columna=self.hoja_actual["columnas"]["codigo"]
          )
          if ultimo_codigo:
               codigo = int(ultimo_codigo) + 1
          else:
               codigo = 1000
          return codigo

     def nuevo_producto(self, retornaFila: bool=False, retornaCodigo: bool=False, **data) -> bool:
          existencia = super().busca_ubicacion(data["producto"],"producto")
          if existencia:
               return False
          fila = super().busca_ubicacion(columna="codigo")
          codigo = self.nuevo_codigo()
          data["codigo"] = codigo
          for dato in data.keys():
               super().putDato(
                    dato=data[dato], 
                    fila=fila, 
                    columna=str(dato)
                    )
          if retornaFila and retornaCodigo:
               return [fila, codigo]
          elif retornaFila:
               return fila
          elif retornaFila:
               return codigo
          return True
          
     def modifica_producto(self, codigo: str, **data) -> bool:
          fila = super().busca_ubicacion(codigo,"codigo")
          if not fila:
               print("ERROR METODO MODIFICA_PRODUCTO: No existe codigo indicado")
               return False
          try:
               for dato in data.keys():
                    super().putDato(
                         dato=data[dato], 
                         fila=fila, 
                         columna=str(dato)
                         )
          except Exception as e:
               print(f"ERROR METODO MODIFICA_PRODUCTO: {e}")
               return False
          else:
               return True
          
     def elimina_producto(self, codigo: str) -> bool:
          fila = super().busca_ubicacion(codigo,"codigo")
          if not fila:
               print("ERROR METODO ELIMINA_PRODUCTO: No existe codigo indicado")
               return False
          try:
               super().eliminar(fila)
          except Exception as e:
               print(f"ERROR METODO MODIFICA_PRODUCTO: {e}")
               return False
          else:
               return True

class SublitoteCotizacion(bdmediclean):
     
     def __init__(self) -> None:
          super().__init__(
               hoja=params.ST_COTIZACION,
               otrolibro=params.LIBROST
               )
     def cotizacion_existente(self, retornoid: bool=False) -> bool:
          datos_existentes = super().getDato(identificador="numcotizacion")
          if datos_existentes:
               if retornoid:
                    return datos_existentes
               return True
          return False
     
     def idcotizacion(self) -> str:
          nuevoid = format(datetime.now()).replace(" ","").replace(".","").replace(":","").replace("-","")
          return 
          
     def nueva_cotizacion(self, retornoid: bool=False) -> bool:
          if self.cotizacion_existente():
               return False
          newid = self.idcotizacion()
          super().eliminarContenidos()
          if super().putDato(dato=newid, identificador="numcotizacion"):
               if retornoid:
                    return newid
               return True
          return False
     
class SublitoteCotizacionesBD(bdmediclean):
     
     def __init__(self) -> None:
          super().__init__(
               hoja=params.ST_BD_COTIZACIONES,
               otrolibro=params.LIBROST
               )
     
     def guardar_cotizacion(self, idcotizacion: str, datos: list, modificacion: bool=False) -> bool:
          if modificacion:
               filalibre = super().busca_ubicacion(dato=idcotizacion,columna="idcotizacion")
          else:
               filalibre = super().busca_ubicacion(columna="idcotizacion")
          try:
               for fila in datos:
                    fila.insert(0,idcotizacion)
                    super().putDato(
                         datos=fila,
                         fila=filalibre,
                         columna="idcotizacion"
                         )
                    filalibre += 1
               else:
                    for f in range(filalibre,self.maxfilas,1):
                         datosremanentes = super().getDato(fila=f,columna="idcotizacion")
                         if str(datosremanentes) == str(idcotizacion):
                              super().eliminar(f)
          except Exception as e:
               print(f"ERROR METODO GUARDAR_COTIZACION: Error al intentar guardar datos {e}")
               return False
          else:
               return True
               
     def extrae_cotizacion(self, idcotizacion: str) -> list:
          filainicial=super().busca_ubicacion(dato=idcotizacion, columna="idcotizacion")
          listadatos = []
          for f in range(filainicial,self.maxfilas,1):
               datoenfila = super().getDato(fila=f,columna="idcotizacion")
               if str(datoenfila) != str(idcotizacion):
                    break
               listadatos.append(
                    super().extraefila(
                         fila=f,
                         columna="todas",
                         retornostr=True
                         )
                    )
          return listadatos
     
     