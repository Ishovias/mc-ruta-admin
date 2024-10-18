from bd.repository import bdmediclean
from params import RETIROS_ELIMINADOS

class RetirosEliminados(bdmediclean):

     def __init__(self):
          super().__init__(hoja=RETIROS_ELIMINADOS)

     