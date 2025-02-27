from django.contrib import admin
from django.urls import path
from drf_yasg.views import get_schema_view

from lab1_app.views import *

schema_view = get_schema_view(
    openapi.Info(
        title="RASA API",
        default_version='v1',
        description="RASA Web Service",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),

    # Компоненты
    path('api/components/', ComponentList.as_view(), name='component-list'),
    path('api/components/<int:pk>/', ComponentDetail.as_view(),
         name='component-detail'),
    path('api/components/<int:pk>/add-to-draft/',
         AddComponentToDraftAPIView.as_view(), name='add-component-to-draft'),
    path('api/components/<int:pk>/draft/',
         DraftComponentManagementAPIView.as_view(),
         name='remove-component-from-draft'),

    # Сборapi/ки
    path('api/assemblies/', AssemblyListAPIView.as_view(),
         name='assembly-list'),
    path('api/assemblies/<int:pk>/', AssemblyDetailAPIView.as_view(),
         name='assembly-detail'),
    path('api/assemblies/<int:pk>/form/', AssemblyFormAPIView.as_view(),
         name='assembly-form'),
    path('api/assemblies/<int:pk>/moderate/',
         AssemblyCompleteRejectAPIView.as_view(),
         name='assembly-status-update'),

    # Аутеapi/нтификация пользователей
    path('api/auth/register/', UserRegistrationAPIView.as_view(),
         name='user-register'),
    path('api/auth/profile/', UserProfileUpdateAPIView.as_view(),
         name='user-profile-update'),
    path('api/auth/login/', UserLoginAPIView.as_view(), name='user-login'),
    path('api/auth/logout/', UserLogoutAPIView.as_view(), name='user-logout'),
]
