"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import HttpResponse
def health(request):
    return HttpResponse("OK")

schema_view = get_schema_view(
    openapi.Info(
        title="Online Courses API",
        default_version='v1',
        description="""
        API для платформы онлайн-курсов

        ## Основные возможности:
        - Просмотр курсов, модулей и уроков
        - Регистрация и авторизация пользователей
        - Покупка курсов
        - Отслеживание прогресса обучения
        - Получение сертификатов
        - Отзывы и поддержка

        ## Аутентификация:
        Используется Basic Authentication. 
        Для тестирования войдите через /api/auth/login/
        """,
        terms_of_service="https://www.skillsup.kg/terms/",
        contact=openapi.Contact(email="support@skilssup.kg"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('courses.urls')),


    path('api-auth/', include('rest_framework.urls')),


    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),


    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)