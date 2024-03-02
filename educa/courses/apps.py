from django.apps import AppConfig


# Конфигурация приложения 'courses'
class CoursesConfig(AppConfig):
    # Указываем, какое поле будет использоваться по умолчанию для автоматически генерируемых первичных ключей
    default_auto_field = 'django.db.models.BigAutoField'
    # Указываем полное Python-имя приложения
    name = 'courses'
