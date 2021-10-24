from django.urls import path
from tabletalks.base import views


urlpatterns = [
    path('', views.home, name='home'),
    path('table/<str:pk>/', views.table, name='table'),
    path('create-table/', views.create_table, name='create-table'),
    path('update-table/<str:pk>/', views.update_table, name='update-table'),
    path('delete-table/<str:pk>/', views.delete_table, name='delete-table'),
]
