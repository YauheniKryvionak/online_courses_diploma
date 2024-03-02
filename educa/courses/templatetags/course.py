from django import template

# Импорт библиотеки шаблонов Django
register = template.Library()


# Фильтр для получения имени модели объекта
@register.filter
def model_name(obj):
    try:
        # Пытается получить имя модели объекта
        return obj._meta.model_name
    except AttributeError:
        # Если объект не является экземпляром модели, возвращает None
        return None
