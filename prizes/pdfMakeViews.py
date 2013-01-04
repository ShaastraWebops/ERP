from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib import styles
from django.http import HttpResponse

def chilka_view(request):     
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=ReportOnShaastra.pdf'
    doc = SimpleDocTemplate(response)
    Catalog = []
    header = Paragraph("Product Inventory", styles.ParagraphStyle)
    Catalog.append(header)
    style = styles['Normal']
    headings = ('Product Name', 'Product Description')
    allproducts = ['chilka','philka']
    t = Table([headings] + allproducts)
    t.setStyle(TableStyle(
                    [('GRID', (0,0), (1,-1), 2, colors.black),
                     ('LINEBELOW', (0,0), (-1,0), 2, colors.red),
                     ('BACKGROUND', (0, 0), (-1, 0), colors.pink)]))
    Catalog.append(t) 
    doc.build(Catalog)
    return response
