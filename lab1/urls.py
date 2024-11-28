from django.contrib import admin
from django.urls import path

from lab1_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.GetMain, name='main'),
    path('component/<int:id>/', views.GetComponent, name='component_url'),
    path('assembly/<int:id>/', views.GetAssembly, name="assembly")
]