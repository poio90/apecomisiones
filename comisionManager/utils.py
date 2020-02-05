from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

def render_pdf(url_template, context={}):
    """Renderiza un template Django a un documento PDF"""
    template = get_template(url_template)
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='aplication/pdf')
    else:
        return HttpResponse("Error Rendering PDF", status=400)


"""def render_pdf2(request):
    ReportLab para generar PDF
    buffer = BytesIO
    c = canvas.Canvas(buffer, pagesize=A4)
   
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf"""

