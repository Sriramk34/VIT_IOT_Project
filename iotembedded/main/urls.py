from django.urls import path
from . import views

urlpatterns = [
    path('', views.empty),
    path('index/', views.index),
    path('login/', views.loginout),
    path('control/', views.control),
    #path('report/', views.report),
    #path('admin/', views.adminPanel),
]