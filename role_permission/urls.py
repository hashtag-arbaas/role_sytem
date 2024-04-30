from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('home/', views.home, name='home'),
    path('roles/', views.role_list, name='roles'),
    path('roles/create/', views.create_role, name='create_role'),
    path('permissions/', views.permission_list, name='permissions'),
    path('permissions/create/', views.create_permission, name='create_permission'),
    path('add_permissions/', views.add_permissions, name='add_permissions'),
    path('remove_permissions/', views.remove_permissions, name='remove_permissions'),
    path('roles/fetch_permissions/', views.fetch_permissions, name='fetch_permissions'),
    path('tasks/', views.task_list, name='tasks'),
    path('tasks/<int:pk>', views.task_list, name='tasks'),
    path('tasks/create/', views.create_task, name='create_tasks'),
]
