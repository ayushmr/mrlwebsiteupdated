from django.urls import path
from.import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
urlpatterns = [
path('', views.index, name='index'),
path('form', views.form, name='form'),
path('download', views.excel_view, name='downloadform'),
path('login', auth_views.LoginView.as_view(), name='login'),
path('logout', auth_views.LogoutView.as_view(), name='logout'),
path('newform',views.newform, name='newform')
]