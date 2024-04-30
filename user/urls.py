from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.signin, name='signin'),
    path('logout/', views.signout, name='signout'),
    path('signup/', views.signup, name='signup'),

]
