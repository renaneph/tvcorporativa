from django.urls import path
from . import views

urlpatterns = [
    path('user/register/', views.users_register, name='register-user'),
    path('user/list-users/', views.table_users, name='table-users'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('user/change-password/', views.changepassword, name='change-password'),
    path('user/delete/<int:id>', views.deleteuser, name='delete'),
    path('user/edit/<int:id>', views.edituser, name='edit-user'),
]
