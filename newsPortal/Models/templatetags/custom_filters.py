from django import template
import re

register = template.Library()


@register.filter()
def censor(text):
    bad_words = ['плохой', 'нехороший', 'дурак', 'дебил', 'news1']
    for word in bad_words:
        text = text.lower().replace(word.lower(), '*' * len(word))
    return text
