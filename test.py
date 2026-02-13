from handlers import RutaBD
from conector import inv_suma_stock

with RutaBD() as rbd:
    conjunto = rbd.obsdecoder("ca3l1 ba1", solo_decodifica=True)
inv_suma_stock(conjunto=conjunto)

