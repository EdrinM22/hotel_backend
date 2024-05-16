from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus.paragraph import Paragraph, ParagraphStyle
from reportlab.platypus.flowables import Spacer
from reportlab.platypus.tables import Table, TableStyle
from reportlab import fonts
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet


class ReservationReceiptPDF:
    def __init__(self, data):
        self.data = data
        self.styles = getSampleStyleSheet()
        self.title_paragraph_center = ParagraphStyle(name='title_Paragraph_center', fontName='Times-Roman', fontSize=22,
                                              alignment=TA_CENTER, style=self.styles['Normal'], leading=20,
                                            )
        self.normal_paragraph_center = ParagraphStyle(name='normal_Paragraph_center', fontName='Times-Roman', fontSize=14,
                                              alignment=TA_CENTER, style=self.styles['Normal'], leading=15,)
        self.small_paragraph_center = ParagraphStyle(name='small_Paragraph_center', fontName='Times-Roman', fontSize=12,
                                              alignment=TA_CENTER, style=self.styles['Normal'], leading=12,)
        self.margin = {
            'leftMargin': 2 * mm,
            'rightMargin': 2 * mm,
            'topMargin': 15 * mm,
            'bottomMargin': 10 * mm
        }


    def _first_page(self):
        title_paragraph = Paragraph("Hotel Moto Moto", style=self.title_paragraph_center)
        normal_paragraph = Paragraph("We thank you for choosing us! The information below shows the information for this receipt", style=self.normal_paragraph_center)
        below_normal_paragraph = Paragraph("This Receipt is different for different customers.", style=self.normal_paragraph_center)
        return [
            title_paragraph,
            normal_paragraph,
            below_normal_paragraph
        ]
    def get_flowables(self):
        flowables = []
        flowables.extend(self._first_page())
        return flowables

    def main(self, request):
        flowables = self.get_flowables()
        simple_doc_template = SimpleDocTemplate(request, pagesize=A4, left_margin=self.margin.get('leftMargin'), right_margin=self.margin.get('rightMargin'),
                                                topMargin=self.margin.get('topMargin'), bottomMargin=self.margin.get('bottomMargin'))
        simple_doc_template.build(flowables)
