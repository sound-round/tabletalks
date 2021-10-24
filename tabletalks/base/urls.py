from django.urls import path
from tabletalks.base import views


urlpatterns = [
    path('', views.home, name='home'),
    path('table/<str:pk>/', views.table, name='table'),
]