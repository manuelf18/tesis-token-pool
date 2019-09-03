from django.contrib.humanize.templatetags.humanize import intcomma
from django.template.defaulttags import register


@register.filter
def currency(dollars):
    dollars = round(float(dollars), 2)
    return "B/.%s%s" % (intcomma(int(dollars), False), ("%0.2f" % dollars)[-3:])
