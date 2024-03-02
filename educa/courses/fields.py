from django.db import models
from django.core.exceptions import ObjectDoesNotExist


# Пользовательское поле для автоматического назначения порядковых номеров объектов
class OrderField(models.PositiveIntegerField):
    # Инициализация объекта OrderField
    def __init__(self, for_fields=None, *args, **kwargs):
        # Поля, по которым будет выполняться сортировка
        self.for_fields = for_fields
        # Вызов метода __init__ базового класса
        super().__init__(*args, **kwargs)

    # Метод, вызываемый перед сохранением объекта в базу данных
    def pre_save(self, model_instance, add):
        # Проверка, установлен ли текущий порядковый номер
        if getattr(model_instance, self.attname) is None:
            try:
                # Получение всех объектов модели
                qs = self.model.objects.all()
                if self.for_fields:
                    # фильтровать по объектам с одинаковыми значениями полей для полей в "for_fields"
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    qs = qs.filter(**query)
                # Определение следующего порядкового номера
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            # Установка порядкового номера для объекта
            setattr(model_instance, self.attname, value)
            return value
        else:
            # Возврат текущего порядкового номера, если он уже установлен
            return super().pre_save(model_instance, add)
