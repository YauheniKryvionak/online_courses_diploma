from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

#  список URL-адресов
urlpatterns = [
    # Определяем URL-адрес для входа в систему
    path('accounts/login/', auth_views.LoginView.as_view(),
         name='login'),
    # Определяем URL-адрес для выхода из системы
    path('accounts/logout/', auth_views.LogoutView.as_view(),
         name='logout'),
    # Определяем URL-адрес для административной панели Django
    path('admin/', admin.site.urls),
    # Определяем URL-адрес для курсов
    path('course/', include('courses.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)