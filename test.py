from handlers import RutaBD
from conector import inv_suma_stock

with RutaBD() as rbd:
    decode = rbd.obsdecoder("ca3l1 ba1", solo_decodifica=True)
    print("decode: ",decode)
inv_suma_stock(conjunto=decode)
