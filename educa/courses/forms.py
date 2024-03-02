from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module

# Функция inlineformset_factory используется для создания класса ModuleFormSet,
# который представляет собой набор форм для модели Module, которые будут встроены в форму для модели Course.
ModuleFormSet = inlineformset_factory(Course,
                                      Module,
                                      fields=['title',
                                              'description'],  # Поля, которые должны быть представлены в форме
                                      extra=2,  # Количество дополнительных пустых форм
                                      can_delete=True)  # Флаг, указывающий, должна ли форма иметь возможность
                                                        # удаления связанных объектов