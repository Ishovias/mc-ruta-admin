__all__ = [
        'get_hora_actual',
        'fecha_formato',
        'fecha_actual',
        'formato_moneda'
        ]

from datetime import datetime
from cimprime import cimprime
import params

# ----------------- FUNCIONES MISCELANEAS ---------------------------

def get_hora_actual(obtener_clase: bool=False) -> str:
    hora_servidor = datetime.now()# {{{
    mes_actual = datetime.today().month
    if mes_actual in params.MESES_HORARIO_INVIERNO:
        diferencia_hr = timedelta(hours=params.DIF_HR_INVIERNO)
    elif mes_actual in params.MESES_HORARIO_VERANO:
        diferencia_hr = timedelta(hours=params.DIF_HR_VERANO)
    hora_calculada = hora_servidor + diferencia_hr
    return hora_calculada if obtener_clase else hora_calculada.strftime(params.FORMATO_HORA)# }}}

def fecha_formato(fecha: str, formato_origen: str, formato_destino: str) -> str:
    fecha = str(fecha)# {{{
    formatos = {
            "vista":params.FORMATO_FECHA,
            "codigo":params.FORMATO_FECHA_CODIGO,
            "explorador":params.FORMATO_FECHA_EXPLORADOR
            }
    try:
        f = datetime.strptime(fecha, formatos.get(formato_origen))
    except:
        print("fecha_formato: Error al convertir fecha",
                f"\nFecha: {fecha}\nFormato Origen: {formato_origen}\nFormato Destino: {formato_destino}")
        return None
    else:
        return datetime.strftime(f, formatos.get(formato_destino))# }}}

def fecha_actual(formato: str="codigo") -> str:
    formatos = {# {{{
            "vista":params.FORMATO_FECHA,
            "codigo":params.FORMATO_FECHA_CODIGO,
            "explorador":params.FORMATO_FECHA_EXPLORADOR
            }
    if formato not in formatos:
        cimprime(
                titulo="Error en helpers.py/fecha_actual",
                error=f"Formato '{formato}' indicado no existe"
                )
        return None
    return datetime.strftime(datetime.today(),formatos.get(formato))# }}}

def formato_moneda(monto: str) -> str:
    monto = str(monto)# {{{
    monto = list(monto)
    monto.reverse()
    monto_construido = []
    count = 0
    for i in monto:
        if count == 3:
            count = 0
            monto_construido.append(",")
        monto_construido.append(i)
        count += 1
    monto_construido.reverse()
    if monto_construido[0] == "-" and monto_construido[1] == ",":
        monto_construido.remove(monto_construido[1])
    monto_construido.insert(0,"$")
    return "".join(monto_construido)# }}}
