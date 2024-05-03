from django import template

register = template.Library() # Регистрация библиотеки тегов


# Создание тега
@register.simple_tag
def media(path):
    if path:
        return f"/media/{path}"

