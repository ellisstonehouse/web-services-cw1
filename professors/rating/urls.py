from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('view', views.view, name='view'),
    path('list', views.list, name='list'),
    path('average', views.average, name='average'),
    path('rate', views.rate, name='rate')
]