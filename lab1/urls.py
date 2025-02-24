from django.contrib import admin
from django.urls import include, path
from lab1_app import views
from rest_framework import routers


router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path(r'main/', views.ComponentList.as_view(), name='components-list'),
    path(r'component/<int:pk>/', views.ComponentDetail.as_view(), name='components-detail'),
    path(r'component/<int:pk>/put/', views.put, name='components-put'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]

#urlpatterns = [
#    path('admin/', admin.site.urls),
#    path('', views.GetMain, name='main'),
#    path('component/<int:id>/', views.GetComponent, name='componentUrl'),
#    path('assembly/<int:id>/', views.GetAssembly, name="assembly"),
#    path('add', views.AddAssembly, name='addAssembly'),
#    path('del', views.DelAssembly, name='delAssembly')
#]
