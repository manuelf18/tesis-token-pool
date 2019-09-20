from django.contrib.humanize.templatetags.humanize import intcomma
from django.template.defaulttags import register


@register.filter
def decimals(number):
    number = round(float(number), 2)
    return "%s%s" % (intcomma(int(number), False), ("%0.2f" % number)[-3:])


@register.filter
def currency(dollars):
    return 'B/.{}'.format(decimals(dollars))
