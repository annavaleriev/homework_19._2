from django import template
from django.conf import settings

register = template.Library() # Регистрация библиотеки тегов


@register.simple_tag  # Регистрация тега
def media(path):  # Функция тега
    if path: # Если путь существует
        return f"{settings.MEDIA_URL}{path}" # Возвращаем путь к медиафайлу
    return "#" # Иначе возвращаем решетку ( решётка это pass)

# @register.filter() # Регистрация фильтра
# def media(path): # Функция фильтра
#     if path: # Если путь существует
#         return f"/media/{path}" # Возвращаем путь к медиафайлу
#     return "#" # Иначе возвращаем решетку
