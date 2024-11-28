from django.contrib import admin
from django.urls import path

from lab1_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.GetMain, name='main'),
    path('component/<int:id>/', views.GetComponent, name='componentUrl'),
    path('assembly/<int:id>/', views.GetAssembly, name="assembly"),
    path('add', views.AddAssembly, name='addAssembly'),
    path('del', views.DelAssembly, name='delAssembly')
]