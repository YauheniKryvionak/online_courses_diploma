from django.urls import path
from . import views

# Список urlpatterns содержит все определенные маршруты для приложения courses.
urlpatterns = [
    # Маршрут для отображения списка курсов пользователя
    path('mine/',
         views.ManageCourseListView.as_view(),
         name='manage_course_list'),
    # Маршрут для создания нового курса
    path('create/',
         views.CourseCreateView.as_view(),
         name='course_create'),
    # Маршрут для редактирования курса
    path('<pk>/edit/',
         views.CourseUpdateView.as_view(),
         name='course_edit'),
    # Маршрут для удаления курса
    path('<pk>/delete/',
         views.CourseDeleteView.as_view(),
         name='course_delete'),
    # Маршрут для обновления модулей курса
    path('<pk>/module/',
         views.CourseModuleUpdateView.as_view(),
         name='course_module_update'),
    # Маршрут для создания контента в модуле курса
    path('module/<int:module_id>/content/<str:model_name>/create/',
         views.ContentCreateUpdateView.as_view(),
         name='module_content_create'),
    # Маршрут для обновления контента в модуле курса
    path('module/<int:module_id>/content/<str:model_name>/<int:id>/',
         views.ContentCreateUpdateView.as_view(),
         name='module_content_update'),
    # Маршрут для удаления контента из модуля курса
    path('content/<int:id>/delete/',
         views.ContentDeleteView.as_view(),
         name='module_content_delete'),
    # Маршрут для отображения списка контента в модуле курса
    path('module/<int:module_id>/',
         views.ModuleContentListView.as_view(),
         name='module_content_list'),
]