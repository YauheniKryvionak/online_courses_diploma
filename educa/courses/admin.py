from django.contrib import admin
from .models import Subject, Course, Module


# Регистрация моделей в админ-панели

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    # Отображаемые поля в списке предметов
    list_display = ['title', 'slug']
    # Автоматически генерируем slug из названия предмета
    prepopulated_fields = {'slug': ('title',)}


# Встроенный интерфейс для модулей внутри страницы редактирования курса
class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # Отображаемые поля в списке курсов
    list_display = ['title', 'subject', 'created']
    # Доступные фильтры
    list_filter = ['created', 'subject']
    # Поля для поиска
    search_fields = ['title', 'overview']
    # Автоматически генерируем slug из названия курса
    prepopulated_fields = {'slug': ('title',)}
    # Встроенный интерфейс для модулей
    inlines = [ModuleInline]
