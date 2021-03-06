from django.urls import path
from tabletalks.base import views


urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    path('', views.home, name='home'),
    path('table/<str:pk>/', views.table, name='table'),
    path('profile/<str:pk>/', views.user_profile, name='user-profile'),

    path('create-table/', views.create_table, name='create-table'),
    path('update-table/<str:pk>/', views.update_table, name='update-table'),
    path('delete-table/<str:pk>/', views.delete_table, name='delete-table'),

    path('delete-message/<str:pk>/', views.delete_message, name='delete-message'),
]
