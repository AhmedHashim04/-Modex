from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa  # تأكد أنك مثبتها: pip install xhtml2pdf

def generate_invoice_pdf(order):
    template = get_template('order/invoice_template.html')
    context = {
        'order': order,
        'user': order.user,
        'items': order.items.all(),
    }
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    if pdf.err:
        return None
    return result.getvalue()
