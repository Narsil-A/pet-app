from django import template

register = template.Library()

@register.filter
def first_ten_words(value):
    words = value.split()[:10]
    return ' '.join(words) + '...'
