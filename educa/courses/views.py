from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.forms.models import modelform_factory
from django.apps import apps
from .forms import ModuleFormSet
from .models import Course
from .models import Module, Content


# Create your views here.
# Создаем представление списка курсов, которые принадлежат текущему пользователю
class ManageCourseListView(ListView):
    model = Course
    template_name = 'courses/manage/course.html'

    # Переопределяем метод get_queryset, чтобы фильтровать список курсов по владельцу
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


# Создаем миксин для фильтрации по владельцу
class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


# Создаем миксин для установки владельца для создаваемого объекта
class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


# Создаем миксин для курсов, который наследуется от OwnerMixin, LoginRequiredMixin и PermissionRequiredMixin
class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


# Создаем миксин для редактирования курсов, который наследуется от OwnerCourseMixin и OwnerEditMixin
class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'


# Создаем представление списка курсов, которые принадлежат текущему пользователю
class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'


# Создаем представление создания курса
class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'


# Создаем представление редактирования курса
class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'


# Создаем представление удаления курса
class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'


# Создаем представление для редактирования модулей курсов
class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None

    # Создаем метод для получения формы для редактирования модулей
    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course,
                             data=data)

    # Переопределяем метод dispatch, чтобы получать курс по его id
    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course,
                                        id=pk,
                                        owner=request.user)
        return super().dispatch(request, pk)

    # Переопределяем метод get, чтобы получать форму для редактирования модулей
    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course,
                                        'formset': formset})

    # Переопределяем метод post, чтобы сохранять изменения в модулях
    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course,
                                        'formset': formset})


# Создаем представление для создания и редактирования контента в модулях курсов
class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    # Создаем метод для получения модели по ее названию
    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses',
                                  model_name=model_name)
        return None

    # Создаем метод для получения формы для модели
    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['owner',
                                                 'order',
                                                 'created',
                                                 'updated'])
        return Form(*args, **kwargs)

    # Переопределяем метод dispatch, чтобы получать модуль и модель по их id
    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module,
                                        id=module_id,
                                        course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         owner=request.user)
        return super().dispatch(request, module_id, model_name, id)

    # Переопределяем метод get, чтобы получать форму для модели
    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj})

    # Переопределяем метод post, чтобы сохранять изменения в модели
    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # new content
                Content.objects.create(module=self.module,
                                       item=obj)
            return redirect('module_content_list', self.module.id)
        return self.render_to_response({'form': form,
                                        'object': self.obj})


class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(Content,
                                    id=id,
                                    module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__owner=request.user)
        return self.render_to_response({'module': module})
