from fpdf import FPDF
from pdfgen.cord import Cord
import os

class PDFGen(FPDF):

    def __init__(self, pdf_output: str="rendicion.pdf") -> None:
        super().__init__()# {{{
        self.set_auto_page_break(auto=False, margin=0)
        self.path = os.getcwd() + "/pdfgen/"
        self.path_output = os.getcwd() + "/static/"
        self.nombre_pdf = pdf_output
        # Agregar nueva página
        self.add_page()
        # }}}

    def __enter__(self) -> object:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is None:# {{{
            # Solo guardar si no hay errores
            self.output(self.path_output + self.nombre_pdf)
        return False  # Propagar excepciones}}}

    def set_nombre_pdf(self, nombre: str) -> None:
        self.nombre_pdf = nombre

    def get_nombre_pdf(self, solo_nombre: bool=False) -> str:
        return self.nombre_pdf if solo_nombre else self.path + self.nombre_pdf

    def add_plantilla(self, plantilla_path: str) -> None:
        # Insertar la plantilla JPG como fondo{{{
        plantilla_path = self.path + plantilla_path
        self.image(plantilla_path, x=0, y=0, w=210, h=297)  # Tamaño carta: 210x297 mm
        # Restaurar posición Y para evitar superposición con la imagen
        self.set_y(10)# }}}
    
    def inserta_texto(self, text: str, xy: tuple=(0,0), font_size: int=12) -> None:
        """
        Agrega texto en coordenadas específicas
        x, y: coordenadas en milímetros desde la esquina superior izquierda
        """
        self.set_font('Arial', size=font_size)
        self.text(xy[0], xy[1], text)


