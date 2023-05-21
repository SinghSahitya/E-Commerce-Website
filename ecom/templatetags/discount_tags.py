from django import template

register = template.Library()

@register.filter
def discounted(price, discount):
    discount_price = price * (discount/100)
    discounted_price = price - discount_price
    return "{:2f}".format(discounted_price)

@register.filter
def floatmul(value, arg):
    return float(value) * float(arg)

@register.filter
def floatadd(value, arg):
    return float(value) + float(arg)