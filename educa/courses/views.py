from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Course


# Create your views here.

class ManageCourseListView(ListView):
    model = Course
    template_name = 'courses/manage/course.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)
