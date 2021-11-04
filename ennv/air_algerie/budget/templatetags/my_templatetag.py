from django import template
from budget.models import *
register = template.Library()

@register.simple_tag
def path_pdf(path):
    pdf = lettre.objects.last()
    filepath= pdf.pdf
    return filepath