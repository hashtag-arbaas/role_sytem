from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('login/', views.signin, name='signin'),
    path('logout/', views.signout, name='signout'),
    path('signup/', views.signup, name='signup'),

]
