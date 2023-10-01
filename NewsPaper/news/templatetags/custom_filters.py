from django import template

censor_list=['запад']
register = template.Library()

@register.filter()
def censor(value):
    if isinstance(value, str):
        words = value.split()
        for i in range(len(words)):
            if words[i].lower() in censor_list:
                if isinstance(words[i], str):
                    words[i] = words[i][0] + '*' * len(words[i - 1])
                else:
                    continue
    else:
        raise AttributeError
    return ' '.join(words)