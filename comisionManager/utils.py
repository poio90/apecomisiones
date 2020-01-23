from io import BytesIO
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
